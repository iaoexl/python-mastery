import logging
import time

import pytest

from records import boundary
from records.boundary import (
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


def test_config_priority_default_file_env_cli():
    cfg = Config.from_sources(
        defaults={"endpoint": "from-default", "timeout_ms": "100"},
        file_values={"endpoint": "from-file", "timeout_ms": "200"},
        env={"endpoint": "from-env"},
        cli={"endpoint": "from-cli"},
    )
    assert cfg.endpoint == "from-cli"
    assert cfg.timeout_ms == 200


def test_config_accepts_uppercase_environment_keys():
    cfg = Config.from_sources(env={"ENDPOINT": "from-env", "TIMEOUT_MS": "300"})
    assert (cfg.endpoint, cfg.timeout_ms) == ("from-env", 300)


def test_config_reads_real_environment(monkeypatch):
    monkeypatch.setenv("ENDPOINT", "from-os")
    monkeypatch.setenv("TIMEOUT_MS", "450")
    cfg = Config.from_sources()
    assert (cfg.endpoint, cfg.timeout_ms) == ("from-os", 450)


def test_config_missing_required_fails_loudly():
    with pytest.raises(ConfigError, match="missing required config"):
        Config.from_sources(defaults={}, file_values={}, env={}, cli={})


def test_config_invalid_timeout_keeps_cause():
    with pytest.raises(ConfigError, match="invalid timeout_ms") as info:
        Config.from_sources(defaults={"endpoint": "x", "timeout_ms": "not-a-number"}, env={})
    assert isinstance(info.value.__cause__, ValueError)


def test_retry_only_for_transient_failures():
    calls = {"n": 0}

    def call(key):
        calls["n"] += 1
        if calls["n"] < 3:
            raise Unavailable("downstream slow")
        return 7

    assert fetch_with_retry("k", call, sleep=lambda _: None) == 7
    assert calls["n"] == 3


def test_deterministic_failure_is_never_retried():
    calls = {"n": 0}

    def call(key):
        calls["n"] += 1
        raise BadRequest("bad parameter")

    with pytest.raises(BadRequest, match="non-retryable"):
        fetch_with_retry("k", call, sleep=lambda _: None)
    assert calls["n"] == 1


def test_retry_budget_exhaustion_raises():
    def call(key):
        raise Unavailable("always down")

    with pytest.raises(Unavailable, match="budget exhausted"):
        fetch_with_retry("k", call, attempts=10, base_seconds=0.02,
                         budget_seconds=0.005, sleep=time.sleep)


def test_monkeypatch_hits_the_lookup_site(monkeypatch):
    """替换要打在 records.boundary 里被查找的那个名称，而不是别处。"""
    seen = []
    monkeypatch.setattr(boundary.time, "sleep", lambda s: seen.append(s))
    calls = {"n": 0}

    def call(key):
        calls["n"] += 1
        if calls["n"] < 2:
            raise Unavailable("slow")
        return 1

    assert fetch_with_retry("k", call, attempts=3, base_seconds=0.002) == 1
    assert len(seen) == 1 and seen[0] > 0  # 抖动后的退避确实被调用


def test_idempotent_key_returns_first_result():
    store = IdempotentStore()
    first, created = store.apply("req-1", lambda: 42)
    again, created_again = store.apply("req-1", lambda: 999)
    assert (first, created) == (42, True)
    assert (again, created_again) == (42, False)


def test_degradation_is_enumerated_not_vague():
    assert degradation_kinds() == (
        "empty_result", "timestamped_cache", "explicit_error", "queued_acceptance",
    )


def test_probes_are_separate():
    assert liveness() is True
    assert readiness(IdempotentStore()) is True
    assert readiness(None) is False


def test_readiness_runs_injected_dependency_probe():
    assert readiness(IdempotentStore(), probe=lambda: True) is True
    assert readiness(IdempotentStore(), probe=lambda: False) is False


def test_idempotent_key_keeps_falsy_first_result():
    store = IdempotentStore()
    first = store.apply("zero", lambda: 0)
    again = store.apply("zero", lambda: 99)
    assert first == (0, True)
    assert again == (0, False)


def test_structured_log_carries_request_id(caplog):
    with caplog.at_level(logging.INFO, logger="records"):
        structured_log("req-1", "evt", step="check")
    record = caplog.records[-1]
    assert record.request_id == "req-1"
    assert record.step == "check"


def test_retry_budget_checked_after_a_slow_failure():
    def call(key):
        time.sleep(0.02)  # 单次调用本身就吃光预算
        raise Unavailable("slow call")

    with pytest.raises(Unavailable, match="budget exhausted"):
        fetch_with_retry("k", call, attempts=5, budget_seconds=0.005, sleep=lambda _: None)


def test_retry_attempts_exhaustion_raises():
    def call(key):
        raise Unavailable("always down")

    with pytest.raises(Unavailable, match="attempts exhausted"):
        fetch_with_retry("k", call, attempts=2, base_seconds=0,
                         budget_seconds=10, sleep=lambda _: None)
