import os
import csv
import psutil
import time
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import mmap

class JavaCheatFileDetector:
    def __init__(self):
        self.output_file = "C:/output/java_cheat_detection.csv"
        self.signature = b"net/java/i.class"
        self.min_size = 30 * 1024  # 30KB
        self.max_size = 10 * 1024 * 1024  # 10MB
        self.found_files = []
        self.scan_complete = False
        self.files_scanned = 0
        
    def ensure_output_directory(self):
        directory = os.path.dirname(self.output_file)
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def get_suspicious_locations(self):
        """Возвращает список подозрительных мест для сканирования"""
        locations = []
        
        # Пользовательские папки
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
        
        # Системные временные папки
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
            # Быстрая проверка размера
            file_size = os.path.getsize(file_path)
            if not (self.min_size <= file_size <= self.max_size):
                return None
            
            # Используем memory mapping для быстрого поиска
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
                        print(f"🚨 Найден: {entry.path}")
                        print(f"   📅 Изменен: {result['file_modified']}")
                elif entry.is_dir():
                    # Пропускаем системные папки для скорости
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
        
        start_time = time.time()
        self.parallel_scan_locations(locations)
        scan_time = time.time() - start_time
        
        print(f"\n📊 Просканировано файлов: {self.files_scanned} (за {scan_time:.1f} сек)")
        return self.found_files
    
    def monitor_java_processes_fast(self, duration=180):
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
        
        # Быстрый поиск целевых файлов в командной строке
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
                        
                        print(f"🚨 Найден в процессе {pid}: {target}")
                        print(f"   📅 Изменен: {result['file_modified']}")
                        self.found_files.append(result)
                    break
    
    def full_scan_fast(self):
        """Быстрое полное сканирование"""
        # Запускаем сканирование файлов в отдельном потоке
        scan_thread = threading.Thread(target=self.quick_scan_suspicious_locations)
        scan_thread.start()
        
        # Запускаем мониторинг процессов
        self.monitor_java_processes_fast(180)
        
        # Ждем завершения сканирования
        scan_thread.join()
        self.scan_complete = True
        
        return self.found_files
    
    def save_results_to_csv(self, results):
        """Сохраняет результаты в CSV"""
        self.ensure_output_directory()
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'detection_type', 'found_time', 'file_path', 'file_size', 
                'file_extension', 'file_modified', 'file_created', 
                'process_pid', 'process_cmdline', 'process_start_time'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                row = {
                    'detection_type': result.get('detection_type', 'UNKNOWN'),
                    'found_time': result.get('found_time', ''),
                    'file_path': result.get('file_path', ''),
                    'file_size': result.get('file_size', 0),
                    'file_extension': result.get('file_extension', ''),
                    'file_modified': result.get('file_modified', ''),
                    'file_created': result.get('file_created', ''),
                    'process_pid': result.get('process_pid', ''),
                    'process_cmdline': result.get('process_cmdline', ''),
                    'process_start_time': result.get('process_start_time', '')
                }
                writer.writerow(row)
        
        print(f"💾 Результаты сохранены в: {self.output_file}")
    
    def print_summary(self, results):
        """Выводит краткую сводку"""
        if results:
            print(f"\n🎯 Найдено файлов: {len(results)}")
        else:
            print(f"\n✅ Файлы не найдены")

def main():
    detector = JavaCheatFileDetector()
    
    try:
        print("🔍 Сканирование...")
        
        start_time = time.time()
        results = detector.full_scan_fast()
        total_time = time.time() - start_time
        
        detector.save_results_to_csv(results)
        detector.print_summary(results)
        print(f"⏱️ Общее время: {total_time:.1f} сек")
        
    except KeyboardInterrupt:
        print("\n⏹️ Прервано")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
    