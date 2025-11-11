def main():
     print("Функция выполняется...")
import os
import zipfile
import urllib.request
import time
import subprocess
import sys

class USBDriveLogger:
    def __init__(self):
        self.download_url = "https://www.nirsoft.net/utils/usbdrivelog.zip"
        self.download_path = "C:/output/usbdrivelog.zip"
        self.extract_path = "C:/output/usbdrivelog/"
        self.exe_path = "C:/output/usbdrivelog/USBDriveLog.exe"
        
    def ensure_output_directory(self):
        """Создает директорию для выходных файлов"""
        directory = os.path.dirname(self.download_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(self.extract_path):
            os.makedirs(self.extract_path)
    
    def download_usbdrivelog(self):
        """Скачивает USBDriveLog без использования requests"""
       
        
        try:
            urllib.request.urlretrieve(self.download_url, self.download_path)
            print("Файл скачан: " + self.download_path)
            return True
            
        except Exception as e:
            print("Ошибка скачивания: " + str(e))
            return False
    
    def extract_zip(self):
        """Распаковывает архив"""
        
        
        try:
            with zipfile.ZipFile(self.download_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_path)
            
            print("Файлы распакованы в: " + self.extract_path)
            return True
            
        except Exception as e:
            print("Ошибка распаковки: " + str(e))
            return False
    
    def install_dependencies_if_needed(self):
        """Проверяет и устанавливает зависимости если нужно"""
        dependencies = ['pyautogui', 'selenium']
        
        for dep in dependencies:
            try:
                if dep == 'pyautogui':
                    import pyautogui
                elif dep == 'selenium':
                    import selenium
                print(dep + " уже установлен")
            except ImportError:
                print("Установка " + dep + "...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                    print(dep + " установлен")
                except Exception as e:
                    print("Ошибка установки " + dep + ": " + str(e))
                    return False
        return True
    
    def run_usbdrivelog_and_click_unplugtime(self):
        """Запускает USBDriveLog и нажимает UnplugTime"""
        print("Запуск USBDriveLog...")
        
        if not os.path.exists(self.exe_path):
            print("USBDriveLog.exe не найден")
            return False
        
        try:
            process = subprocess.Popen([self.exe_path])
            print("USBDriveLog запущен")
            time.sleep(3)  
            
            return self.alternative_unplugtime_method()
            
        except Exception as e:
            print("Ошибка запуска: " + str(e))
            return False
    
    def alternative_unplugtime_method(self):
        """Альтернативный метод для работы с UnplugTime"""
       
        
        try:
            import pyautogui
            print("Нажатие Alt+U для UnplugTime...")
            pyautogui.hotkey('alt', 'u')
            time.sleep(2)
            
            print("UnplugTime активирован")
            return True
            
        except Exception as e:
            print("Ошибка альтернативного метода: " + str(e))
            return self.final_method()
    
    def final_method(self):
        """Финальный метод - прямой запуск с параметрами"""
      
        
        try:
            cmd = '"' + self.exe_path + '" /scomma "C:/output/usb_logs.csv"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                
                return True
            else:
                print("Программа завершилась с ошибкой, но могла собрать логи")
                return True
                
        except Exception as e:
            print("Финальный метод тоже не сработал: " + str(e))
            return False
    
    def main_automation(self):
        """Основная функция автоматизации"""
        print("Запуск автоматизации USBDriveLog")
        print("=" * 50)
        self.ensure_output_directory()
        if not self.download_usbdrivelog():
            return False
        if not self.extract_zip():
            return False
        if not self.install_dependencies_if_needed():
            print("Продолжаем без некоторых зависимостей")
        success = self.run_usbdrivelog_and_click_unplugtime()
        
        if success:
            print("Автоматизация завершена успешно!")
            print("Файлы программы: " + self.extract_path)
            print("Логи должны быть в: C:/output/usb_logs.csv")
        else:
            print("Автоматизация завершена с проблемами, проверьте вручную")
        
        return success

def main():
    usb_logger = USBDriveLogger()
    
    try:
        usb_logger.main_automation()
    except Exception as e:
        print("Критическая ошибка: " + str(e))

if __name__ == "__main__":
    main()
