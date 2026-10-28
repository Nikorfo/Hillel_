import base64
import json


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode()


def export_vault(conn, path) -> int:
    """Експортує зашифровані дані у JSON. Повертає кількість записів"""
    meta = conn.execute("SELECT salt, check_token FROM meta WHERE id = 1").fetchone()
    entries = conn.execute("SELECT * FROM entries").fetchall()
    data = {
        "salt": _b64(meta["salt"]),
        "check_token": _b64(meta["check_token"]),
        "entries": [
            {**dict(e), "password_encrypted": _b64(e["password_encrypted"])}
            for e in entries
        ],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return len(entries)


def import_vault(conn, path) -> int:
    """Імпортує у порожнє сховище. Усе в одній транзакції"""
    if conn.execute("SELECT 1 FROM meta").fetchone():
        raise ValueError("Імпорт можливий лише в порожнє сховище")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    with conn:
        conn.execute(
            "INSERT INTO meta (id, salt, check_token) VALUES (1, ?, ?)",
            (base64.b64decode(data["salt"]), base64.b64decode(data["check_token"])),
        )
        for e in data["entries"]:
            conn.execute(
                "INSERT INTO entries (service, login, password_encrypted, url, tags, "
                "notes, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    e["service"], e["login"], base64.b64decode(e["password_encrypted"]),
                    e["url"], e["tags"], e["notes"], e["created_at"], e["updated_at"],
                ),
            )
    return len(data["entries"])
