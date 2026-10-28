import os
import sqlite3

import click

from vault import crypto, db, generator, repository, strength, transfer


def get_conn():
    path = os.environ.get("VAULT_DB", str(db.DEFAULT_DB))
    conn = db.get_connection(path)
    db.init_schema(conn)
    return conn


def unlock(conn):
    """Просить майстер-пароль, повертає ключ або завершує команду з помилкою"""
    row = conn.execute("SELECT salt, check_token FROM meta WHERE id = 1").fetchone()
    if row is None:
        raise click.ClickException("Сховище не створено. Спочатку: python -m vault init")
    master = click.prompt("Майстер-пароль", hide_input=True)
    key = crypto.derive_key(master, row["salt"])
    if not crypto.verify_key(key, row["check_token"]):
        raise click.ClickException("Невірний майстер-пароль")
    return key


@click.group()
def cli():
    """Консольний менеджер паролів"""


@cli.command()
def init():
    """Створити сховище"""
    conn = get_conn()
    if conn.execute("SELECT 1 FROM meta").fetchone():
        raise click.ClickException("Сховище вже існує")
    master = click.prompt("Новий майстер-пароль", hide_input=True, confirmation_prompt=True)
    level, tips = strength.evaluate(master)
    if level == "слабкий":
        click.echo("Увага: майстер-пароль слабкий " + "; ".join(tips))
    salt = crypto.new_salt()
    key = crypto.derive_key(master, salt)
    with conn:
        conn.execute(
            "INSERT INTO meta (id, salt, check_token) VALUES (1, ?, ?)",
            (salt, crypto.make_check(key)),
        )
    click.echo("Сховище створено")


@cli.command()
@click.argument("service")
@click.option("--login", required=True)
@click.option("--generate", "gen", is_flag=True, help="Згенерувати пароль автоматично")
@click.option("--length", default=16, show_default=True)
@click.option("--tag", "tags", multiple=True)
@click.option("--url")
def add(service, login, gen, length, tags, url):
    """Додати запис"""
    conn = get_conn()
    key = unlock(conn)
    if gen:
        password = generator.generate_password(length)
        click.echo(f"Згенеровано пароль: {password}")
    else:
        password = click.prompt("Пароль для сервісу", hide_input=True, confirmation_prompt=True)
    try:
        repository.add_entry(conn, key, service, login, password, url=url, tags=tags)
    except sqlite3.IntegrityError:
        raise click.ClickException(f"Запис '{service}' вже існує")
    click.echo(f"Запис '{service}' додано")


@cli.command()
@click.argument("service")
def get(service):
    """Показати запис"""
    conn = get_conn()
    key = unlock(conn)
    entry = repository.get_entry(conn, key, service)
    if entry is None:
        raise click.ClickException("Запис не знайдено")
    click.echo(f"Логін:  {entry['login']}")
    click.echo(f"Пароль: {entry['password']}")
    if entry["url"]:
        click.echo(f"URL:    {entry['url']}")


@cli.command("list")
@click.option("--tag")
@click.option("--search")
@click.option("--page", default=1, show_default=True)
@click.option("--size", default=10, show_default=True)
def list_cmd(tag, search, page, size):
    """Список записів (паролі не показуються)."""
    conn = get_conn()
    rows, total = repository.list_entries(conn, tag, search, page, size)
    pages = max(1, -(-total // size))
    for r in rows:
        click.echo(f"{r['service']:<20} {r['login']}")
    click.echo(f"\nСторінка {page}/{pages}, усього: {total}")


@cli.command()
@click.argument("service")
@click.option("--generate", "gen", is_flag=True)
@click.option("--length", default=16, show_default=True)
def update(service, gen, length):
    """Змінити пароль запису"""
    conn = get_conn()
    key = unlock(conn)
    if gen:
        password = generator.generate_password(length)
        click.echo(f"Згенеровано пароль: {password}")
    else:
        password = click.prompt("Новий пароль", hide_input=True, confirmation_prompt=True)
    if not repository.update_password(conn, key, service, password):
        raise click.ClickException("Запис не знайдено")
    click.echo(f"Пароль для '{service}' оновлено")


@cli.command()
@click.argument("service")
@click.option("--yes", is_flag=True, help="Не питати підтвердження")
def delete(service, yes):
    """Видалити запис"""
    conn = get_conn()
    unlock(conn)
    if not yes:
        click.confirm(f"Видалити '{service}'?", abort=True)
    if not repository.delete_entry(conn, service):
        raise click.ClickException("Запис не знайдено")
    click.echo(f"Запис '{service}' видалено")


@cli.command()
@click.option("--length", default=16, show_default=True)
@click.option("--no-symbols", is_flag=True)
@click.option("--no-digits", is_flag=True)
def generate(length, no_symbols, no_digits):
    """Згенерувати пароль"""
    try:
        pwd = generator.generate_password(length, digits=not no_digits, symbols=not no_symbols)
    except ValueError as exc:
        raise click.ClickException(str(exc))
    click.echo(pwd)


@cli.command()
@click.argument("password")
def check(password):
    """Оцінити надійність пароля"""
    level, tips = strength.evaluate(password)
    click.echo(f"Рівень: {level}")
    for tip in tips:
        click.echo(f" - {tip}")


@cli.command("change-master")
def change_master():
    """Змінити майстер-пароль"""
    conn = get_conn()
    old_key = unlock(conn)
    new_master = click.prompt("Новий майстер-пароль", hide_input=True, confirmation_prompt=True)
    new_salt = crypto.new_salt()
    new_key = crypto.derive_key(new_master, new_salt)
    repository.change_master(conn, old_key, new_key, new_salt)
    click.echo("Майстер-пароль змінено, усі записи перешифровано")


@cli.command("export")
@click.option("--out", required=True, type=click.Path())
def export_cmd(out):
    """Експортувати зашифрований бекап у JSON"""
    conn = get_conn()
    unlock(conn)
    count = transfer.export_vault(conn, out)
    click.echo(f"Експортовано записів: {count}")


@cli.command("import")
@click.argument("path", type=click.Path(exists=True))
def import_cmd(path):
    """Імпортувати бекап у порожнє сховище"""
    conn = get_conn()
    try:
        count = transfer.import_vault(conn, path)
    except ValueError as exc:
        raise click.ClickException(str(exc))
    click.echo(f"Імпортовано записів: {count}")
    