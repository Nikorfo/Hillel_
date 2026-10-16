from shop import profile, username


def test_string():
    assert username("Ann", "Lee") == "ann_lee"

def test_dict():
    assert profile("Ann", "Lee", "ann@shop.ua") == {
        "username": "ann.lee",
        "email": "ann@shop.ua",
        "roles": ["customer", "admin"]
    }

def test_list():
    assert [1, 2, 3, 4] == [1, 2, 4, 3]

def test_in():
    assert "admin" in [ "a", "b" ]

def test_call():
    assert username("Ann", "Lee").startswith("lee")
    
