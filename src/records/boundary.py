"""承载 11_1 的机理：配置四级优先、错误分类、退避抖动、幂等键、存活/就绪两分探针、结构化日志。"""

from __future__ import annotations

import logging
import os
import random
import time
from dataclasses import dataclass
from typing import Callable, Mapping

LOGGER = logging.getLogger("records")


class ConfigError(RuntimeError):
    """必填配置缺失或取值不合法。"""


class Unavailable(RuntimeError):
    """暂时性失败，是唯一允许重试的错误类别。"""


class BadRequest(ValueError):
    """确定性失败：参数或鉴权错误，重试多少次结果都一样。"""


@dataclass(frozen=True)
class Config:
    endpoint: str
    timeout_ms: int

    @classmethod
    def from_sources(
        cls,
        *,
        defaults: Mapping[str, str] | None = None,
        file_values: Mapping[str, str] | None = None,
        env: Mapping[str, str] | None = None,
        cli: Mapping[str, str] | None = None,
    ) -> "Config":
        """优先级：内置默认 < 配置文件 < 环境变量 < 显式参数。

        endpoint 是必填项，四级都没有值时启动即报错，绝不静默拼一个能用的地址。
        """
        merged: dict[str, str] = {}
        # 真实环境变量惯例用大写；四级来源统一归一化后再合并。
        aliases = {
            "endpoint": "endpoint", "ENDPOINT": "endpoint", "RECORDS_ENDPOINT": "endpoint",
            "timeout_ms": "timeout_ms", "TIMEOUT_MS": "timeout_ms", "RECORDS_TIMEOUT_MS": "timeout_ms",
        }
        for layer in (defaults or {}, file_values or {}, env if env is not None else os.environ, cli or {}):
            for key, value in layer.items():
                if key in aliases:
                    merged[aliases[key]] = value
        endpoint = merged.get("endpoint")
        if not endpoint:
            raise ConfigError("missing required config: endpoint")
        raw_timeout = merged.get("timeout_ms", "800")
        try:
            timeout_ms = int(raw_timeout)
        except ValueError as exc:
            raise ConfigError(f"invalid timeout_ms: {raw_timeout}") from exc
        return cls(endpoint=endpoint, timeout_ms=timeout_ms)


def fetch_with_retry(
    key: str,
    call: Callable[[str], int],
    *,
    attempts: int = 4,
    base_seconds: float = 0.001,
    budget_seconds: float = 0.05,
    sleep: Callable[[float], None] | None = None,
) -> int:
    """退避加抖动、错误分类、总耗时预算、幂等键由入口生成且全程不变。

    sleep 可注入，测试用 monkeypatch 替换"被查找处"的名称，而不是替换 time 模块定义处。
    """
    nap = sleep if sleep is not None else time.sleep
    started = time.monotonic()
    last: Exception | None = None
    for attempt in range(attempts):
        if time.monotonic() - started > budget_seconds:
            raise Unavailable(f"budget exhausted for {key}") from last
        try:
            return call(key)
        except Unavailable as exc:
            last = exc
        except BadRequest as exc:
            raise BadRequest(f"non-retryable for {key}") from exc
        wait = base_seconds * (2**attempt) + random.uniform(0, base_seconds / 2)
        remaining = budget_seconds - (time.monotonic() - started)
        if remaining <= 0:
            raise Unavailable(f"budget exhausted for {key}") from last
        nap(min(wait, remaining))
    raise Unavailable(f"attempts exhausted for {key}") from last


class IdempotentStore:
    """同一幂等键重复提交返回首次结果，不产生第二条记录。"""

    def __init__(self) -> None:
        self._seen: dict[str, int] = {}

    def apply(self, key: str, compute: Callable[[], int]) -> tuple[int, bool]:
        if key in self._seen:
            return self._seen[key], False
        value = compute()
        self._seen[key] = value
        return value, True


def degradation_kinds() -> tuple[str, ...]:
    """四种降级形态，评审时不能只写"返回兜底"。"""
    return ("empty_result", "timestamped_cache", "explicit_error", "queued_acceptance")


def liveness() -> bool:
    """只判本进程是否活着，不查依赖，避免下游抖动触发全体重启。"""
    return True


def readiness(
    store: IdempotentStore,
    probe: Callable[[], bool] | None = None,
) -> bool:
    """存活之外的就绪判定：先做结构守卫，再执行注入的依赖探针。

    生产调用应传入 probe，让它真实反映依赖状态；依赖未就绪时摘流量，但不重启进程。
    """
    if store is None or not callable(getattr(store, "apply", None)):
        return False
    return True if probe is None else bool(probe())


def structured_log(request_id: str, event: str, **fields: object) -> None:
    """按字段输出，靠请求标识串起整条链路。"""
    LOGGER.info("%s", event, extra={"request_id": request_id, **fields})
