#!/usr/bin/env python2
import curses

class promptr(object):
    def __init__(self):
        import curses
    
    class button(object):
        def __init__(self, name, function):
            self.name = name
            self.function = function
        def off(self,stdscr):
            stdscr.addstr(self.name)
        def hover(self,stdscr):
            stdscr.addstr(self.name, curses.A_REVERSE)
        def info(self, stdscr, success):
            y, x = stdscr.getyx()
            stdscr.move(0,0)
            stdscr.addstr(str(success))
            stdscr.move(y,x)
        def press(self, stdscr):
            try:
                success = self.function(stdscr=stdscr)
            except:
                success = self.function()
            self.info(stdscr, success)

    
    def navigate(self, menu): 
        
        def menuList(stdscr, menu, cursor):
            i = 0
            centerX = curses.COLS /2
            
            for item in menu:
                if hasattr(item[1], 'name'):
                    offset = len(item[1].name) / 2
                else:
                    offset = len(item[0]) / 2
                stdscr.move(i*2+5, centerX - offset)
                if i == cursor:
                    pos = i*3+5
                    if hasattr(item[1], 'hover'):
                        item[1].hover(stdscr)
                    else:
                        stdscr.addstr( item[0], curses.A_REVERSE)
                else:
                    pos = i*3+5
                    if hasattr(item[1], 'off'):
                        item[1].off(stdscr)
                    else:
                        stdscr.addstr( item[0] )
                i +=1
                
            stdscr.move(0,0)
            stdscr.refresh()
        cursor = 0
        while True:
            stdscr = curses.initscr()
            try:
                curses.start_color()
            except:
                pass
            curses.curs_set(0)
            curses.noecho()
            curses.cbreak()
            stdscr.keypad(True)
            stdscr.clear()

            
            while True: 
                
                menuList(stdscr, menu, cursor)
                
                ch = stdscr.getch()
                
                if ch == curses.KEY_UP:
                    cursor -=1
                elif ch == curses.KEY_DOWN:
                    cursor +=1
                elif ch == curses.KEY_RIGHT:
                    if type(menu[cursor][1]) is list:
                        self.navigate(menu[cursor][1])
                    elif isinstance(menu[cursor][1], self.button):
                        menu[cursor][1].press(stdscr)
                    break
                    curses.noecho()
                    curses.cbreak()
                    stdscr.keypad(True)
                elif ch == curses.KEY_LEFT:
                    curses.nocbreak()
                    stdscr.keypad(False)
                    curses.echo()
                    curses.endwin()
                    return 1
                elif ch == save:
                    saveData            
                if cursor < 0:
                    cursor = 0
                if cursor >= len(menu):
                    cursor = len(menu) - 1 

    


if __name__ == '__main__':
    
    
    something =0
    
    window = promptr()

    def dummy(stdscr):
        i = 0
        stdscr.clear()
        stdscr.addstr('helo')
        stdscr.getch()
        return 0
    
    button1 = promptr.button( 'up' ,dummy)
    button2 = promptr.button( 'down' ,dummy)
    
    
    settingsMenu = [ ('Account Settings', button1) , ('Treasurer Settings', 'settingsWindow') ]
    
    financeMenu = [ ('view stats', 'statsWindow') , ('Change Settings', settingsMenu) ]
    duesMenu = [('list current members', 'membersWindow') , ('member refund', 'refundWindow')]
    billsMenu = [ ('some garbage', button1 ), ('Pay Water', 'waterWindow') ]
    
    mainMenu = [ ('Bill Payment', billsMenu) , ('Membership Dues', duesMenu), ('Financal Information', financeMenu)]
    
    window.navigate(mainMenu)
