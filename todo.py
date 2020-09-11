#!/usr/bin/python3

import curses
import json
import sys
import os

PATH = os.path.dirname(os.path.realpath(__file__))
def get_todos():
    with open(f"{PATH}/todos.json", "r") as tdj:
        return json.load(tdj)

def save_todos(todos):
    with open(f"{PATH}/todos.json", "w") as tdj:
        json.dump(todos,tdj)

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    main_loop(stdscr)

def main_loop(stdscr):
    todos = get_todos()
    maxh, maxw = stdscr.getmaxyx()
    startline = 0
    endline = maxh - 2
    selected = 0
    while True:
        stdscr.clear()
        for i,item in enumerate(todos["todos"]):
            if i < startline:
                continue
            if i > endline:
                break
            status = "[x]" if item["status"] else "[ ]"
            description = item["description"]
            if i == selected:
                stdscr.addstr(f"{status} {description}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"{status} {description}\n")

        stdscr.addstr(maxh-1,0,f"[{selected}] j:down,k:up,space:toggle,d:delete,a:add new")
        stdscr.refresh()
        key = stdscr.getkey()
        if key == "q":
            curses.curs_set(1)
            sys.exit(0)
        elif key == "j":
            selected=min(selected+1,len(todos["todos"]))
            if selected > endline:
                endline += 1
                startline += 1
        elif key == "k":
            selected=max(selected-1,0)
            if selected < startline:
                startline -= 1
                endline -= 1
        elif key == " ":
            todos["todos"][selected]["status"] = not todos["todos"][selected]["status"]
            save_todos(todos)
        elif key == "d":
            del todos["todos"][selected]
            save_todos(todos)
        elif key == "a":
            stdscr.addstr(maxh-1,0, "Add Item:                                                ")
            curses.echo()
            inp = stdscr.getstr(maxh-1,10,128)
            todos["todos"].append({"status": False, "description": str(inp, "utf-8")})
            save_todos(todos)

curses.wrapper(main)
