import sqlite3

connection = sqlite3.connect('example.db')

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    departament TEXT NOT NULL,
    salary REAL
)
''')

connection.commit()

cursor.execute('''
INSERT INTO employees (name, position, departament, salary)
VALUES (?,?,?,?)
''', ('Dion Konjuhi', 'Software Engineer', 'IT', 7000.00))


connection.commit()

cursor.execute('SELECT * FROM employees')

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.execute('''
UPDATE employees
SET salary = ?
WHERE name = ?
''', (7500.00, 'Dion Konjuhi'))

connection.commit()

cursor.execute('''
DELETE FROM employees
WHERE name = ?
''',('Dion Konjuhi',))

connection.commit()

cursor.close()
connection.close()