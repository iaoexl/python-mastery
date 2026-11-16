from records.workers import run_all


def double(x):
    return x * 2


def test_run_all_on_empty_input_returns_two_empty_lists():
    results, dead = run_all([], double)
    assert results == [] and dead == []


def test_run_all_collects_every_result():
    results, dead = run_all([1, 2, 3, 4, 5], double, workers=3)
    assert sorted(results) == [2, 4, 6, 8, 10]
    assert dead == []


def test_failure_goes_to_dead_letters_not_silently_dropped():
    def sometimes(x):
        if x == 3:
            raise RuntimeError("boom")
        return double(x)

    results, dead = run_all([1, 2, 3, 4], sometimes, workers=2)
    assert sorted(results) == [2, 4, 8]
    assert len(dead) == 1
    assert dead[0]["item"] == "3"
    assert "boom" in dead[0]["error"]


def test_completion_count_alone_would_hide_the_failure():
    """只数"完成了几个 Future"会得到 4，但真正可用的结果只有 3 个。"""
    def sometimes(x):
        if x == 3:
            raise RuntimeError("boom")
        return double(x)

    results, dead = run_all([1, 2, 3, 4], sometimes, workers=2)
    assert len(results) + len(dead) == 4
    assert len(results) < 4
