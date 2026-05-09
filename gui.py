from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QDoubleSpinBox,
)
import csv
from hr_db import HRDatabase


class HRApp(QMainWindow):
    def __init__(self, db_path: str = "hr.db"):
        super().__init__()
        self.setWindowTitle("HR System")
        self.resize(800, 500)
        self.db = HRDatabase(db_path)
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        v = QVBoxLayout(central)

        # Table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["id", "name", "position", "department", "salary"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemSelectionChanged.connect(self._on_select)
        v.addWidget(self.table)

        # Form
        form = QHBoxLayout()
        v.addLayout(form)

        self.name_in = QLineEdit()
        self.pos_in = QLineEdit()
        self.dep_in = QLineEdit()
        self.sal_in = QDoubleSpinBox()
        self.sal_in.setMaximum(1e9)
        self.sal_in.setPrefix("$")

        form.addWidget(QLabel("Name"))
        form.addWidget(self.name_in)
        form.addWidget(QLabel("Position"))
        form.addWidget(self.pos_in)
        form.addWidget(QLabel("Department"))
        form.addWidget(self.dep_in)
        form.addWidget(QLabel("Salary"))
        form.addWidget(self.sal_in)

        # Buttons + Search
        h = QHBoxLayout()
        v.addLayout(h)

        self.add_btn = QPushButton("Add")
        self.update_btn = QPushButton("Update")
        self.delete_btn = QPushButton("Delete")
        self.refresh_btn = QPushButton("Refresh")
        self.export_btn = QPushButton("Export CSV")

        h.addWidget(self.add_btn)
        h.addWidget(self.update_btn)
        h.addWidget(self.delete_btn)
        h.addWidget(self.refresh_btn)
        h.addStretch()
        h.addWidget(self.export_btn)

        self.search_in = QLineEdit()
        self.search_btn = QPushButton("Search")
        h2 = QHBoxLayout()
        h2.addWidget(QLabel("Search:"))
        h2.addWidget(self.search_in)
        h2.addWidget(self.search_btn)
        v.addLayout(h2)

        # Connect
        self.add_btn.clicked.connect(self.add)
        self.update_btn.clicked.connect(self.update)
        self.delete_btn.clicked.connect(self.delete)
        self.refresh_btn.clicked.connect(self.load_data)
        self.export_btn.clicked.connect(self.export_csv)
        self.search_btn.clicked.connect(self.search)

    def load_data(self):
        rows = self.db.get_all()
        self.table.setRowCount(0)
        for r in rows:
            self._insert_row(r)

    def _insert_row(self, row):
        row_pos = self.table.rowCount()
        self.table.insertRow(row_pos)
        for i, val in enumerate(row):
            item = QTableWidgetItem(str(val))
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.table.setItem(row_pos, i, item)

    def _on_select(self):
        sel = self.table.selectedItems()
        if not sel:
            return
        # items by column
        values = [it.text() for it in sel]
        # ensure we have 5 columns; selection returns items row-wise
        if len(values) >= 5:
            _, name, pos, dep, sal = values[:5]
            self.name_in.setText(name)
            self.pos_in.setText(pos)
            self.dep_in.setText(dep)
            try:
                self.sal_in.setValue(float(sal.strip().lstrip("$")))
            except Exception:
                self.sal_in.setValue(0)

    def _get_selected_id(self):
        sel = self.table.selectedItems()
        if not sel:
            return None
        try:
            return int(sel[0].text())
        except Exception:
            return None

    def add(self):
        name = self.name_in.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing", "Name is required")
            return
        salary = float(self.sal_in.value())
        self.db.add_employee(name, self.pos_in.text().strip(), self.dep_in.text().strip(), salary)
        self.load_data()
        self._clear_form()

    def update(self):
        emp_id = self._get_selected_id()
        if not emp_id:
            QMessageBox.information(self, "Select", "Select an employee to update")
            return
        salary = float(self.sal_in.value())
        self.db.update_employee(emp_id, self.name_in.text().strip(), self.pos_in.text().strip(), self.dep_in.text().strip(), salary)
        self.load_data()

    def delete(self):
        emp_id = self._get_selected_id()
        if not emp_id:
            QMessageBox.information(self, "Select", "Select an employee to delete")
            return
        if QMessageBox.question(self, "Confirm", "Delete selected employee?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.delete_employee(emp_id)
            self.load_data()

    def search(self):
        term = self.search_in.text().strip()
        if not term:
            rows = self.db.get_all()
        else:
            rows = self.db.search(term)
        self.table.setRowCount(0)
        for r in rows:
            self._insert_row(r)

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", filter="CSV Files (*.csv)")
        if not path:
            return
        rows = self.db.get_all()
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "name", "position", "department", "salary"])
            w.writerows(rows)
        QMessageBox.information(self, "Exported", f"Exported {len(rows)} rows to {path}")

    def _clear_form(self):
        self.name_in.clear()
        self.pos_in.clear()
        self.dep_in.clear()
        self.sal_in.setValue(0)

    def closeEvent(self, event):
        self.db.close()
        event.accept()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    win = HRApp()
    win.show()
    sys.exit(app.exec_())
