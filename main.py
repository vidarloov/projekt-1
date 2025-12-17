import csv
import curses
import locale
import os


CSV_FILE = "db_bilar.csv"
locale.setlocale(locale.LC_ALL, '')


# Ladda alla bilar från databasen
def load_cars():
    cars = []
        
    with open(CSV_FILE) as f:
        for r in csv.DictReader(f):
                car = {
                        "id": int(r["id"]), 
                        "name": r["name"], 
                        "hp": int(r["hp"]), 
                        "fuel": r["fuel"], 
                        "year": int(r["year"]), 
                        "price": float(r["price"])
                    }
                cars.append(car)
    
    return cars


cars = load_cars()

            
# Hindrar texten från att bli för lång
def truncate(text, max_len):
    if len(text) > max_len:
        return text[:max_len-3] + "..." 
    return text


# Spara till CSV filen
def save_data():
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id","name","hp","fuel","year","price"])
        writer.writeheader()
        for car in cars:
            writer.writerow(car)


# Visa statistik
def show_statistics(stdscr):
    stdscr.clear()
    
    
    # Hitta dyraste och billigaste
    dyrast = max(cars, key=lambda c: c['price'])
    billigast = min(cars, key=lambda c: c['price'])
    
    
    # Hitta starkaste
    starkast = max(cars, key=lambda c: c['hp'])
    
    # Hitta nyaste och äldsta
    nyast = max(cars, key=lambda c: c['year'])
    aldst = min(cars, key=lambda c: c['year'])
    
    
    # visa statistik
    stdscr.addstr(0, 0, "STATISTIK")
    stdscr.addstr(1, 0, "=" * 50)
    stdscr.addstr(3, 0, f"Antal bilar: {len(cars)} st")
    stdscr.addstr(5, 0, f"Dyrast: {dyrast['name']} - {int(dyrast['price']):,} kr".replace(",", " "))
    stdscr.addstr(6, 0, f"Billigast: {billigast['name']} - {int(billigast['price']):,} kr".replace(",", " "))
    stdscr.addstr(8, 0, f"Starkast: {starkast['name']} - {starkast['hp']} hk")
    stdscr.addstr(10, 0, f"Nyast: {nyast['name']} ({nyast['year']})")
    stdscr.addstr(11, 0, f"Äldst: {aldst['name']} ({aldst['year']})")
    stdscr.addstr(13, 0, "Tryck valfri tangent")
    stdscr.getch()


# Visar detaljer
def show_details(stdscr, car):
    stdscr.clear()
    stdscr.addstr(0,0,f"Bil: {car['name']}")
    stdscr.addstr(1,0,f"Hästkrafter: {car['hp']}")
    stdscr.addstr(2,0,f"Bränsle: {car['fuel']}")
    stdscr.addstr(3,0,f"År: {car['year']}")
    stdscr.addstr(4,0,f"Pris: {int(car['price']):,} kr".replace(",", " "))
    stdscr.addstr(6,0,"Tryck valfri tangent")
    stdscr.getch()


# Ny eller redigera
def input_car(stdscr, car=None):
    curses.echo()
    stdscr.clear()
    if car:
        stdscr.addstr(0,0,f"Redigera bil: {car['name']}")
    else:
        stdscr.addstr(0,0,"Lägg till ny bil")

    stdscr.addstr(2,0,f"Namn [{car['name'] if car else ''}]: ")
    name = stdscr.getstr().decode() or (car['name'] if car else "")

    stdscr.addstr(3,0,f"Hästkrafter [{car['hp'] if car else ''}]: ")
    hp_input = stdscr.getstr().decode()
    hp = int(hp_input) if hp_input else (car['hp'] if car else 0)

    stdscr.addstr(4,0,f"Bränsle [{car['fuel'] if car else ''}]: ")
    fuel = stdscr.getstr().decode() or (car['fuel'] if car else "")

    stdscr.addstr(5,0,f"År [{car['year'] if car else ''}]: ")
    year_input = stdscr.getstr().decode()
    year = int(year_input) if year_input else (car['year'] if car else 0)

    stdscr.addstr(6,0,f"Pris [{int(car['price']) if car else ''}]: ")
    price_input = stdscr.getstr().decode()
    price = float(price_input) if price_input else (car['price'] if car else 0)

    curses.noecho()
    return name, hp, fuel, year, price


# Skapar tabellen
def view_cars_table(cars):
    
    top = f"{'ID':<4} {'NAMN':<22} {'HK':<5} {'BRÄNSLE':<10} {'ÅR':<6} {'PRIS':<15}"
    separate = "=" * 65
    rows = []
    for car in cars:
        price_str = f"{int(car['price']):,}".replace(",", " ") + " kr"
        row = (
            f"{str(car['id'])[:4]:<4} "
            f"{truncate(car['name'], 22):<22} "
            f"{truncate(str(car['hp']), 5):<5} "
            f"{truncate(car['fuel'], 10):<10} "
            f"{truncate(str(car['year']), 6):<6} "
            f"{truncate(price_str, 15):<15}")
        rows.append(row)
    return "\n".join([top, separate] + rows)


# Meny
def main(stdscr):
    selected = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(0,0,"BILLISTA (upp/ned=bläddra, ENTER=info, N=ny, E=redigera, D=radera, T=statistik, S=spara, SPACE=avsluta)"[:w-1])

        # Skriv tabellen
        table_str = view_cars_table(cars)
        for idx, line in enumerate(table_str.splitlines(), 2):
            stdscr.addstr(idx, 0, line[:w-1])

        # Markören
        if cars:
            marker_line = 4 + selected
            stdscr.addstr(marker_line, 0, "->"[:w-1])

        key = stdscr.getch()
        
        # Navigation
        if cars:
            if key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(cars)-1:
                selected += 1
            elif key == 10:  # ENTER visar detaljer
                show_details(stdscr, cars[selected])
            elif key == ord('e') or key == ord('E'):  # redigera bil
                car = cars[selected]
                name, hp, fuel, year, price = input_car(stdscr, car)
                car['name'] = name
                car['hp'] = hp
                car['fuel'] = fuel
                car['year'] = year
                car['price'] = price
            elif key == ord('d') or key == ord('D'):  # ta bort bil
                cars.pop(selected)
                if selected >= len(cars) and len(cars) > 0:
                    selected = len(cars)-1
                elif len(cars) == 0:
                    selected = 0
        
        if key == ord('n') or key == ord('N'):  # ny bil
            name, hp, fuel, year, price = input_car(stdscr)
            new_id = max([c['id'] for c in cars], default=0) + 1
            cars.append({"id": new_id, "name": name, "hp": hp, "fuel": fuel, "year": year, "price": price})
            selected = len(cars) - 1
        elif key == ord('t') or key == ord('T'):  # statistik
            show_statistics(stdscr)
        elif key == ord('s') or key == ord('S'):  # spara
            save_data()
            stdscr.addstr(len(cars)+6,0,"Sparat till databas. Tryck valfri tangent"[:w-1])
            stdscr.getch()
        elif key == ord(' '):  # SPACE avslutar
            break

curses.wrapper(main)