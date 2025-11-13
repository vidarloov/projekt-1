import curses 

def main(main_window): 
    curses.curs_set(0)
    
    items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"] 
    current_row = 0 

    def print_menu(main_window, selected_row): 
        main_window.clear() 
        h, w = main_window.getmaxyx() 
        
        for idx, row in enumerate(items): 
            x = w // 2 - len(row) // 2 
            y = h // 2 - len(items) // 2 + idx 
            
            if idx == selected_row: 
                main_window.attron(curses.color_pair(1)) 
                main_window.addstr(y, x, row) 
                main_window.attroff(curses.color_pair(1)) 
            
            else: 
                main_window.addstr(y, x, row) 
        
        main_window.refresh() 
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) 

    print_menu(main_window, current_row)
        
    while True: 
        key = main_window.getch() 
        
        if key == curses.KEY_UP and current_row > 0: 
            current_row -= 1 
        
        elif key == curses.KEY_DOWN and current_row < len(items) - 1: 
            current_row += 1 
        
        elif key == ord('\n'): 
            main_window.addstr(0, 0, f"You selected '{items[current_row]}'") 
            main_window.refresh() 
            main_window.getch() 
            break 
        
        print_menu(main_window, current_row)
    
curses.wrapper(main)