# test---
# prepare_system()
# test()
# return_back_system()

# /tests --- conftest.py
#   /users --- test_a.py test_b.py
#   /books --- test_a.py test_b.py


def test_simple_fixture( test_fixture ):
    assert test_fixture == 10

def test_ann(ann):
    assert ann["username"] == "ann.lee"

def test_two_users(make_user):
    bob = make_user("Bob")
    ann = make_user()

    assert ann != bob


def test_insert( db ):
    db.execute( "INSERT INTO users VALUES ('ann')" )
    assert db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 1

