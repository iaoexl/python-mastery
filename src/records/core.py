"""承载 2_1 / 3_1 / 4_1 / 7_1 的机理：名称绑定、共享容器、拷贝深度、金额精度。"""

from __future__ import annotations

import copy
from decimal import Decimal
from typing import Dict, Iterable, List, Mapping, Sequence, TypedDict, cast


class SpecError(ValueError):
    """解析失败，可被 pytest.raises 的 match 锁定关键消息。"""


class Record(TypedDict):
    region: str
    amount: Decimal


def _label(row: Record, key: str) -> str:
    """把 TypedDict 当只读映射取动态键。

    直接写 row[key] 会被类型检查拒绝：TypedDict 的键必须是字面量。
    这里显式 cast 到 Mapping，既保留运行时的通用分组，又不把动态键伪装成类型安全。
    """
    return str(cast(Mapping[str, object], row)[key])


def parse_spec(text: str, *, extra: List[str] | None = None) -> List[str]:
    """演示可变默认参数的正确写法：默认值用 None 占位，函数体内新建。

    若写成 extra=[]，连续两次调用会共享同一个列表，第二次"记住"第一次的内容。
    """
    if extra is None:
        extra = []
    parts = [p.strip() for p in text.split(":") if p.strip()]
    if not parts:
        raise SpecError("empty spec")
    extra.extend(parts)
    return extra


def group_by(rows: Iterable[Record], key: str) -> Dict[str, List[Record]]:
    """正确写法：推导式/setdefault 每次迭代新建列表，每个键各自持有独立对象。"""
    out: Dict[str, List[Record]] = {}
    for row in rows:
        out.setdefault(_label(row, key), []).append(row)
    return out


def group_by_shared(rows: Iterable[Record], key: str) -> Dict[str, List[Record]]:
    """反模式：第二参数只求值一次，所有键共享同一个列表。

    只用于让测试主动把它变红，生产代码不要调用。
    """
    keys = [_label(row, key) for row in rows]
    return dict.fromkeys(keys, [])


def snapshot(rows: Sequence[Record]) -> List[Record]:
    """深拷贝：元素对象也递归新建，改副本不影响原数据。"""
    return copy.deepcopy(list(rows))


def shallow_window(rows: Sequence[Record], n: int) -> List[Record]:
    """切片只复制外层引用，元素对象仍与原容器共享。"""
    return list(rows[:n])


def total_amount(rows: Iterable[Record]) -> Decimal:
    """金额用 Decimal 累加，避免二进制浮点把 0.1 加出尾差。"""
    return sum((row["amount"] for row in rows), Decimal("0"))


def parse_batch(lines: Iterable[str]) -> tuple[int, list[str]]:
    """批量解析：成功项累加，失败项连同原始输入逐条留痕，不吞掉任何一条。"""
    total = 0
    errors: list[str] = []
    for i, line in enumerate(lines, start=1):
        try:
            parts = parse_spec(line)
            total += int(parts[-1])
        except ValueError as exc:
            errors.append(f"line {i}: {exc}")
    return total, errors


def load_payload(blob: bytes, *, trusted: bool) -> object:
    """反序列化红线：不可信输入不进入可构造对象的通道。

    这里刻意不做任何解码，只保留一道显式闸门；测试用它验证"拒绝"而非"解析成功"。
    """
    if not trusted:
        raise SpecError("untrusted payload refused before deserialization")
    raise SpecError("no decoder configured: keep the boundary explicit")
