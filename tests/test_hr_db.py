import pytest
from hr_db import HRDatabase


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test.db")


@pytest.fixture
def db(db_path):
    d = HRDatabase(db_path)
    yield d
    d.close()


def test_add_and_get_all(db):
    id1 = db.add_employee("Alice", "Engineer", "R&D", 70000)
    id2 = db.add_employee("Bob", "Manager", "Sales", 80000)
    rows = db.get_all()
    assert len(rows) == 2
    assert rows[0][0] == id2
    assert rows[1][0] == id1


def test_update(db):
    eid = db.add_employee("Carol", "Dev", "IT", 60000)
    db.update_employee(eid, "Carolyn", "Senior Dev", "IT", 75000)
    rows = db.search("Carolyn")
    assert len(rows) == 1
    assert rows[0][1] == "Carolyn"
    assert float(rows[0][4]) == 75000


def test_delete(db):
    eid = db.add_employee("Dave", "Support", "Help", 40000)
    db.delete_employee(eid)
    rows = db.search("Dave")
    assert rows == []


def test_search(db):
    db.add_employee("Eve", "Analyst", "Finance", 65000)
    db.add_employee("Evan", "Analyst", "Finance", 66000)
    res = db.search("Eve")
    names = [r[1] for r in res]
    assert "Eve" in names
