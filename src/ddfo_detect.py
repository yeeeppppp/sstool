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

console = Console()

def main():
    """Поиск подозрительных файлов и Java читов"""
    console.print("=== Поиск подозрительных файлов и Java читов ===")
    
    all_results = []
    
    # Сначала выполняем поиск по твоим критериям
    custom_results = search_custom_files()
    all_results.extend(custom_results)
    
    # Затем запускаем поиск Java читов
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

# Функции для поиска по твоим критериям
def is_hidden_file(filepath):
    """Проверяет, является ли файл скрытым"""
    try:
        if os.name == 'nt':  # Windows
            attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
            return attrs != -1 and bool(attrs & 2)  # FILE_ATTRIBUTE_HIDDEN
        else:
            return os.path.basename(filepath).startswith('.')
    except:
        return False

def get_file_signature(filepath):
    """Получает информацию о цифровой подписи файла"""
    try:
        cmd = f'powershell "Get-AuthenticodeSignature -FilePath \'{filepath}\' | Format-List"'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        output = result.stdout
        
        if "IP Kayukin Gleb Anatolievich" in output:
            return "IP Kayukin Gleb Anatolievich"
        return None
    except:
        return None

def search_custom_files():
    """Поиск файлов по заданным критериям"""
    found_files = []
    excluded_dirs = {'system32', 'syswow64', 'windows'}
    
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
    
    # Поиск по дискам
    drives = []
    for drive_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        drive_path = f"{drive_letter}:\\"
        if os.path.exists(drive_path):
            drives.append(drive_path)
    
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            # Пропускаем системные папки
            dirs[:] = [d for d in dirs if d.lower() not in excluded_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                file_lower = file.lower()
                
                try:
                    file_size = os.path.getsize(file_path)
                    
                    # Проверяем все критерии
                    for criteria in search_criteria:
                        match = False
                        reason = criteria['name']
                        
                        # Проверка по расширению
                        if 'extensions' in criteria:
                            ext_matches = any(file_lower.endswith(ext.lower()) for ext in criteria['extensions'])
                            if not ext_matches:
                                continue
                        
                        # Проверка по имени файла
                        if 'filename' in criteria:
                            if file_lower != criteria['filename'].lower():
                                continue
                            match = True
                        
                        # Проверка по размеру
                        if 'size_range' in criteria and match:
                            min_size, max_size = criteria['size_range']
                            if not (min_size <= file_size <= max_size):
                                continue
                        
                        # Проверка цифровой подписи
                        if criteria.get('check_signature', False):
                            signature = get_file_signature(file_path)
                            if signature == criteria['signature']:
                                match = True
                                reason = f"Цифровая подпись: {signature}"
                        
                        if match:
                            found_files.append({
                                'path': file_path,
                                'name': file,
                                'size': file_size,
                                'reason': reason,
                                'hidden': is_hidden_file(file_path),
                                'type': 'CUSTOM_SEARCH',
                                'file_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                                'file_created': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                            })
                            console.print(f"[green]Найден: {file_path}[/green]")
                            
                except (OSError, PermissionError):
                    continue
    
    # Поиск в AppData
    search_appdata_jars(found_files)
    
    return found_files

def search_appdata_jars(found_files):
    """Поиск больших JAR файлов в AppData (включая подпапки versions)"""
    appdata_folders = ['Roaming', 'Local', 'LocalLow']
    user_profile = os.environ.get('USERPROFILE', '')
    
    for folder in appdata_folders:
        appdata_path = os.path.join(user_profile, 'AppData', folder)
        if not os.path.exists(appdata_path):
            continue
            
        try:
            for root, dirs, files in os.walk(appdata_path):
                # Ищем папку versions и ее подпапки
                if 'versions' in [d.lower() for d in dirs]:
                    versions_dir = next((d for d in dirs if d.lower() == 'versions'), None)
                    if versions_dir:
                        versions_path = os.path.join(root, versions_dir)
                        # Сканируем саму папку versions и все ее подпапки
                        for version_root, version_dirs, version_files in os.walk(versions_path):
                            for file in version_files:
                                if file.lower().endswith('.jar'):
                                    file_path = os.path.join(version_root, file)
                                    try:
                                        file_size = os.path.getsize(file_path)
                                        # Файлы больше 30MB
                                        if file_size > 30 * 1024 * 1024:
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
        except (OSError, PermissionError):
            continue

def search_java_cheats():
    """Поиск Java читов"""
    detector = JavaCheatFileDetector()
    
    try:
        results = detector.full_scan_fast()
        
        # Конвертируем результаты в общий формат
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
        console.print(f"[red]Ошибка при поиске Java читов: {e}[/red]")
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
    
    # Возможность открыть папку с файлом
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

# Класс для поиска Java читов
class JavaCheatFileDetector:
    def __init__(self):
        self.signature = b"net/java/i.class"
        self.min_size = 30 * 1024  # 30KB
        self.max_size = 10 * 1024 * 1024  # 10MB
        self.found_files = []
        self.scan_complete = False
        self.files_scanned = 0
        
    def get_suspicious_locations(self):
        """Возвращает список подозрительных мест для сканирования"""
        locations = []
        
        user_folders = [
            "Downloads",
            "Desktop", 
            "Documents",
            "OneDrive\\Downloads",
            "OneDrive\\Desktop", 
            "OneDrive\\Documents",
            "AppData\\Local\\Temp",
            "AppData\\Local",
            "AppData\\Roaming"
        ]
        
        for folder in user_folders:
            path = os.path.expanduser(f"~\\{folder}")
            if os.path.exists(path):
                locations.append(path)
        
        system_temp_folders = [
            "C:\\Temp",
            "C:\\Windows\\Temp",
            os.getenv('TEMP', ''),
            os.getenv('TMP', ''),
        ]
        
        for folder in system_temp_folders:
            if folder and os.path.exists(folder):
                locations.append(folder)
        
        return locations
    
    def fast_scan_file(self, file_path):
        """Быстрая проверка файла на соответствие сигнатуре"""
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
                            'file_extension': os.path.splitext(file_path)[1].lower(),
                            'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'file_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                            'file_created': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                            'detection_type': 'FILE_SCAN'
                        }
                    
        except (PermissionError, FileNotFoundError, OSError, ValueError):
            pass
        
        return None
    
    def scan_directory_fast(self, directory):
        """Быстрое рекурсивное сканирование директории"""
        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    self.files_scanned += 1
                    result = self.fast_scan_file(entry.path)
                    if result:
                        self.found_files.append(result)
                        console.print(f"[green]Найден Java чит: {entry.path}[/green]")
                elif entry.is_dir():
                    if not entry.name.startswith(('.', '$', 'Windows', 'System32')):
                        self.scan_directory_fast(entry.path)
        except (PermissionError, OSError):
            pass
    
    def parallel_scan_locations(self, locations):
        """Параллельное сканирование локаций"""
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(self.scan_directory_fast, location): location for location in locations}
            
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    pass
    
    def quick_scan_suspicious_locations(self):
        """Быстрое сканирование подозрительных мест"""
        locations = self.get_suspicious_locations()
        self.parallel_scan_locations(locations)
        return self.found_files
    
    def monitor_java_processes_fast(self, duration=60):
        """Быстрый мониторинг Java процессов"""
        known_processes = set()
        start_time = time.time()
        
        while time.time() - start_time < duration and not self.scan_complete:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'exe', 'create_time']):
                try:
                    proc_name = proc.info['name'] or ''
                    if proc_name.lower() in ['java.exe', 'javaw.exe']:
                        proc_id = f"{proc.info['pid']}_{proc.info['exe']}"
                        
                        if proc_id not in known_processes:
                            known_processes.add(proc_id)
                            self.analyze_java_process_fast(proc.info['pid'], proc.info['cmdline'] or [], proc.info['create_time'])
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            time.sleep(1)
    
    def analyze_java_process_fast(self, pid, cmdline, create_time):
        """Быстрый анализ Java процесса"""
        if not cmdline:
            return
        
        for i, arg in enumerate(cmdline):
            if (arg == '-jar' and i + 1 < len(cmdline)) or (len(arg) > 3 and '.' in arg and not arg.startswith('-')):
                target = cmdline[i + 1] if arg == '-jar' else arg
                if os.path.exists(target):
                    result = self.fast_scan_file(target)
                    if result:
                        result['detection_type'] = 'PROCESS_MONITOR'
                        result['process_pid'] = pid
                        result['process_cmdline'] = ' '.join(cmdline[:3]) + '...'
                        result['process_start_time'] = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
                        
                        console.print(f"[green]Найден в процессе {pid}: {target}[/green]")
                        self.found_files.append(result)
                    break
    
    def full_scan_fast(self):
        """Быстрое полное сканирование"""
        scan_thread = threading.Thread(target=self.quick_scan_suspicious_locations)
        scan_thread.start()
        
        self.monitor_java_processes_fast(60)
        
        scan_thread.join()
        self.scan_complete = True
        
        return self.found_files

if __name__ == "__main__":
    main()