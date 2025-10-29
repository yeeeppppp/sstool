from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table

console = Console()

def show_title():
    ascii_art_scanner = """
  ░██████                                               ░██████████░██                                      
 ░██   ░██                                                  ░██                                             
░██         ░████████   ░██████    ░███████   ░███████      ░██    ░██░█████████████   ░███████   ░███████  
 ░████████  ░██    ░██       ░██  ░██    ░██ ░██    ░██     ░██    ░██░██   ░██   ░██ ░██    ░██ ░██        
        ░██ ░██    ░██  ░███████  ░██        ░█████████     ░██    ░██░██   ░██   ░██ ░█████████  ░███████  
 ░██   ░██  ░███   ░██ ░██   ░██  ░██    ░██ ░██            ░██    ░██░██   ░██   ░██ ░██               ░██ 
  ░██████   ░██░█████   ░█████░██  ░███████   ░███████      ░██    ░██░██   ░██   ░██  ░███████   ░███████  
            ░██                                                                                             
            ░██
"""
    panel_style = "bold red"
    console.print(Panel(Text(ascii_art_scanner, style=panel_style), border_style=panel_style))
    signature = Text("dev: avarice.dll // m3tad0n.", style="italic cyan")
    console.print(signature, justify="center")

def show_menu():
    table = Table(title="Выберите сканирование", style="red")
    table.add_column("Номер", justify="center", style="bold red")
    table.add_column("Описание", style="white")
    table.add_row("1", "EverythingReplace")
    table.add_row("2", "RecycleBinAnalyzer")
    table.add_row("3", "Registry Parser")
    table.add_row("4", "Проверка запущенных exe/bat/py")
    table.add_row("5", "Signature Checker (.dll)")
    table.add_row("6", "Firewall Checker")
    table.add_row("7", "Service Checker")
    table.add_row("0", "Выход из программы")
    console.print(table)

def show_registry_parser_menu():
    console.print(Panel(Text("Registry Parser - выберите пункт:\n"
                              "1. OpenPidSaveMRU\n"
                              "2. PrefetchEnable\n"
                              "3. RecentDocs\n"
                              "4. NetworkHistory\n"
                              "5. PcaSvcCheck", style="bold cyan"),
                        title="Registry Parser Меню", border_style="cyan"))
    choice = Prompt.ask("Введите номер пункта", choices=["1", "2", "3", "4", "5", "0"])
    if choice == "0":
        return
    elif choice == "1":
        console.print("Запуск OpenPidSaveMRU...", style="yellow")
    elif choice == "2":
        console.print("Запуск PrefetchEnable...", style="yellow")
    elif choice == "3":
        console.print("Запуск RecentDocs...", style="yellow")
    elif choice == "4":
        console.print("Запуск NetworkHistory...", style="yellow")
    elif choice == "5":
        console.print("Запуск PcaSvcCheck...", style="yellow")

def main():
    show_title()
    while True:
        show_menu()
        console.print("[green]Введите номер пункта[/]")
        choice = Prompt.ask("", choices=["0", "1", "2", "3", "4", "5", "6", "7"])
        if choice == "0":
            console.print("Выход из программы. Пока!", style="bold red")
            break
        elif choice == "1":
            console.print("Запуск EverythingReplace...", style="red")
        elif choice == "2":
            console.print("Запуск RecycleBinAnalyzer...", style="red")
        elif choice == "3":
            show_registry_parser_menu()
        elif choice == "4":
            console.print("Проверка запущенных exe/bat/py...", style="red")
        elif choice == "5":
            console.print("Запуск Signature Checker (.dll)...", style="red")
        elif choice == "6":
            console.print("Запуск Firewall Checker ...", style="red")
        elif choice == "7":
            console.print("Запуск Service Checker ...", style="red")
        else:
            console.print("Некорректный ввод!", style="bold red")

if __name__ == "__main__":
    main()