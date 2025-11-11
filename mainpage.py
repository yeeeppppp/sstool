import os
import csv
import glob
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from datetime import datetime

console = Console()

def main():
    """Everything Replace - поиск файлов по системе"""
    try:
        console.print("=== Everything Replace ===")
        

        search_directory = "C:/"
        search_patterns = ["*.txt", "*.log", "*.csv", "*.doc", "*.docx", "*.pdf"]
        
        console.print(f"Поиск файлов в {search_directory}")
        console.print(f"Шаблоны поиска: {', '.join(search_patterns)}")
        
        found_files = []
        
    
        with Progress() as progress:
            task = progress.add_task("Поиск файлов...", total=None)
            
            for pattern in search_patterns:
                search_path = os.path.join(search_directory, "**", pattern)
                try:
                    files = glob.glob(search_path, recursive=True)
                    found_files.extend(files)
                except Exception as e:
                    console.print(f"Ошибка при поиске {pattern}: {e}")
        
    
        if found_files:
            table = Table(title=f"Найдено файлов: {len(found_files)}")
            table.add_column("Номер", style="cyan")
            table.add_column("Имя файла", style="white")
            table.add_column("Путь", style="green")
            table.add_column("Размер (КБ)", style="yellow")
            table.add_column("Изменен", style="blue")
            
            for i, file_path in enumerate(found_files[:10], 1):
                try:
                    file_name = os.path.basename(file_path)
                    size_kb = os.path.getsize(file_path) // 1024
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%d.%m.%Y %H:%M")
                    table.add_row(str(i), file_name, os.path.dirname(file_path), str(size_kb), mtime)
                except:
                    table.add_row(str(i), "N/A", "N/A", "N/A", "N/A")
            
            console.print(table)
            
            if len(found_files) > 10:
                console.print(f"... и еще {len(found_files) - 10} файлов")
            
       
            output_dir = "C:/output"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "everything_replace_results.csv")
            
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Имя файла', 'Полный путь', 'Размер (байт)', 'Дата изменения'])
                
                for file_path in found_files:
                    try:
                        file_name = os.path.basename(file_path)
                        size = os.path.getsize(file_path)
                        mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%d.%m.%Y %H:%M:%S")
                        writer.writerow([file_name, file_path, size, mtime])
                    except Exception as e:
                        writer.writerow([file_name, file_path, 'N/A', 'N/A'])
            
            console.print(f"Результаты сохранены в CSV: {output_path}")
            console.print(f"Всего найдено файлов: {len(found_files)}")
            
        else:
            console.print("Файлы по указанным шаблонам не найдены")
            
    except Exception as e:
        console.print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()