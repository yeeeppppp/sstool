import os
import sys
import importlib
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.align import Align
from rich import box
import time

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
    
    
    title_panel = Panel(
        Align.center(
            Text(ascii_art_scanner, style="bold red")
        ),
        box=box.DOUBLE_EDGE,
        border_style="red",
        padding=(1, 2),
    )
    console.print(title_panel)

def show_menu():
    
    menu_table = Table(
        show_header=True,
        header_style="bold red",
        box=box.ROUNDED,
        border_style="red",
    )
    
    menu_table.add_column("№", justify="center", style="bold red", width=8)
    menu_table.add_column("ОПИСАНИЕ", style="white", width=50)
    menu_table.add_column("СТАТУС", justify="center", style="red", width=15)
    
    menu_items = [
        ("1", "Everything Replace", "ГОТОВ"),
        ("2", "RecycleBin Analyzer", "ГОТОВ"),
        ("3", "Registry Parser", "ГОТОВ"),
        ("4", "Проверка запущенных exe/bat/py", "ГОТОВ"),
        ("5", "Поиск DLL", "ГОТОВ"),
        ("6", "Firewall Checker", "ГОТОВ"),
        ("7", "Service Checker", "ГОТОВ"),
        ("8", "Проверка очистки USN и журнала аудита", "ГОТОВ"),
        ("9", "Проверка подключенных USB", "ГОТОВ"),
        ("10", "Анализ стороннего ПО", "ГОТОВ"),
        ("11", "Анализ модификации", "ГОТОВ"),
        ("0", "Выход из программы", "ВЫХОД")
    ]
    
    for num, desc, status in menu_items:
        menu_table.add_row(
            f"[red]{num}[/red]",
            f"[white]{desc}[/white]",
            f"[red]{status}[/red]"
        )
    
    console.print()
    console.print(menu_table)

def show_loading_animation(message="Выполняется сканирование"):
    """Показывает анимацию загрузки в красном стиле"""
    with Progress(
        SpinnerColumn(spinner_name="dots", style="red"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="red", finished_style="red"),
        TaskProgressColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task(f"[red]{message}...", total=100)
        
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.02)

def show_success_message(module_name, execution_time=None):
    """Показывает сообщение о выполнении"""
    success_panel = Panel(
        Align.center(
            Text(f"Модуль: [white]{module_name}[/white]", style="red") +
            (Text(f"\nВремя выполнения: [white]{execution_time:.2f} сек[/white]", style="red") 
             if execution_time else Text(""))
        ),
        box=box.ROUNDED,
        border_style="red",
        padding=(1, 2),
    )
    console.print(success_panel)

def show_error_message(module_name, error):
    """Показывает сообщение об ошибке"""
    error_panel = Panel(
        Align.center(
            Text(f"Модуль: [white]{module_name}[/white]", style="red") +
            Text(f"\nОшибка: [white]{error}[/white]", style="red")
        ),
        box=box.ROUNDED,
        border_style="red",
        padding=(1, 2),
    )
    console.print(error_panel)

def show_module_not_found(module_name):
    """Показывает сообщение о ненайденном модуле"""
    not_found_panel = Panel(
        Align.center(
            Text(f"Файл: [white]{module_name}.py[/white]", style="red") +
            Text("\nФайл не найден в папке src", style="red")
        ),
        box=box.ROUNDED,
        border_style="red",
        padding=(1, 2),
    )
    console.print(not_found_panel)

def show_function_not_found(module_name, function_name, fallback_function):
    """Показывает сообщение о ненайденной функции"""
    function_panel = Panel(
        Align.center(
            Text(f"Модуль: [white]{module_name}[/white]", style="red") +
            Text(f"\nФункция не найдена: [white]{function_name}[/white]", style="red") +
            Text(f"\nИспользована: [white]{fallback_function}[/white]", style="red")
        ),
        box=box.ROUNDED,
        border_style="red",
        padding=(1, 2),
    )
    console.print(function_panel)

def show_exit_message():
    """Показывает сообщение о выходе"""
    exit_panel = Panel(
        Align.center(
            Text("Завершение работы", style="red")
        ),
        box=box.DOUBLE_EDGE,
        border_style="red",
        padding=(1, 2),
    )
    console.print(exit_panel)

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
            "11": {"menu_name": "Анализ модификации", "file": "modanalyzer", "function": "main"}
        }
        
    def load_function(self, choice):
        """Загружает и выполняет функцию по выбору"""
        if choice not in self.function_pool:
            return False
            
        func_info = self.function_pool[choice]
        menu_name = func_info["menu_name"]
        file_name = func_info["file"]
        function_name = func_info["function"]
        
       
        start_panel = Panel(
            Align.center(
                Text(f"Модуль: [white]{menu_name}[/white]", style="red") +
                Text(f"\nФайл: [white]{file_name}.py[/white]", style="red")
            ),
            box=box.ROUNDED,
            border_style="red",
            padding=(1, 2),
        )
        console.print(start_panel)
        
        try:
            
            show_loading_animation(f"Инициализация {menu_name}")
            
            start_time = time.time()
            module = importlib.import_module(file_name)
            
            if hasattr(module, function_name):
                func = getattr(module, function_name)
                func()  
                execution_time = time.time() - start_time
                show_success_message(menu_name, execution_time)
                return True
            else:
                functions = [name for name in dir(module) 
                           if not name.startswith('_') and callable(getattr(module, name))]
                
                if functions:
                    fallback_function = functions[0]
                    show_function_not_found(file_name, function_name, fallback_function)
                    
                    show_loading_animation(f"Выполнение {menu_name}")
                    start_time = time.time()
                    func = getattr(module, fallback_function)
                    func()
                    execution_time = time.time() - start_time
                    show_success_message(menu_name, execution_time)
                    return True
                else:
                    show_error_message(menu_name, "В модуле не найдено подходящих функций")
                    return False
                    
        except ImportError:
            show_module_not_found(file_name)
            return False
        except Exception as e:
            show_error_message(menu_name, str(e))
            return False

def main():
    show_title()
    
    function_manager = FunctionManager()
    
    while True:
        show_menu()
        console.print()
        
      
        choice = Prompt.ask(
            "Ваш выбор", 
            choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
            show_choices=False
        )
        
        if choice == "0":
            show_exit_message()
            break
        
        function_manager.load_function(choice)
        
       
        console.print("[red]Нажмите Enter для продолжения...[/red]")
        input()

if __name__ == "__main__":
    main()