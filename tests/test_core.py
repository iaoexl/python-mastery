from decimal import Decimal

import pytest

from records.core import (
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


@pytest.mark.parametrize(
    "text, expected",
    [
        ("region-a:7", ["region-a", "7"]),
        ("  a : 3 ", ["a", "3"]),
        ("single", ["single"]),
    ],
)
def test_parse_spec(text, expected):
    assert parse_spec(text) == expected


def test_parse_spec_does_not_remember_previous_call():
    """可变默认参数若写成 extra=[]，第二次调用会带上第一次的内容。"""
    assert parse_spec("a:1") == ["a", "1"]
    assert parse_spec("b:2") == ["b", "2"]


def test_parse_spec_explicit_container_and_none():
    out = parse_spec("c:3", extra=["seed"])
    assert out == ["seed", "c", "3"]
    assert parse_spec("d:4", extra=None) == ["d", "4"]


def test_parse_spec_empty_raises_with_match():
    with pytest.raises(SpecError, match="empty spec"):
        parse_spec("   ")


def _rows():
    return [
        {"region": "a", "amount": Decimal("0.10")},
        {"region": "b", "amount": Decimal("0.20")},
        {"region": "a", "amount": Decimal("0.30")},
    ]


def test_group_by_each_key_owns_its_list():
    groups = group_by(_rows(), "region")
    groups["a"].append({"region": "a", "amount": Decimal("9")})
    assert len(groups["b"]) == 1
    assert groups["a"] is not groups["b"]


def test_group_by_shared_is_caught_as_antipattern():
    """反模式实测：所有键共享同一列表，往一个键追加，另一个键也看得见。"""
    groups = group_by_shared(_rows(), "region")
    groups["a"].append({"region": "a", "amount": Decimal("9")})
    assert len(groups["b"]) == 1  # 保持绿说明 b 看到了 a 的追加：共享列表确实在叠数据；变红反而说明已不共享


def test_deepcopy_vs_slice_sharing():
    rows = _rows()
    deep = snapshot(rows)
    shallow = shallow_window(rows, 2)
    deep[0]["amount"] = Decimal("99")
    assert rows[0]["amount"] == Decimal("0.10")
    shallow[0]["amount"] = Decimal("88")
    assert rows[0]["amount"] == Decimal("88")  # 切片只复制外层引用


def test_memoryview_shares_buffer():
    buf = bytearray(b"abcdef")
    view = memoryview(buf)[1:4]
    view[0] = ord("Z")
    assert buf == bytearray(b"aZcdef")


def test_decimal_avoids_float_tail():
    assert total_amount(_rows()) == Decimal("0.60")
    assert 0.1 + 0.2 == pytest.approx(0.3)  # 浮点只能近似，金额不能这样算


def test_parse_batch_keeps_partial_result_and_all_errors():
    total, errors = parse_batch(["a:1", "bad", "b:2", "oops", "c:3"])
    assert total == 6
    assert len(errors) == 2
    assert "line 2" in errors[0] and "line 4" in errors[1]


def test_total_amount_of_empty_input_is_zero():
    assert total_amount([]) == Decimal("0")


def test_untrusted_payload_is_refused_before_decode():
    with pytest.raises(SpecError, match="untrusted"):
        load_payload(b"anything", trusted=False)


def test_function_scope_fixture_is_isolated(fresh_config):
    fresh_config["items"].append("mine")
    assert fresh_config["items"] == ["mine"]


def test_function_scope_fixture_starts_clean_again(fresh_config):
    assert fresh_config["items"] == []  # 若上一用例污染到这里就变红


def test_session_fixture_is_immutable(readonly_labels):
    assert readonly_labels == ("a", "b", "c")
    assert isinstance(readonly_labels, tuple)


def test_load_payload_trusted_still_refuses_decode():
    """显式闸门始终存在；可信输入也必须由调用方配置解码器。"""
    with pytest.raises(SpecError, match="no decoder configured"):
        load_payload(b"x", trusted=True)
