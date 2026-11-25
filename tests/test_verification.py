from types import SimpleNamespace

import dns.resolver

from openprospect import verification


def test_email_syntax_and_disposable_domain_checks():
    invalid = verification.verify_email("not-an-email", smtp_probe=False)
    assert invalid["status"] == "invalid"
    assert not invalid["syntax_valid"]

    disposable = verification.verify_email("person@mailinator.com", smtp_probe=False)
    assert disposable["status"] == "invalid"
    assert disposable["disposable"] is True


def test_email_verified_only_when_mx_and_non_catchall_smtp_accept(monkeypatch):
    monkeypatch.setattr(
        dns.resolver, "resolve",
        lambda domain, record_type, lifetime: [SimpleNamespace(preference=10, exchange="mx.example.test.")],
    )
    monkeypatch.setattr(verification, "_smtp_check", lambda host, address: {
        "target_accepted": True, "target_code": 250, "target_message": "accepted",
        "catch_all": False, "catch_all_code": 550, "catch_all_message": "unknown recipient",
    })
    result = verification.verify_email("info@example.test")
    assert result["status"] == "verified"
    assert result["role_account"] is True
    assert verification.is_deliverable(result)


def test_catchall_and_guessed_addresses_never_become_deliverable(monkeypatch):
    monkeypatch.setattr(
        dns.resolver, "resolve",
        lambda domain, record_type, lifetime: [SimpleNamespace(preference=10, exchange="mx.example.test.")],
    )
    monkeypatch.setattr(verification, "_smtp_check", lambda host, address: {
        "target_accepted": True, "target_code": 250, "target_message": "accepted",
        "catch_all": True, "catch_all_code": 250, "catch_all_message": "accepted",
    })
    catchall = verification.verify_email("alex@example.test")
    assert catchall["status"] == "risky"
    assert not verification.is_deliverable(catchall)

    guess = verification.verify_email("alex@example.test", is_guess=True)
    assert guess["status"] == "guess"
    assert not verification.is_deliverable(guess)


def test_email_pattern_learning_and_guess_labels():
    pattern = verification.learn_email_pattern([
        {"name": "Nora Vale", "email": "nora.vale@example.test"},
        {"name": "Alex Kim", "email": "alex.kim@example.test"},
    ])
    assert pattern == "first.last"
    guess = verification.guess_email("Jamie", "Fox", "example.test", pattern)
    assert guess == {
        "address": "jamie.fox@example.test",
        "status": "guess",
        "pattern": "first.last",
    }
