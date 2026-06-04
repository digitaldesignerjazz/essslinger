#!/usr/bin/env python3
import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(__file__), ".todo.json")


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as fp:
            return json.load(fp)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as fp:
        json.dump(tasks, fp, indent=2, ensure_ascii=False)


def print_usage():
    print("Usage: todo.py <command> [args]")
    print("Commands:")
    print("  add <task>       Add a new task")
    print("  list             Show all tasks")
    print("  done <number>    Mark a task as completed")
    print("  remove <number>  Remove a task")
    print("  clear            Remove all tasks")
    print("  help             Show this help message")


def list_tasks(tasks):
    if not tasks:
        print("Keine Aufgaben vorhanden.")
        return

    print("To-Do-Liste:")
    for index, task in enumerate(tasks, start=1):
        status = "x" if task.get("done") else " "
        print(f"{index}. [{status}] {task['text']}")


def add_task(tasks, args):
    if not args:
        print("Fehler: Bitte gib eine Aufgabe an.")
        return
    text = " ".join(args).strip()
    if not text:
        print("Fehler: Aufgabe kann nicht leer sein.")
        return
    tasks.append({"text": text, "done": False})
    save_tasks(tasks)
    print(f"Aufgabe hinzugefügt: {text}")


def mark_done(tasks, args):
    if not args or not args[0].isdigit():
        print("Fehler: Bitte gib die Nummer der abzuschließenden Aufgabe an.")
        return
    index = int(args[0]) - 1
    if index < 0 or index >= len(tasks):
        print("Fehler: Ungültige Aufgabennummer.")
        return
    tasks[index]["done"] = True
    save_tasks(tasks)
    print(f"Aufgabe abgeschlossen: {tasks[index]['text']}")


def remove_task(tasks, args):
    if not args or not args[0].isdigit():
        print("Fehler: Bitte gib die Nummer der zu entfernenden Aufgabe an.")
        return
    index = int(args[0]) - 1
    if index < 0 or index >= len(tasks):
        print("Fehler: Ungültige Aufgabennummer.")
        return
    task = tasks.pop(index)
    save_tasks(tasks)
    print(f"Aufgabe entfernt: {task['text']}")


def clear_tasks(tasks):
    if not tasks:
        print("Keine Aufgaben zum Entfernen.")
        return
    save_tasks([])
    print("Alle Aufgaben wurden entfernt.")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()
    args = sys.argv[2:]
    tasks = load_tasks()

    if command == "add":
        add_task(tasks, args)
    elif command == "list":
        list_tasks(tasks)
    elif command == "done":
        mark_done(tasks, args)
    elif command == "remove":
        remove_task(tasks, args)
    elif command == "clear":
        clear_tasks(tasks)
    elif command == "help" or command == "-h" or command == "--help":
        print_usage()
    else:
        print(f"Unbekannter Befehl: {command}")
        print_usage()


if __name__ == "__main__":
    main()
