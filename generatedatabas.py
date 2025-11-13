import csv

products = [
    {
        "id": 0,
        "name": "BMW E30 325i",
        "hp": 170,
        "fuel": "Bensin",
        "year": 1989,
        "price": 85000,
        "quantity": 3
    },
    {
        "id": 1,
        "name": "Saab 900 Turbo",
        "hp": 175,
        "fuel": "Bensin",
        "year": 1991,
        "price": 49000,
        "quantity": 2
    },
    {
        "id": 2,
        "name": "Audi 80 B4",
        "hp": 115,
        "fuel": "Bensin",
        "year": 1994,
        "price": 43000,
        "quantity": 5
    },
    {
        "id": 3,
        "name": "Subaru Impreza GT Turbo",
        "hp": 211,
        "fuel": "Bensin",
        "year": 1998,
        "price": 99000,
        "quantity": 1
    },
    {
        "id": 4,
        "name": "BMW E34 540i",
        "hp": 286,
        "fuel": "Bensin",
        "year": 1995,
        "price": 69000,
        "quantity": 1
    },
    {
        "id": 5,
        "name": "Saab 99 EMS",
        "hp": 145,
        "fuel": "Bensin",
        "year": 1977,
        "price": 32000,
        "quantity": 1
    },
    {
        "id": 6,
        "name": "Audi 100 C3",
        "hp": 136,
        "fuel": "Bensin",
        "year": 1987,
        "price": 29000,
        "quantity": 2
    },
    {
        "id": 7,
        "name": "Subaru Legacy RS",
        "hp": 220,
        "fuel": "Bensin",
        "year": 1991,
        "price": 61000,
        "quantity": 2
    },
    {
        "id": 8,
        "name": "BMW E21 323i",
        "hp": 143,
        "fuel": "Bensin",
        "year": 1982,
        "price": 49000,
        "quantity": 1
    },
    {
        "id": 9,
        "name": "Saab 9000 Aero",
        "hp": 225,
        "fuel": "Bensin",
        "year": 1994,
        "price": 68000,
        "quantity": 1
    },
    {
        "id": 10,
        "name": "Audi Coupe GT",
        "hp": 115,
        "fuel": "Bensin",
        "year": 1986,
        "price": 38000,
        "quantity": 1
    },
    {
        "id": 11,
        "name": "Subaru SVX",
        "hp": 230,
        "fuel": "Bensin",
        "year": 1993,
        "price": 54000,
        "quantity": 1
    }
]

csv_file_path = "db_bilar.csv"
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["id", "name", "hp", "fuel", "year", "price", "quantity"])
    writer.writeheader()
    writer.writerows(products)

print(f"Data successfully saved to {csv_file_path}")