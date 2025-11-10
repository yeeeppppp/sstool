import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table

# Добавляем текущую папку в путь для импортов
sys.path.append(os.path.dirname(__file__))

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

def load_functions():
    """Динамически загружает функции из всех модулей"""
    
    # Словарь для импортов
    modules_to_import = {
        'file_searcher': 'everything_replace',
        'recycle_bin_analyzer': 'recycle_bin_analyzer', 
        'registry_parser': 'registry_parser',
        'LastExt': 'check_running_files',
        'signature_checker_dll': 'signature_checker_dll',
        'firewall_parser': 'firewall_checker',
        'service_checker': 'service_checker',
        'evtx_check': 'check_usn_and_audit',
        'usb': 'check_usb_devices',
        'ddfo_detect': 'analyze_third_party_software'
    }
    
    functions = {}
    
    for module_name, function_name in modules_to_import.items():
        try:
            # Динамический импорт
            module = __import__(module_name)
            function = getattr(module, function_name)
            functions[function_name] = function
            console.print(f"[green]✓ Загружен: {module_name}.{function_name}[/green]")
        except ImportError as e:
            console.print(f"[yellow]⚠ Модуль {module_name} не найден: {e}[/yellow]")
            # Создаем заглушку
            def stub_function():
                console.print(f"[yellow]{function_name}: Модуль {module_name}.py не найден[/yellow]")
            functions[function_name] = stub_function
        except AttributeError as e:
            console.print(f"[yellow]⚠ Функция {function_name} не найдена в {module_name}: {e}[/yellow]")
            # Создаем заглушку
            def stub_function():
                console.print(f"[yellow]{function_name}: Функция не найдена в {module_name}.py[/yellow]")
            functions[function_name] = stub_function
    
    return functions

def main():
    show_title()
    
    # Загружаем все функции
    console.print("\n[bold cyan]Загрузка модулей...[/bold cyan]")
    functions = load_functions()
    
    # Словарь для связи пунктов меню с функциями
    menu_actions = {
        '1': ("Everything Replace", functions.get('everything_replace')),
        '2': ("RecycleBin Analyzer", functions.get('recycle_bin_analyzer')),
        '3': ("Registry Parser", functions.get('registry_parser')),
        '4': ("Проверка запущенных файлов", functions.get('check_running_files')),
        '5': ("Поиск DLL", functions.get('signature_checker_dll')),
        '6': ("Firewall Checker", functions.get('firewall_checker')),
        '7': ("Service Checker", functions.get('service_checker')),
        '8': ("Проверка USN и аудита", functions.get('check_usn_and_audit')),
        '9': ("Проверка USB устройств", functions.get('check_usb_devices')),
        '10': ("Анализ стороннего ПО", functions.get('analyze_third_party_software'))
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
            if function:
                console.print(f"\n[bold yellow]Запуск {function_name}...[/bold yellow]")
                try:
                    # Вызываем функцию
                    function()
                    console.print(f"[bold green]✓ {function_name} завершено![/bold green]")
                except Exception as e:
                    console.print(f"[bold red]✗ Ошибка в {function_name}: {str(e)}[/bold red]")
            else:
                console.print(f"[bold red]✗ Функция {function_name} не загружена[/bold red]")
        else:
            console.print("Некорректный ввод!", style="bold red")
        
        # Пауза перед следующим выбором
        if choice != "0":
            console.print("\n[italic]Нажмите Enter для продолжения...[/italic]")
            input()

if __name__ == "__main__":
    main()