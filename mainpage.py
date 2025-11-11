import os
import sys
import importlib
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

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
    table.add_row("11", "Анализ модификации")  
    table.add_row("0", "Выход из программы")
    console.print(table)

class FunctionManager:
    def __init__(self):
        self.function_pool = {
            "1": {"menu_name": "Everything Replace", "file": "file_searcher", "function": "main"},
            "2": {"menu_name": "RecycleBin Analyzer", "file": "recycle_bin_analyzer", "function": "main"},
            "3": {"menu_name": "Registry Parser", "file": "registry_parser", "function": "main"},
            "4": {"menu_name": "Проверка запущенных exe/bat/py", "file": "LastExt", "function": "main"},
            "5": {"menu_name": "Поиск DLL", "file": "signature_checker_dll", "function": "main"},
            "6": {"menu_name": "Firewall Checker", "file": "firewall_parser", "function": "main"},
            "7": {"menu_name": "Service Checker", "file": "service_checker", "function": "main"},
            "8": {"menu_name": "Проверка очистки USN и журнала аудита", "file": "evtx_check", "function": "main"},
            "9": {"menu_name": "Проверка подключенных USB", "file": "usb", "function": "main"},
            "10": {"menu_name": "Анализ стороннего ПО", "file": "ddfo_detect", "function": "main"},
            "11": {"menu_name": "Анализ модификации", "file": "modanalyzer", "function": "main"}  # Добавлена новая связка
        }
        
    def load_function(self, choice):
        """Загружает и выполняет функцию по выбору"""
        if choice not in self.function_pool:
            return False
            
        func_info = self.function_pool[choice]
        menu_name = func_info["menu_name"]
        file_name = func_info["file"]
        function_name = func_info["function"]
        
        console.print(f"\n[bold yellow]Запуск {menu_name}...[/bold yellow]")
        
        try:
            module = importlib.import_module(file_name)
            
            if hasattr(module, function_name):
                func = getattr(module, function_name)
                func()  
                console.print(f"[bold green] {menu_name} завершено![/bold green]")
                return True
            else:
                functions = [name for name in dir(module) 
                           if not name.startswith('_') and callable(getattr(module, name))]
                
                if functions:
                    func = getattr(module, functions[0])
                    console.print(f"[yellow] Функция '{function_name}' не найдена, используем '{functions[0]}'[/yellow]")
                    func()
                    console.print(f"[bold green] {menu_name} завершено![/bold green]")
                    return True
                else:
                    console.print(f"[red] В файле {file_name}.py не найдено функций[/red]")
                    return False
                    
        except ImportError:
            console.print(f"[red] Файл {file_name}.py не найден в папке src[/red]")
            return False
        except Exception as e:
            console.print(f"[red] Ошибка в {menu_name}: {str(e)}[/red]")
            return False

def main():
    show_title()
    
    function_manager = FunctionManager()
    
    while True:
        show_menu()
        console.print("[green]Введите номер пункта[/]")
        choice = Prompt.ask("", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])  # Добавлен выбор 11
        
        if choice == "0":
            console.print("Выход из программы. Пока!", style="bold red")
            break
        
        function_manager.load_function(choice)
        
        console.print("\n[italic]Нажмите Enter для продолжения...[/italic]")
        input()

if __name__ == "__main__":
    main()

