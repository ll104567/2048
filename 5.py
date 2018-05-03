#!/usr/bin/python
# coding:utf-8
# date 2018.03.14
# add Score
__author__ = 'HuS'

import curses
import random

win_value = -1
score = 0

UP,DOWN,LEFT,RIGHT=65,66,68,67

help_string1 = '----------(w)Up (s)Down (a)Left (d)Right---------'
help_string2 = '---------------(r)Restart (q)Quit----------------'
gameover_string = '====================Game Over====================='
win_string = '^^^^^^^^^^^^^^^^^^ You Win ^^^^^^^^^^^^^^^^^^'

def display_info(str, x, y,):
    global stdscr
    stdscr.addstr(y,x,str)
    stdscr.refresh()

def get_ch_and_continue():
    global stdscr
    try:
        stdscr.nodelay(0)
        ch=stdscr.getch()
        stdscr.nodelay(1)
    except:
        exit(2)
    return ch

def set_win():
    global stdscr
    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(1)

def unset_win():
    global stdscr
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

def generate(n=4):
    return [[0 for i in range(n)] for i in range(n)]

def get_max_length(l):
    max = 0
    for i in l:
        for j in i:
            if len(str(j)) > max:
                max = len(str(j))
    if max < 5 :
        return 5
    return max

def get_random_number():
    if random.randint(1,100) > 90:
        return 4
    else:
        return 2

def gui(l_in_l):
    
    size = len(l_in_l)
    length = get_max_length(l_in_l)

    gui_str = ''
    init_str = '+' + ('-'*length + '+')*size
    gui_str += init_str + '\n'

    for i in l_in_l:
        for j in i:
            if j == 0:
                j = ' '
            space = length - len(str(j))
            gui_str += '|' + ' '*space + str(j)
        gui_str += '|\n'
        gui_str += init_str + '\n'
    return gui_str

def reverse_l(l_in_l):

    new_l = []
    for i in l_in_l:
        new_l.append(i[::-1])
    
    return new_l

def reverse_l_x(l_in_l):

    n = len(l_in_l)
    
    new_l = [ [0 for i in range(n)] for i in range(n) ]
    for i in range(n):
        for j in range(n):
                new_l[i][j] = l_in_l[j][i]
    return new_l

def switch_up_down(l_in_l):
    
    return l_in_l[::-1]

def move_left(l_in_l):
   
    global score
    l_in_l = rebuild(l_in_l)
    size = len(l_in_l)
    new_l = [ [] for i in range(size) ]

    for i in range(len(l_in_l)):
        j = 0
        while j < size:
            if j == size - 1:
                new_l[i].append(l_in_l[i][j])
                break

            if l_in_l[i][j] == l_in_l[i][j+1]:
                new_l[i].append(l_in_l[i][j]*2)
                new_l[i].append(0)
                score += 2*l_in_l[i][j]
                j += 2
            else:
                new_l[i].append(l_in_l[i][j])
                j += 1

    return rebuild(new_l)

def move_right(l_in_l):
    
    l = reverse_l(l_in_l)
    new_l = move_left(l)
    l = rebuild(new_l)
    new_l = reverse_l(l)

    return new_l

def move_up(l_in_l):
    l = reverse_l_x(l_in_l) 
    l = rebuild(l)
    new_l = move_left(l)
    new_l = reverse_l_x(new_l)

    return new_l

def move_down(l_in_l):
   
    l = switch_up_down(l_in_l)
    new_l = move_up(l)
    new_l = switch_up_down(new_l)
    
    return new_l

def rebuild(l_in_l):
    
    n = len(l_in_l)
    new_l = [ [] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if l_in_l[i][j] != 0:
                new_l[i].append(l_in_l[i][j])
        if len(new_l[i]) < n:
            for x in range(n-len(new_l[i])):
                new_l[i].append(0)

    return new_l

def get_space_position(l_in_l):
    
    space_pool = []
    n = len(l_in_l)
    for i in range(n):
        for j in range(n):
            if l_in_l[i][j] == 0:
                space_pool.append([i,j])

    return space_pool

def get_a_random_position(l_in_l):

    x = get_space_position(l_in_l)
    if x:
        return random.choice(x)
    else:
        return None

def not_go_die(l_in_l):
    n = len(l_in_l)
    for i in range(n):
        for j in range(n):
            if j == n-1:
                break
            if l_in_l[i][j] == l_in_l[i][j+1]:
                return True
    for i in range(n):
        for j in range(n):
            if i == n-1:
                break
            if l_in_l[i][j] == l_in_l[i+1][j]:
                return True
    return False

def go_die(l_in_l):
    if not get_a_random_position(l_in_l):
        if not not_go_die(l_in_l):
            return True
    return False

def get_max_number(l_in_l):
    
    max = 0
    for i in l_in_l:
        for j in i:
            if j > max:
                max = j
    return max

def initial(l_in_l):
    l = l_in_l[:]
    a = get_a_random_position(l_in_l)
    l[a[0]][a[1]] = get_random_number()
    return l

def init(n=4):
    global score
    score = 0
    l_in_l = generate(n)
    l = initial(l_in_l)
    l_in_l = initial(l)
    return l_in_l

def win(l_in_l,win_value=2048):
    max = get_max_number(l_in_l)
    if win_value < 0:
        return False
    if max < win_value:
        return  False
    else:
        return True

def display():
    display_info('Score:{}'.format(score),0,0)
    display_info(gui(a),0,2)
    display_info(help_string1,0,12)
    display_info(help_string2,0,13)
    display_info('>>>',0,14)
nxn = 4
a = init(nxn)
stdscr = curses.initscr()

#### main 
while 1:
    try:
        set_win()
        if win(a,win_value):
            stdscr.clear()
            display_info(win_string,0,1)
            display() 
            while 1:
                c = get_ch_and_continue()
                if c in (ord('q'),ord('Q')):
                    exit()
                elif c in (ord('r'),ord('R')):
                    a = init(nxn)
                    break
        if go_die(a):
            stdscr.clear()
            display_info(gameover_string,0,1)
            display()
            while 1:
                c = get_ch_and_continue()
                if c in (ord('q'),ord('Q')):
                    exit()
                elif c in (ord('r'),ord('R')):
                    a = init(nxn)
                    break
                
        stdscr.clear()
        display()

        c = get_ch_and_continue()
        if c in (ord('q'),ord('Q')):
            exit()
        if c in (ord('r'),ord('R')):
            a = init(nxn)
        if c in (ord('x'),ord('X')):
            n = get_a_random_position(a)
            if n:
                score = 999999
                if win_value > 0:
                    a[n[0]][n[1]] = win_value
                else:
                    a[n[0]][n[1]] = 2048

        if c in (ord('w'),UP):
            a = move_up(a)
            n = get_a_random_position(a)
            if n:
                a[n[0]][n[1]] = get_random_number()
        if c in (ord('a'),LEFT):
            a = move_left(a)
            n = get_a_random_position(a)
            if n:
                a[n[0]][n[1]] = get_random_number()
        if c in (ord('s'),DOWN):
            a = move_down(a)
            n = get_a_random_position(a)
            if n:
                a[n[0]][n[1]] = get_random_number()
        if c in (ord('d'),RIGHT):
            a = move_right(a)
            n = get_a_random_position(a)
            if n:
                a[n[0]][n[1]] = get_random_number()
        else:
            continue
    except:
        exit()
    finally:
        unset_win()
