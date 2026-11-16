"""records：按知识库板块拆分的可验证实现。

包顶层只放定义，不写有副作用的启动逻辑；入口与门禁都在 scripts 下。
"""

from .boundary import (
    BadRequest,
    Config,
    ConfigError,
    IdempotentStore,
    Unavailable,
    degradation_kinds,
    fetch_with_retry,
    liveness,
    readiness,
    structured_log,
)
from .core import (
    SpecError,
    group_by,
    group_by_shared,
    load_payload,
    parse_batch,
    parse_spec,
    shallow_window,
    snapshot,
    total_amount,
)
from .workers import run_all

__all__ = [
    "BadRequest", "Config", "ConfigError", "IdempotentStore", "Unavailable",
    "SpecError", "degradation_kinds", "fetch_with_retry", "liveness",
    "readiness", "structured_log", "group_by", "group_by_shared",
    "load_payload", "parse_batch", "parse_spec", "shallow_window",
    "snapshot", "total_amount", "run_all",
]
