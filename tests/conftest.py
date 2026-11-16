"""9_1 的 fixture 作用域判据：函数级每次新建，会话级只放不可变对象。"""

import pytest


@pytest.fixture
def fresh_config() -> dict[str, list[str]]:
    """每次返回新建字典。若改成会话级，用例之间就会通过它隐式耦合。"""
    return {"items": []}


@pytest.fixture(scope="session")
def readonly_labels() -> tuple[str, ...]:
    """作用域很大，但返回不可变元组，无法被任何用例改写。"""
    return ("a", "b", "c")
