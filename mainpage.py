from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from file_searcher import everything_replace
from recycle_bin_analyzer import recycle_bin_analyzer
from registry_parser import registry_parser
from LastExt import check_running_files
from signature_checker_dll import signature_checker_dll
from firewall_parser import firewall_checker
from service_checker import service_checker
from evtx_check import check_usn_and_audit
from usb import check_usb_devices
from ddfo_detect import analyze_third_party_software

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
    table.add_row("1", "Everything Replace")
    table.add_row("2", "RecycleBin Analyzer")
    table.add_row("3", "Registry Parser")
    table.add_row("4", "Проверка запущенных exe/bat/py")
    table.add_row("5", "Поиск DLL")
    table.add_row("6", "Firewall Checker")
    table.add_row("7", "Service Checker")
    table.add_row("8", "Проверка очистки USN и журнала аудита")
    table.add_row("9", "Проверка подключенных USB")
    table.add_row("10", "Анализ стороннего ПО")
    table.add_row("0", "Выход из программы")
    console.print(table)

def main():
    show_title()
    menu_actions = {
        '1': ("Everything Replace", everything_replace),
        '2': ("RecycleBin Analyzer", recycle_bin_analyzer),
        '3': ("Registry Parser", registry_parser),
        '4': ("Проверка запущенных файлов", check_running_files),
        '5': ("Поиск DLL", signature_checker_dll),
        '6': ("Firewall Checker", firewall_checker),
        '7': ("Service Checker", service_checker),
        '8': ("Проверка USN и аудита", check_usn_and_audit),
        '9': ("Проверка USB устройств", check_usb_devices),
        '10': ("Анализ стороннего ПО", analyze_third_party_software)
    }
    
    while True:
        show_menu()
        console.print("[green]Введите номер пункта[/]")
        choice = Prompt.ask("", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        
        if choice == "0":
            console.print("Выход из программы. Пока!", style="bold red")
            break
        
        if choice in menu_actions:
            function_name, function = menu_actions[choice]
            console.print(f"\n[bold yellow]Запуск {function_name}...[/bold yellow]")
            try:
                function()
                console.print(f"[bold green]✓ {function_name} завершено успешно![/bold green]")
            except Exception as e:
                console.print(f"[bold red]✗ Ошибка в {function_name}: {str(e)}[/bold red]")
        else:
            console.print("Некорректный ввод!", style="bold red")
        if choice != "0":
            console.print("\n[italic]Нажмите Enter для продолжения...[/italic]")
            input()

if __name__ == "__main__":
    main()