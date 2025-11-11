def main():
     print("Функция выполняется...")
import os
import re
import csv
from datetime import datetime

class DLLAnalyzer:
    def __init__(self):
       
        self.keywords_general = [
            "doomsday",
            "io/github/lefraudeur/gui/clickgui/ClickGUI.class",
            "io/github/lefraudeur/gui/clickgui/widgets/CheckBox.class",
            "(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invok",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}",
            "AxisAlignedBB"
        ]
        
        
        self.keyword_special = "glPushClientAttrib"
        
       
        self.general_min_size = 30 * 1024    
        self.general_max_size = 6000 * 1024 
        
        self.special_min_size = 460 * 1024  
        self.special_max_size = 480 * 1024   
        
        self.found_dlls_general = [] 
        self.found_dlls_special = []  
        
       
        self.csv_general = "C:/output/general_dlls.csv"
        self.csv_special = "C:/output/special_dlls.csv"
        self.csv_combined = "C:/output/all_dlls.csv"
        
      
        self.exclude_folders = [
            'System32', 'SysWOW64', 'winsxs', 'WinSxS', 
            '$Recycle.Bin', 'System Volume Information', 'Recovery',
            'Windows\\System32', 'Windows\\SysWOW64', 'Windows\\winsxs',
            'Windows.old', 'Boot', 'Prefetch', 'Logs', 'Cache',
            'Microsoft', 'AppData\\Local\\Microsoft', 'ProgramData\\Microsoft',
            'Windows\\Logs', 'Windows\\CbsTemp', 'Windows\\servicing'
        ]
        
    def ensure_output_directory(self):
        """Создает директорию для выходных файлов"""
        directory = os.path.dirname(self.csv_general)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
    def get_all_drives(self):
        """Получает список всех дисков в системе"""
        drives = []
        for drive in range(65, 91):  
            drive_letter = chr(drive) + ":\\"
            if os.path.exists(drive_letter):
                drives.append(drive_letter)
        return drives
    
    def should_skip_folder(self, folder_path):
        """Проверяет, нужно ли пропустить папку"""
        folder_path_lower = folder_path.lower()
        
      
        for exclude in self.exclude_folders:
            if exclude.lower() in folder_path_lower:
                return True
            
        return False
    
    def is_in_general_range(self, file_size):
        """Проверяет, находится ли размер в общем диапазоне 30KB-6000KB"""
        return self.general_min_size <= file_size <= self.general_max_size
    
    def is_in_special_range(self, file_size):
        """Проверяет, находится ли размер в специальном диапазоне 460KB-480KB"""
        return self.special_min_size <= file_size <= self.special_max_size
    
    def analyze_dll_general(self, dll_path):
        """Анализ DLL файла для общего поиска"""
        try:
            file_size = os.path.getsize(dll_path)
            
          
            if not self.is_in_general_range(file_size):
                return None
            
            
            read_size = min(file_size, 4 * 1024 * 1024)
            with open(dll_path, 'rb') as f:
                content = f.read(read_size)
                
            
            found_keywords = []
            
            for keyword in self.keywords_general:
                if keyword.encode('utf-8') in content:
                    found_keywords.append(keyword)
            
            
            if found_keywords:
                return {
                    'path': dll_path,
                    'keywords': found_keywords,
                    'size': file_size,
                    'size_kb': file_size // 1024,
                    'modified': os.path.getmtime(dll_path),
                    'search_type': 'general'
                }
                    
        except Exception as e:
            pass
        
        return None
    
    def analyze_dll_special(self, dll_path):
        """Анализ DLL файла для специального поиска glPushClientAttrib"""
        try:
            file_size = os.path.getsize(dll_path)
            
        
            if not self.is_in_special_range(file_size):
                return None
            
           
            read_size = min(file_size, 4 * 1024 * 1024)
            with open(dll_path, 'rb') as f:
                content = f.read(read_size)
                
          
            if self.keyword_special.encode('utf-8') in content:
                return {
                    'path': dll_path,
                    'keywords': [self.keyword_special],
                    'size': file_size,
                    'size_kb': file_size // 1024,
                    'modified': os.path.getmtime(dll_path),
                    'search_type': 'special'
                }
                    
        except Exception as e:
            pass
        
        return None
    
    def search_dlls(self):
        """Поиск DLL файлов по всем критериям"""
        search_paths = self.get_all_drives()
        
        print("ПОИСК DLL ФАЙЛОВ") 
        total_scanned = 0
        general_found = 0
        special_found = 0
        
        for path in search_paths:
            print(f"Сканирование диска: {path}")
            
            try:
                for root, dirs, files in os.walk(path):
             
                    dirs[:] = [d for d in dirs if not self.should_skip_folder(os.path.join(root, d))]
                    
                    for file in files:
                        if file.lower().endswith('.dll'):
                            dll_path = os.path.join(root, file)
                            total_scanned += 1
                            
                            if total_scanned % 1000 == 0:
                                print(f"Просканировано DLL файлов: {total_scanned}")
                            
                    
                            general_result = self.analyze_dll_general(dll_path)
                            if general_result:
                                self.found_dlls_general.append(general_result)
                                general_found += 1
                                print(f"[ОБЩИЙ] НАЙДЕНА DLL: {dll_path}")
                                print(f"  Размер: {general_result['size_kb']} KB")
                                print(f"  Найдено ключевых слов: {len(general_result['keywords'])}")
                            
                            special_result = self.analyze_dll_special(dll_path)
                            if special_result:
                                self.found_dlls_special.append(special_result)
                                special_found += 1
                                print(f"[СПЕЦИАЛЬНЫЙ] НАЙДЕНА DLL: {dll_path}")
                                print(f"  Размер: {special_result['size_kb']} KB")
                            
            except Exception as e:
                continue
        
        print(f"\nИтоги сканирования:")
        print(f"Всего просканировано DLL файлов: {total_scanned}")
        print(f"Найдено в общем поиске: {general_found}")
        print(f"Найдено в специальном поиске: {special_found}")
        
        return general_found, special_found
    
    def save_to_csv(self):
        """Сохраняет все найденные DLL в CSV файлы"""
        self.ensure_output_directory()
        
        if self.found_dlls_general:
            with open(self.csv_general, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['path', 'size_kb', 'keywords', 'modified', 'search_type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for dll in self.found_dlls_general:
                    writer.writerow({
                        'path': dll['path'],
                        'size_kb': dll['size_kb'],
                        'keywords': '; '.join(dll['keywords']),
                        'modified': dll['modified'],
                        'search_type': dll['search_type']
                    })
            print(f"Общие результаты сохранены в: {self.csv_general}")
        if self.found_dlls_special:
            with open(self.csv_special, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['path', 'size_kb', 'keywords', 'modified', 'search_type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for dll in self.found_dlls_special:
                    writer.writerow({
                        'path': dll['path'],
                        'size_kb': dll['size_kb'],
                        'keywords': '; '.join(dll['keywords']),
                        'modified': dll['modified'],
                        'search_type': dll['search_type']
                    })
            print(f"Специальные результаты сохранены в: {self.csv_special}")
        all_dlls = self.found_dlls_general + self.found_dlls_special
        if all_dlls:
            with open(self.csv_combined, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['path', 'size_kb', 'keywords', 'modified', 'search_type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for dll in all_dlls:
                    writer.writerow({
                        'path': dll['path'],
                        'size_kb': dll['size_kb'],
                        'keywords': '; '.join(dll['keywords']),
                        'modified': dll['modified'],
                        'search_type': dll['search_type']
                    })
            print(f"Объединенные результаты сохранены в: {self.csv_combined}")
    
    def display_results(self):
        """Отображает все найденные DLL в CMD"""
        all_dlls = self.found_dlls_general + self.found_dlls_special
        
        if not all_dlls:
            print("DLL файлы не найдены.")
            return
        
        print("\n" + "=" * 100)
        print("ВСЕ НАЙДЕННЫЕ DLL ФАЙЛЫ:")
        print("=" * 100)
        
        if self.found_dlls_general:
            
            for i, dll_info in enumerate(self.found_dlls_general, 1):
                print(f"{i}. {dll_info['path']}")
                print(f"   Размер: {dll_info['size_kb']} KB")
                print(f"   Найдено ключевых слов: {len(dll_info['keywords'])}")
                print()
        
        if self.found_dlls_special:
           
            start_idx = len(self.found_dlls_general) + 1
            for i, dll_info in enumerate(self.found_dlls_special, start_idx):
                print(f"{i}. {dll_info['path']}")
                print(f"   Размер: {dll_info['size_kb']} KB")
                print()

def main():
    analyzer = DLLAnalyzer()
    
    print("Анализатор DLL файлов - Расширенный поиск")
    print("Включает общий поиск и специальный поиск")
    print("=" * 80)
    general_count, special_count = analyzer.search_dlls()
    if analyzer.found_dlls_general or analyzer.found_dlls_special:
        analyzer.save_to_csv()
    analyzer.display_results()
    
    print(f"\nФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
    print(f"Общий поиск: {general_count} файлов")
    print(f"Специальный поиск: {special_count} файлов")
    print(f"Всего найдено: {general_count + special_count} файлов")
    
    if general_count + special_count > 0:
        print(f"\nРезультаты сохранены в:")
        print(f"- {analyzer.csv_general} (общие)")
        print(f"- {analyzer.csv_special} (специальные)")
        print(f"- {analyzer.csv_combined} (все результаты)")

if __name__ == "__main__":
    main()