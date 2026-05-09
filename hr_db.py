import sqlite3
from typing import List, Tuple


class HRDatabase:
    def __init__(self, db_path: str = "hr.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT,
                department TEXT,
                salary REAL
            )
            """
        )
        self.conn.commit()

    def add_employee(self, name: str, position: str, department: str, salary: float) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO employees (name, position, department, salary) VALUES (?, ?, ?, ?)",
            (name, position, department, salary),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_all(self) -> List[Tuple]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, position, department, salary FROM employees ORDER BY id DESC")
        return cur.fetchall()

    def update_employee(self, emp_id: int, name: str, position: str, department: str, salary: float) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE employees SET name=?, position=?, department=?, salary=? WHERE id=?",
            (name, position, department, salary, emp_id),
        )
        self.conn.commit()

    def delete_employee(self, emp_id: int) -> None:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        self.conn.commit()

    def search(self, term: str) -> List[Tuple]:
        cur = self.conn.cursor()
        like = f"%{term}%"
        cur.execute(
            "SELECT id, name, position, department, salary FROM employees WHERE name LIKE ? OR position LIKE ? OR department LIKE ? ORDER BY id DESC",
            (like, like, like),
        )
        return cur.fetchall()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = HRDatabase()
    print('DB initialized at hr.db')
    db.close()
