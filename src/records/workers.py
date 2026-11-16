"""承载 8_1 / 8_4：Future.result 才是异常的出口，完成数量不等于结果正确。"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def run_all(
    items: list[T],
    fn: Callable[[T], R],
    *,
    workers: int = 4,
) -> tuple[list[R], list[dict[str, str]]]:
    """按完成顺序消费，逐个调用 result() 把异常回收到调用方。

    只统计"完成数量"会漏掉封装在 Future 里的失败，因此这里显式维护死信列表，
    每条都保留原始输入与异常文本，便于重试或对账。
    """
    results: list[R] = []
    dead_letters: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(fn, item): item for item in items}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as exc:  # 汇总到死信，不吞、不静默
                dead_letters.append({"item": str(futures[future]), "error": repr(exc)})
    return results, dead_letters
