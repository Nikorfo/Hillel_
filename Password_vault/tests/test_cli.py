from click.testing import CliRunner

from vault.cli import cli

MASTER = "Master#12345"


def run(args, inp, db_path):
    return CliRunner().invoke(cli, args, input=inp, env={"VAULT_DB": str(db_path)})


def setup_vault(db_file):
    return run(["init"], f"{MASTER}\n{MASTER}\n", db_file)


def add_entry(db_file, service="gh", password="secret1"):
    return run(
        ["add", service, "--login", "nik"],
        f"{MASTER}\n{password}\n{password}\n",
        db_file,
    )


def test_full_flow(tmp_path):
    db_file = tmp_path / "t.db"
    assert "Сховище створено" in setup_vault(db_file).output
    assert "додано" in add_entry(db_file).output
    assert "secret1" in run(["get", "gh"], f"{MASTER}\n", db_file).output


def test_init_twice_fails(tmp_path):
    db_file = tmp_path / "t.db"
    setup_vault(db_file)
    r = setup_vault(db_file)
    assert r.exit_code != 0
    assert "вже існує" in r.output


def test_wrong_master(tmp_path):
    db_file = tmp_path / "t.db"
    setup_vault(db_file)
    r = run(["get", "x"], "wrong\n", db_file)
    assert r.exit_code != 0
    assert "Невірний" in r.output


def test_command_without_init(tmp_path):
    r = run(["get", "x"], "any\n", tmp_path / "t.db")
    assert r.exit_code != 0
    assert "не створено" in r.output


def test_add_generated_password(tmp_path):
    db_file = tmp_path / "t.db"
    setup_vault(db_file)
    r = run(["add", "gh", "--login", "nik", "--generate"], f"{MASTER}\n", db_file)
    assert "Згенеровано пароль" in r.output


def test_duplicate_add(tmp_path): 
    db_file = tmp_path / "t.db"
    setup_vault(db_file)
    add_entry(db_file)
    r = add_entry(db_file)
    assert r.exit_code != 0
    assert "вже існує" in r.output


def test_get_missing_entry(tmp_path):
    db_file = tmp_path / "t.db"
    setup_vault(db_file)
    r = run(["get", "nope"], f"{MASTER}\n", db_file)
    assert r.exit_code != 0
    assert "не знайдено" in r.output


def test_list_pagination(tmp_path):
    db_file = tmp_path / "t.db"
    setup_vault(db_file)
    for i in range(3):
        run(["add", f"s{i}", "--login", "u", "--generate"], f"{MASTER}\n", db_file)
    r = run(["list", "--size", "2", "--page", "2"], "", db_file)
    assert "Сторінка 2/2, усього: 3" in r.output


def test_update_and_delete(tmp_path):
    db_file = tmp_path / "t.db"
    setup_vault(db_file)
    add_entry(db_file, password="old")

    r = run(["update", "gh"], f"{MASTER}\nnew\nnew\n", db_file)
    assert "оновлено" in r.output
    assert "new" in run(["get", "gh"], f"{MASTER}\n", db_file).output

    r = run(["delete", "gh", "--yes"], f"{MASTER}\n", db_file)
    assert "видалено" in r.output
    assert run(["get", "gh"], f"{MASTER}\n", db_file).exit_code != 0


def test_generate_and_check():
    r = CliRunner().invoke(cli, ["generate", "--length", "20"])
    assert len(r.output.strip()) == 20
    r = CliRunner().invoke(cli, ["check", "abc"])
    assert "слабкий" in r.output


def test_generate_too_short():
    r = CliRunner().invoke(cli, ["generate", "--length", "2"])
    assert r.exit_code != 0


def test_change_master(tmp_path):
    db_file = tmp_path / "t.db"
    setup_vault(db_file)
    add_entry(db_file)

    new = "NewMaster#999"
    r = run(["change-master"], f"{MASTER}\n{new}\n{new}\n", db_file)
    assert "змінено" in r.output

    assert run(["get", "gh"], f"{MASTER}\n", db_file).exit_code != 0
    assert "secret1" in run(["get", "gh"], f"{new}\n", db_file).output


def test_export_import(tmp_path):
    db1, db2, out = tmp_path / "a.db", tmp_path / "b.db", tmp_path / "bk.json"
    setup_vault(db1)
    add_entry(db1)

    r = run(["export", "--out", str(out)], f"{MASTER}\n", db1)
    assert "Експортовано записів: 1" in r.output

    r = run(["import", str(out)], "", db2)
    assert "Імпортовано записів: 1" in r.output
    assert "secret1" in run(["get", "gh"], f"{MASTER}\n", db2).output
    