import sqlite3

import pytest

from vault import crypto, repository

NEW_SALT = b"fedcba9876543210"


def test_add_and_get(conn, key):
    repository.add_entry(conn, key, "github", "nik", "pass123", tags=["work"])
    entry = repository.get_entry(conn, key, "github")
    assert entry["password"] == "pass123"
    assert entry["login"] == "nik"


def test_password_is_stored_encrypted(conn, key):
    repository.add_entry(conn, key, "github", "nik", "pass123")
    raw = conn.execute("SELECT password_encrypted FROM entries").fetchone()[0]
    assert b"pass123" not in raw


def test_get_missing_returns_none(conn, key):
    assert repository.get_entry(conn, key, "nope") is None


def test_duplicate_service_raises(conn, key):
    repository.add_entry(conn, key, "gh", "u", "p")
    with pytest.raises(sqlite3.IntegrityError):
        repository.add_entry(conn, key, "gh", "u", "p")


def test_normalize_tags():
    assert repository.normalize_tags(["Work", " study ", "work", ""]) == ",study,work,"
    assert repository.normalize_tags([]) == ""


def test_pagination(conn, key):
    for i in range(25):
        repository.add_entry(conn, key, f"svc{i:02}", "u", "p")
    rows, total = repository.list_entries(conn, page=3, size=10)
    assert total == 25
    assert len(rows) == 5


def test_tag_filter_is_exact(conn, key):
    repository.add_entry(conn, key, "a", "u", "p", tags=["homework"])
    repository.add_entry(conn, key, "b", "u", "p", tags=["work"])
    rows, _ = repository.list_entries(conn, tag="work")
    assert [r["service"] for r in rows] == ["b"]


def test_search_filter(conn, key):
    for name in ("github", "gitlab", "netflix"):
        repository.add_entry(conn, key, name, "u", "p")
    _, total = repository.list_entries(conn, search="git")
    assert total == 2


def test_update_password(conn, key):
    repository.add_entry(conn, key, "gh", "u", "old")
    assert repository.update_password(conn, key, "gh", "new") is True
    assert repository.get_entry(conn, key, "gh")["password"] == "new"


def test_update_missing_returns_false(conn, key):
    assert repository.update_password(conn, key, "nope", "x") is False


def test_delete_entry(conn, key):
    repository.add_entry(conn, key, "gh", "u", "p")
    assert repository.delete_entry(conn, "gh") is True
    assert repository.get_entry(conn, key, "gh") is None
    assert repository.delete_entry(conn, "gh") is False


def test_change_master_success(conn, key):
    conn.execute(
        "INSERT INTO meta (id, salt, check_token) VALUES (1, ?, ?)",
        (b"0123456789abcdef", crypto.make_check(key)),
    )
    repository.add_entry(conn, key, "a", "u", "pass-a")
    repository.add_entry(conn, key, "b", "u", "pass-b")

    new_key = crypto.derive_key("new-master", NEW_SALT)
    repository.change_master(conn, key, new_key, NEW_SALT)

    assert repository.get_entry(conn, new_key, "a")["password"] == "pass-a"
    assert repository.get_entry(conn, new_key, "b")["password"] == "pass-b"
    row = conn.execute("SELECT check_token FROM meta WHERE id = 1").fetchone()
    assert crypto.verify_key(new_key, row["check_token"])


def test_change_master_rolls_back_on_error(conn, key, mocker):
    for name in ("a", "b", "c"):
        repository.add_entry(conn, key, name, "u", f"pass-{name}")
    new_key = crypto.derive_key("new", NEW_SALT)

    # перше шифрування успішне а  друге падає *__* 
    mocker.patch(
        "vault.repository.encrypt",
        side_effect=[b"first-ok", RuntimeError("boom")],
    )
    with pytest.raises(RuntimeError):
        repository.change_master(conn, key, new_key, NEW_SALT)

    # після відкату 
    assert repository.get_entry(conn, key, "a")["password"] == "pass-a"
    assert repository.get_entry(conn, key, "c")["password"] == "pass-c"
    