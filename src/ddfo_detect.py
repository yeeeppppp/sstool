import os
import csv
import psutil
import time
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import mmap
import ctypes
from ctypes import wintypes
import subprocess
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import win32file
import win32con

console = Console()

def main():
    """Поиск подозрительных файлов и Java читов"""
    console.print("=== Поиск подозрительных файлов и Java читов ===")
    
    all_results = []
    
    # Быстрый поиск по целевым местам
    custom_results = fast_search_custom_files()
    all_results.extend(custom_results)
    
    # Поиск Java читов
    java_results = search_java_cheats()
    all_results.extend(java_results)
    
    # Сохраняем все результаты в один CSV
    save_all_results_to_csv(all_results)
    
    # Выводим общие результаты
    display_final_results(all_results)

def save_all_results_to_csv(all_results):
    """Сохраняет все результаты в один CSV файл"""
    output_dir = "C:/output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, "detection.csv")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'type', 'file_path', 'file_name', 'file_size', 'reason', 
            'hidden', 'found_time', 'file_modified', 'file_created'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in all_results:
            row = {
                'type': result.get('type', 'UNKNOWN'),
                'file_path': result.get('path', ''),
                'file_name': result.get('name', ''),
                'file_size': result.get('size', 0),
                'reason': result.get('reason', ''),
                'hidden': result.get('hidden', 'Нет'),
                'found_time': result.get('found_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                'file_modified': result.get('file_modified', ''),
                'file_created': result.get('file_created', '')
            }
            writer.writerow(row)
    
    console.print(f"[green]Все результаты сохранены в: {output_file}[/green]")

def is_hidden_file(filepath):
    """Быстрая проверка скрытого файла"""
    try:
        if os.name == 'nt':
            attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
            return attrs != -1 and bool(attrs & 2)
        return False
    except:
        return False

def get_file_signature(filepath):
    """Быстрая проверка подписи"""
    try:
        cmd = f'powershell "Get-AuthenticodeSignature -FilePath \'{filepath}\' | Select-Object Status,SignerSubject"'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=5)
        if "IP Kayukin Gleb Anatolievich" in result.stdout:
            return "IP Kayukin Gleb Anatolievich"
        return None
    except:
        return None

def fast_search_custom_files():
    """Быстрый поиск по целевым местам"""
    found_files = []
    
    # ТОЛЬКО целевые места для быстрого поиска
    target_locations = get_target_locations()
    
    # Критерии поиска
    search_criteria = [
        {
            'name': 'Файлы с подписью IP Kayukin Gleb Anatolievich',
            'extensions': ['.exe'],
            'check_signature': True,
            'signature': 'IP Kayukin Gleb Anatolievich'
        },
        {
            'name': 'DeltaLoader.exe (11-14 MB)',
            'filename': 'DeltaLoader.exe',
            'size_range': (11*1024*1024, 14*1024*1024),
            'extensions': ['.exe']
        },
        {
            'name': 'Celestial.exe (17-19 MB)',
            'filename': 'Celestial.exe', 
            'size_range': (17*1024*1024, 19*1024*1024),
            'extensions': ['.exe']
        },
        {
            'name': 'NewLauncher.exe (180-190 MB)',
            'filename': 'NewLauncher.exe',
            'size_range': (180*1024*1024, 190*1024*1024),
            'extensions': ['.exe']
        },
        {
            'name': 'Exloader.exe (200-500 KB)',
            'filename': 'Exloader.exe',
            'size_range': (200*1024, 500*1024),
            'extensions': ['.exe']
        },
        {
            'name': 'Exloader_Installer.exe (20-40 MB)',
            'filename': 'Exloader_Installer.exe',
            'size_range': (20*1024*1024, 40*1024*1024),
            'extensions': ['.exe']
        }
    ]
    
    # Параллельный поиск по целевым местам
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = []
        for location in target_locations:
            future = executor.submit(scan_location_fast, location, search_criteria)
            futures.append(future)
        
        for future in as_completed(futures):
            try:
                results = future.result()
                found_files.extend(results)
            except Exception as e:
                continue
    
    # Быстрый поиск в AppData
    fast_search_appdata_jars(found_files)
    
    return found_files

def get_target_locations():
    """Возвращает только целевые места для быстрого поиска"""
    locations = []
    
    # Основные пользовательские места
    user_profile = os.environ.get('USERPROFILE', '')
    user_locations = [
        user_profile,
        os.path.join(user_profile, 'Desktop'),
        os.path.join(user_profile, 'Downloads'),
        os.path.join(user_profile, 'Documents'),
        os.path.join(user_profile, 'OneDrive'),
    ]
    
    for loc in user_locations:
        if os.path.exists(loc):
            locations.append(loc)
    
    # Temp папки
    temp_locations = [
        os.environ.get('TEMP', ''),
        os.environ.get('TMP', ''),
        'C:\\Temp',
        'C:\\Windows\\Temp',
    ]
    
    for loc in temp_locations:
        if loc and os.path.exists(loc):
            locations.append(loc)
    
    # Корни дисков (только быстрая проверка)
    for drive in 'CDEFGHIJKLMNOPQRSTUVWXYZ':
        drive_path = f"{drive}:\\"
        if os.path.exists(drive_path):
            # Добавляем только для быстрой проверки в корне
            locations.append(drive_path)
    
    return locations

def scan_location_fast(location, search_criteria):
    """Быстрое сканирование одной локации"""
    found_files = []
    excluded_dirs = {'system32', 'syswow64', 'windows', 'program files', 'program files (x86)'}
    
    try:
        for root, dirs, files in os.walk(location):
            # Быстро фильтруем директории
            dirs[:] = [d for d in dirs if d.lower() not in excluded_dirs and not d.startswith('.')]
            
            for file in files:
                file_path = os.path.join(root, file)
                file_lower = file.lower()
                
                try:
                    # Быстрая проверка размера
                    file_size = os.path.getsize(file_path)
                    
                    for criteria in search_criteria:
                        if not check_criteria_fast(file_lower, file_size, file_path, criteria):
                            continue
                            
                        found_files.append({
                            'path': file_path,
                            'name': file,
                            'size': file_size,
                            'reason': criteria['name'],
                            'hidden': is_hidden_file(file_path),
                            'type': 'CUSTOM_SEARCH',
                            'file_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                            'file_created': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                        })
                        console.print(f"[green]Найден: {file_path}[/green]")
                        
                except (OSError, PermissionError):
                    continue
                    
    except (OSError, PermissionError):
        pass
    
    return found_files

def check_criteria_fast(file_lower, file_size, file_path, criteria):
    """Быстрая проверка критериев"""
    # Проверка расширения
    if 'extensions' in criteria:
        ext_matches = any(file_lower.endswith(ext.lower()) for ext in criteria['extensions'])
        if not ext_matches:
            return False
    
    # Проверка имени файла
    if 'filename' in criteria:
        if file_lower != criteria['filename'].lower():
            return False
    
    # Проверка размера
    if 'size_range' in criteria:
        min_size, max_size = criteria['size_range']
        if not (min_size <= file_size <= max_size):
            return False
    
    # Проверка подписи (только если другие критерии совпали)
    if criteria.get('check_signature', False):
        signature = get_file_signature(file_path)
        if signature != criteria['signature']:
            return False
    
    return True

def fast_search_appdata_jars(found_files):
    """Быстрый поиск больших JAR файлов в AppData"""
    appdata_folders = ['Roaming', 'Local', 'LocalLow']
    user_profile = os.environ.get('USERPROFILE', '')
    
    for folder in appdata_folders:
        appdata_path = os.path.join(user_profile, 'AppData', folder)
        if not os.path.exists(appdata_path):
            continue
            
        try:
            # Быстрый поиск папок versions
            for root, dirs, files in os.walk(appdata_path):
                if 'versions' in [d.lower() for d in dirs]:
                    versions_dir = next((d for d in dirs if d.lower() == 'versions'), None)
                    if versions_dir:
                        versions_path = os.path.join(root, versions_dir)
                        # Быстро сканируем versions и подпапки
                        for version_root, version_dirs, version_files in os.walk(versions_path):
                            for file in version_files:
                                if file.lower().endswith('.jar'):
                                    file_path = os.path.join(version_root, file)
                                    try:
                                        file_size = os.path.getsize(file_path)
                                        if file_size > 30 * 1024 * 1024:  # >30MB
                                            found_files.append({
                                                'path': file_path,
                                                'name': file,
                                                'size': file_size,
                                                'reason': f'Большой JAR файл в AppData/{folder}/versions',
                                                'hidden': is_hidden_file(file_path),
                                                'type': 'APPDATA_JAR',
                                                'file_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                                                'file_created': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                                            })
                                            console.print(f"[green]Найден: {file_path}[/green]")
                                    except (OSError, PermissionError):
                                        continue
                # Ограничиваем глубину поиска для скорости
                if root.count(os.sep) - appdata_path.count(os.sep) > 3:
                    dirs.clear()
                    
        except (OSError, PermissionError):
            continue

def search_java_cheats():
    """Поиск Java читов (упрощенный)"""
    detector = FastJavaCheatDetector()
    
    try:
        results = detector.quick_scan()
        
        converted_results = []
        for result in results:
            converted_results.append({
                'path': result.get('file_path', ''),
                'name': os.path.basename(result.get('file_path', '')),
                'size': result.get('file_size', 0),
                'reason': 'Java чит файл',
                'hidden': is_hidden_file(result.get('file_path', '')),
                'type': 'JAVA_CHEAT',
                'file_modified': result.get('file_modified', ''),
                'file_created': result.get('file_created', '')
            })
        
        return converted_results
        
    except Exception as e:
        return []

def display_final_results(all_results):
    """Отображение финальных результатов"""
    if not all_results:
        console.print("[green]Подозрительные файлы не найдены[/green]")
        return
    
    console.print(f"\n[bold red]Всего найдено файлов: {len(all_results)}[/bold red]")
    
    table = Table(title="Общие результаты поиска")
    table.add_column("№", style="cyan")
    table.add_column("Тип", style="white")
    table.add_column("Файл", style="yellow")
    table.add_column("Размер", style="green")
    table.add_column("Причина", style="red")
    
    for i, file_info in enumerate(all_results, 1):
        size_mb = file_info['size'] / (1024 * 1024)
        table.add_row(
            str(i),
            file_info['type'],
            os.path.basename(file_info['path']),
            f"{size_mb:.2f} MB",
            file_info['reason']
        )
    
    console.print(table)
    
    if all_results:
        console.print("\n[bold cyan]Для открытия папки с файлом введите его номер (0 для выхода):[/bold cyan]")
        try:
            choice = Prompt.ask("Ваш выбор", choices=[str(i) for i in range(len(all_results) + 1)])
            if choice != "0":
                file_index = int(choice) - 1
                if 0 <= file_index < len(all_results):
                    file_path = all_results[file_index]['path']
                    folder_path = os.path.dirname(file_path)
                    console.print(f"[yellow]Открываю папку: {folder_path}[/yellow]")
                    os.startfile(folder_path)
        except Exception as e:
            console.print(f"[red]Ошибка: {e}[/red]")

# Упрощенный детектор Java читов
class FastJavaCheatDetector:
    def __init__(self):
        self.signature = b"net/java/i.class"
        self.min_size = 30 * 1024
        self.max_size = 10 * 1024 * 1024
        
    def quick_scan(self):
        """Быстрое сканирование только ключевых мест"""
        locations = [
            os.path.expanduser("~\\Downloads"),
            os.path.expanduser("~\\Desktop"),
            os.path.expanduser("~\\AppData\\Local\\Temp"),
        ]
        
        found_files = []
        for location in locations:
            if os.path.exists(location):
                found_files.extend(self.scan_location(location))
        
        return found_files
    
    def scan_location(self, location):
        """Сканирование одной локации"""
        found_files = []
        
        try:
            for root, dirs, files in os.walk(location):
                for file in files:
                    if not file.lower().endswith('.jar'):
                        continue
                        
                    file_path = os.path.join(root, file)
                    result = self.fast_scan_file(file_path)
                    if result:
                        found_files.append(result)
                        console.print(f"[green]Найден Java чит: {file_path}[/green]")
        except:
            pass
        
        return found_files
    
    def fast_scan_file(self, file_path):
        """Быстрая проверка файла"""
        try:
            file_size = os.path.getsize(file_path)
            if not (self.min_size <= file_size <= self.max_size):
                return None
            
            with open(file_path, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    if mm.find(self.signature) != -1:
                        return {
                            'file_path': file_path,
                            'file_size': file_size,
                            'file_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                            'file_created': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                        }
        except:
            pass
        
        return None

if __name__ == "__main__":
    main()