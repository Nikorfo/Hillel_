from vault.crypto import decrypt, encrypt, make_check


def normalize_tags(tags) -> str:
    cleaned = sorted({t.strip().lower() for t in tags if t.strip()})
    return "," + ",".join(cleaned) + "," if cleaned else ""


def add_entry(conn, key, service, login, password, url=None, tags=(), notes=None):
    with conn:
        conn.execute(
            "INSERT INTO entries (service, login, password_encrypted, url, tags, notes) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (service, login, encrypt(key, password), url, normalize_tags(tags), notes),
        )


def get_entry(conn, key, service):
    row = conn.execute("SELECT * FROM entries WHERE service = ?", (service,)).fetchone()
    if row is None:
        return None
    data = dict(row)
    data["password"] = decrypt(key, data.pop("password_encrypted"))
    return data


def list_entries(conn, tag=None, search=None, page=1, size=10):
    where, params = [], []
    if tag:
        where.append("tags LIKE ?")
        params.append(f"%,{tag.lower()},%")
    if search:
        where.append("service LIKE ?")
        params.append(f"%{search}%")
    clause = ("WHERE " + " AND ".join(where)) if where else ""

    total = conn.execute(f"SELECT COUNT(*) FROM entries {clause}", params).fetchone()[0]
    rows = conn.execute(
        f"SELECT id, service, login, tags FROM entries {clause} "
        "ORDER BY service LIMIT ? OFFSET ?",
        [*params, size, (page - 1) * size],
    ).fetchall()
    return rows, total


def update_password(conn, key, service, new_password) -> bool:
    with conn:
        cur = conn.execute(
            "UPDATE entries SET password_encrypted = ?, updated_at = CURRENT_TIMESTAMP "
            "WHERE service = ?",
            (encrypt(key, new_password), service),
        )
    return cur.rowcount > 0


def delete_entry(conn, service) -> bool:
    with conn:
        cur = conn.execute("DELETE FROM entries WHERE service = ?", (service,))
    return cur.rowcount > 0


def change_master(conn, old_key, new_key, new_salt) -> None:
    """Перешифровує всі записи новим ключем. Усе або нічого"""
    with conn:
        rows = conn.execute("SELECT id, password_encrypted FROM entries").fetchall()
        for row in rows:
            plain = decrypt(old_key, row["password_encrypted"])
            conn.execute(
                "UPDATE entries SET password_encrypted = ? WHERE id = ?",
                (encrypt(new_key, plain), row["id"]),
            )
        conn.execute(
            "UPDATE meta SET salt = ?, check_token = ? WHERE id = 1",
            (new_salt, make_check(new_key)),
        )
 