import psycopg2
from prettytable import PrettyTable

# Підключення до бази даних
connection = psycopg2.connect(
    host="localhost",
    port="5433",
    database="WorkShop",
    user="postgres",
    password="postgres"
)
cursor = connection.cursor()

# Запити до бази даних
# 1. Відобразити інформацію про всі гарантійні ремонти
cursor.execute('''
SELECT Clients.CompanyName, Repairs.RepairDate, Repairs.RepairType, Cars.CarModel
FROM Repairs
JOIN Cars ON Repairs.CarID = Cars.CarID
JOIN Clients ON Cars.ClientID = Clients.ClientID
WHERE Repairs.RepairType = 'гарантійний'
ORDER BY Clients.CompanyName;
''')
warranty_repairs = cursor.fetchall()

cursor.execute('''
SELECT Cars.CarModel, 
       Repairs.HoursWorked * Repairs.HourlyRate AS TotalCost,
       (Repairs.HoursWorked * Repairs.HourlyRate) * (1 - Repairs.Discount / 100) AS DiscountedCost
FROM Repairs
JOIN Cars ON Repairs.CarID = Cars.CarID;
''')
repair_costs = cursor.fetchall()

# 3. Відобразити інформацію по ремонту для всіх авто заданої марки
car_model = 'fiesta'
cursor.execute('''
SELECT Repairs.RepairID, Repairs.RepairDate, Repairs.RepairType, Repairs.HourlyRate, Repairs.HoursWorked, Cars.CarModel
FROM Repairs
JOIN Cars ON Repairs.CarID = Cars.CarID
WHERE Cars.CarModel = %s;
''', (car_model,))
specific_model_repairs = cursor.fetchall()

# 4. Порахувати загальну суму, яку сплатив кожен клієнт
cursor.execute('''
SELECT Clients.CompanyName, 
       SUM((Repairs.HoursWorked * Repairs.HourlyRate) * (1 - Repairs.Discount / 100)) AS TotalPaid
FROM Repairs
JOIN Cars ON Repairs.CarID = Cars.CarID
JOIN Clients ON Cars.ClientID = Clients.ClientID
GROUP BY Clients.CompanyName;
''')
total_paid = cursor.fetchall()

# 5. Порахувати кількість кожного типу ремонтів для кожного клієнта
cursor.execute('''
SELECT Clients.CompanyName, 
       Repairs.RepairType,
       COUNT(Repairs.RepairID) AS RepairCount
FROM Repairs
JOIN Cars ON Repairs.CarID = Cars.CarID
JOIN Clients ON Cars.ClientID = Clients.ClientID
GROUP BY Clients.CompanyName, Repairs.RepairType;
''')
repair_counts_by_type = cursor.fetchall()

# 6. Порахувати кількість ремонтів для кожної марки автомобіля
cursor.execute('''
SELECT Cars.CarModel, 
       COUNT(Repairs.RepairID) AS RepairCount
FROM Repairs
JOIN Cars ON Repairs.CarID = Cars.CarID
GROUP BY Cars.CarModel;
''')
repair_counts_by_model = cursor.fetchall()

# Виведення результатів у консоль у вигляді таблиць
def print_table(headers, rows):
    table = PrettyTable(headers)
    for row in rows:
        table.add_row(row)
    print(table)

print("Інформація про всі гарантійні ремонти:")
print_table(["CompanyName", "RepairDate", "RepairType", "CarModel"], warranty_repairs)

print("\nВартість ремонту та вартість з урахуванням знижки для кожного автомобіля:")
print_table(["CarModel", "TotalCost", "DiscountedCost"], repair_costs)

print("\nІнформація по ремонту для всіх авто заданої марки:")
print_table(["RepairID", "RepairDate", "RepairType", "HourlyRate", "HoursWorked", "CarModel"], specific_model_repairs)

print("\nЗагальна сума, яку сплатив кожен клієнт:")
print_table(["CompanyName", "TotalPaid"], total_paid)

print("\nКількість кожного типу ремонтів для кожного клієнта:")
print_table(["CompanyName", "RepairType", "RepairCount"], repair_counts_by_type)

print("\nКількість ремонтів для кожної марки автомобіля:")
print_table(["CarModel", "RepairCount"], repair_counts_by_model)

# Закриття курсору та з'єднання
cursor.close()
connection.close()
