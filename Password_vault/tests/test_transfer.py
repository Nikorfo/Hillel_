import sqlite3

import pytest

from vault import crypto, db, repository, transfer


def make_conn():
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    db.init_schema(c)
    return c


@pytest.fixture 
def filled_conn(conn, key):
    conn.execute(
        "INSERT INTO meta (id, salt, check_token) VALUES (1, ?, ?)",
        (b"0123456789abcdef", crypto.make_check(key)),
    )
    repository.add_entry(conn, key, "github", "nik", "pass-gh", tags=["work"])
    repository.add_entry(conn, key, "gmail", "nik@x.com", "pass-gm")
    return conn


def test_export_import_roundtrip(filled_conn, key, tmp_path):
    out = tmp_path / "backup.json"
    assert transfer.export_vault(filled_conn, out) == 2

    new_conn = make_conn()
    assert transfer.import_vault(new_conn, out) == 2

    assert repository.get_entry(new_conn, key, "github")["password"] == "pass-gh"
    assert repository.get_entry(new_conn, key, "gmail")["password"] == "pass-gm"


def test_import_into_nonempty_vault_raises(filled_conn, tmp_path):
    out = tmp_path / "backup.json"
    transfer.export_vault(filled_conn, out)
    with pytest.raises(ValueError):
        transfer.import_vault(filled_conn, out)


def test_exported_file_has_no_plaintext(filled_conn, tmp_path):
    out = tmp_path / "backup.json"
    transfer.export_vault(filled_conn, out)
    text = out.read_text(encoding="utf-8")
    assert "pass-gh" not in text
    assert "pass-gm" not in text