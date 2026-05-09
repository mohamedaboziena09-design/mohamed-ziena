from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import pytest

from gui import HRApp


def test_add_update_delete(qtbot, tmp_path, monkeypatch):
    db_path = str(tmp_path / "gui_test.db")
    win = HRApp(db_path=db_path)
    qtbot.addWidget(win)
    win.show()

    # Add an employee
    qtbot.keyClicks(win.name_in, "Tester")
    qtbot.keyClicks(win.pos_in, "Dev")
    qtbot.keyClicks(win.dep_in, "QA")
    win.sal_in.setValue(55000)
    qtbot.mouseClick(win.add_btn, Qt.LeftButton)

    qtbot.waitUntil(lambda: win.table.rowCount() == 1, timeout=2000)
    assert win.table.rowCount() == 1
    assert win.table.item(0, 1).text() == "Tester"

    # Select and update the employee
    win.table.selectRow(0)
    qtbot.keyClicks(win.name_in, "_Updated")
    # simulate clicking update
    qtbot.mouseClick(win.update_btn, Qt.LeftButton)
    qtbot.wait(200)
    assert "Updated" in win.table.item(0, 1).text()

    # Monkeypatch QMessageBox.question to auto-confirm deletes
    monkeypatch.setattr(QMessageBox, 'question', lambda *args, **kwargs: QMessageBox.Yes)

    # Delete
    win.table.selectRow(0)
    qtbot.mouseClick(win.delete_btn, Qt.LeftButton)
    qtbot.waitUntil(lambda: win.table.rowCount() == 0, timeout=2000)
    assert win.table.rowCount() == 0


def test_search(qtbot, tmp_path):
    db_path = str(tmp_path / "gui_search.db")
    win = HRApp(db_path=db_path)
    qtbot.addWidget(win)
    win.show()

    qtbot.keyClicks(win.name_in, "Alice")
    qtbot.keyClicks(win.pos_in, "Analyst")
    qtbot.keyClicks(win.dep_in, "Finance")
    win.sal_in.setValue(70000)
    qtbot.mouseClick(win.add_btn, Qt.LeftButton)

    qtbot.waitUntil(lambda: win.table.rowCount() == 1, timeout=2000)
    qtbot.keyClicks(win.search_in, "Alice")
    qtbot.mouseClick(win.search_btn, Qt.LeftButton)
    qtbot.wait(200)
    assert win.table.rowCount() >= 1
