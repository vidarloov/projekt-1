import csv
import os
import locale
import curses

CSV_FILE = 'db_bilar.csv'

def format_currency(value):
    try:
        return locale.currency(float(value), grouping=True)
    except Exception:
        return f"{float(value):,.2f} kr".replace(",", " ").replace(".", ",")

def load_data(filename):
    products = []
    if not os.path.exists(filename):
        # Skapa testfil om den saknas
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id','name','hp','fuel','year','price'])
            writer.writerow([1, 'BMW E30 325i', '170', 'Bensin', '1989', '85000'])
            writer.writerow([2, 'Saab 900 Turbo', '175', 'Bensin', '1991', '49000'])
            writer.writerow([3, 'Audi 80 B4', '115', 'Bensin', '1994', '43000'])
            writer.writerow([4, 'Subaru Impreza GT', '211', 'Bensin', '1998', '99000'])
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append({
                "id": int(row['id']),
                "name": row['name'],
                "hp": int(row['hp']),
                "fuel": row['fuel'],
                "year": int(row['year']),
                "price": float(row['price'])
            })
    return products

def save_data(filename, products):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ["id", "name", "hp", "fuel", "year", "price"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def show_table_curses(products):
    def _table(stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        selected = 0
        col_id    = 4
        col_name  = 22
        col_hp    = 8
        col_fuel  = 10
        col_year  = 8
        col_price = 14

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            # Header med tangentinfo
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(0, 0, " Lagedit 1.0 ".ljust(w-1))
            stdscr.addstr(0, min(22, w-15), "[UPP/NED] Navigera [ENTER] Välj [N] Ny [S] Spara [ESC] Avsluta"[:w-23])
            stdscr.attroff(curses.color_pair(2))
            stdscr.attron(curses.color_pair(3))
            headline = f"{'#':<{col_id}}{'NAMN':<{col_name}}{'HK':<{col_hp}}{'BRÄNSLE':<{col_fuel}}{'ÅR':<{col_year}}{'PRIS':>{col_price}}"
            stdscr.addstr(2, 0, headline[:w-1])
            stdscr.attroff(curses.color_pair(3))
            stdscr.addstr(3, 0, "-" * (w-1))
            table_start = 4
            visible_rows = h - table_start - 2
            start_idx = max(0, min(selected - visible_rows//2, max(0, len(products)-visible_rows)))
            for idx, product in enumerate(products[start_idx:start_idx+visible_rows]):
                abs_idx = start_idx + idx
                name = product['name'][:col_name-1]
                hp = str(product['hp'])
                fuel = product['fuel'][:col_fuel-1]
                year = str(product['year'])
                price = format_currency(product['price'])
                row = f"{product['id']:<{col_id}}{name:<{col_name}}{hp:<{col_hp}}{fuel:<{col_fuel}}{year:<{col_year}}{price:>{col_price}}"
                if abs_idx == selected:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(table_start + idx, 0, row[:w-1])
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(table_start + idx, 0, row[:w-1])
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_DOWN and selected < len(products)-1:
                selected += 1
            elif key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == ord('n') or key == ord('N'):
                # Lägg till ny produkt
                curses.echo()
                stdscr.clear()
                stdscr.addstr(0, 0, "Lägg till ny bil:")
                stdscr.addstr(1, 0, "Namn: ")
                name = stdscr.getstr(1, 6, 40).decode("utf-8")
                stdscr.addstr(2, 0, "Hästkrafter: ")
                hp = int(stdscr.getstr(2, 13, 7).decode("utf-8"))
                stdscr.addstr(3, 0, "Bränsletyp: ")
                fuel = stdscr.getstr(3, 11, 10).decode("utf-8")
                stdscr.addstr(4, 0, "Årsmodell: ")
                year = int(stdscr.getstr(4, 11, 6).decode("utf-8"))
                stdscr.addstr(5, 0, "Pris: ")
                price = float(stdscr.getstr(5, 6, 15).decode("utf-8"))
                curses.noecho()
                new_id = max([p["id"] for p in products], default=0) + 1
                products.append({
                    "id": new_id,
                    "name": name,
                    "hp": hp,
                    "fuel": fuel,
                    "year": year,
                    "price": price
                })
                stdscr.addstr(7, 0, f"Bilen '{name}' tillagd! Tryck valfri tangent.")
                stdscr.getch()
            elif key == ord('s') or key == ord('S'):
                save_data(CSV_FILE, products)
                stdscr.addstr(h-1, 0, "Sparat till fil! Tryck valfri tangent.")
                stdscr.getch()
            elif key == ord('\n'):
                # Visa detaljer
                p = products[selected]
                stdscr.clear()
                stdscr.addstr(0, 0, f"Bil: {p['name']}")
                stdscr.addstr(1, 0, f"Hästkrafter: {p['hp']}")
                stdscr.addstr(2, 0, f"Bränsle: {p['fuel']}")
                stdscr.addstr(3, 0, f"Årsmodell: {p['year']}")
                stdscr.addstr(4, 0, f"Pris: {format_currency(p['price'])}")
                stdscr.addstr(6, 0, "[ESC] Tillbaka")
                stdscr.refresh()
                k = stdscr.getch()
                # ESC går tillbaka, annars ignoreras
            elif key == 27: # ESC
                break
    curses.wrapper(_table)

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  
products = load_data(CSV_FILE)
show_table_curses(products)
# Programmet slutar här, ingen extra input/radering utanför curses längre.