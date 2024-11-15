import psycopg2
from psycopg2 import sql

# Підключення до бази даних
connection = psycopg2.connect(
    host="localhost",
    port="5433",
    database="WorkShop",
    user="postgres",
    password="postgres"
)
cursor = connection.cursor()

# Створення таблиць
cursor.execute('''
CREATE TABLE IF NOT EXISTS Clients (
    ClientID SERIAL PRIMARY KEY,
    CompanyName VARCHAR(100),
    BankAccount VARCHAR(50),
    Phone VARCHAR(20),
    ContactPerson VARCHAR(100),
    Address TEXT
);

CREATE TABLE IF NOT EXISTS Cars (
    CarID SERIAL PRIMARY KEY,
    CarModel VARCHAR(50),
    CarPrice DECIMAL,
    ClientID INTEGER REFERENCES Clients(ClientID)
);

CREATE TABLE IF NOT EXISTS Repairs (
    RepairID SERIAL PRIMARY KEY,
    RepairDate DATE,
    CarID INTEGER REFERENCES Cars(CarID),
    RepairType VARCHAR(50),
    HourlyRate DECIMAL,
    Discount DECIMAL CHECK (Discount BETWEEN 0 AND 10),
    HoursWorked INTEGER
);
''')

# Заповнення таблиць даними
clients = [
    ("Company A", "123456789", "123-456-7890", "John Doe", "123 Street, City"),
    ("Company B", "987654321", "098-765-4321", "Jane Smith", "456 Avenue, City"),
    ("Company C", "111222333", "111-222-3333", "Alice Johnson", "789 Boulevard, City"),
    ("Company D", "444555666", "444-555-6666", "Bob Brown", "101 Road, City"),
    ("Company E", "777888999", "777-888-9999", "Eve White", "202 Lane, City"),
    ("Company F", "000111222", "000-111-2222", "Charlie Green", "303 Path, City")
]

cars = [
    ("fiesta", 15000, 1),
    ("focus", 20000, 2),
    ("fusion", 25000, 3),
    ("mondeo", 30000, 4),
    ("fiesta", 15000, 5),
    ("focus", 20000, 6)
]

repairs = [
    ("2024-01-01", 1, "гарантійний", 50, 5, 10),
    ("2024-02-01", 2, "плановий", 60, 10, 15),
    ("2024-03-01", 3, "капітальний", 70, 0, 20),
    ("2024-04-01", 4, "гарантійний", 50, 5, 10),
    ("2024-05-01", 5, "плановий", 60, 10, 15),
    ("2024-06-01", 6, "капітальний", 70, 0, 20),
    ("2024-07-01", 1, "гарантійний", 50, 5, 10),
    ("2024-08-01", 2, "плановий", 60, 10, 15),
    ("2024-09-01", 3, "капітальний", 70, 0, 20),
    ("2024-10-01", 4, "гарантійний", 50, 5, 10),
    ("2024-11-01", 5, "плановий", 60, 10, 15),
    ("2024-12-01", 6, "капітальний", 70, 0, 20),
    ("2024-01-01", 1, "гарантійний", 50, 5, 10),
    ("2024-02-01", 2, "плановий", 60, 10, 15),
    ("2024-03-01", 3, "капітальний", 70, 0, 20)
]

cursor.executemany('INSERT INTO Clients (CompanyName, BankAccount, Phone, ContactPerson, Address) VALUES (%s, %s, %s, %s, %s)', clients)
cursor.executemany('INSERT INTO Cars (CarModel, CarPrice, ClientID) VALUES (%s, %s, %s)', cars)
cursor.executemany('INSERT INTO Repairs (RepairDate, CarID, RepairType, HourlyRate, Discount, HoursWorked) VALUES (%s, %s, %s, %s, %s, %s)', repairs)

# Фіксація змін
connection.commit()

# Закриття курсору та з'єднання
cursor.close()
connection.close()

print("Таблиці створені та заповнені успішно.")
