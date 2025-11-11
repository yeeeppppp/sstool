from rich.console import Console
import os
import zipfile
import urllib.request
import subprocess
import tempfile
import re

console = Console()

def main():
    """Анализ модификации файлов"""
    console.print("=== Анализ модификации ===")
    scan_loop()

SIGNATURES = {
    "examplemod": "Возможно софт",
    "neat": "Возможно софт",
    "tapemouse": "Возможно софт",
    "creativecore": "Возможно софт",
    "minecraftoptimization": "Возможно софт",
    "smoothboot": "Возможно софт",
    "hitboxes": "Возможно софт",
    "bypass": "Возможно софт",
    "goodman": "Возможно софт",
    "customhitboxes": "Возможно софт",
    "killyourfamily": "Возможно софт",
    "opaclient": "Возможно софт",
    "fabricmc": "Возможно софт",
    "nohurtcam": "Возможно софт",
    "fpsboost": "Возможно софт",
    "fpsreducer": "Возможно софт",
    "autojump": "Возможно софт",
    "triggerbot": "Возможно софт",
    "Start": "Возможно софт",
    "ALLATORI": "Возможно софт",
    "bushroot": "Возможно софт",
    "Creator": "Доп проверка через Luyten",
    "cmdcoders": "Возможно софт",
    "@rejavastealbot": "Возможно софт",
    "freecam": "Возможно софт",
    "modd": "Возможно софт",
    "ichunutil": "Возможно софт",
    "wao": "Возможно софт",
}

FORGE_SIGS = ["func_174826_a","AxisAlignedBB","func_226277_ct_()",
              "func_226278_cu_()","func_226281_cx_()","func_174813_aQ",
              "func_213302_cg"]
FABRIC_SIGS = ["method_5829","class_238","method_23317","method_23321","method_5857"]

LABYMOD_SIGS = [
    "player.cD()", "player.cE()", "player.cH()",
    "target.cD()", "target.cE()", "target.cH()",
    "cD()", "cE()", "cH()",  
    "dzm", "dcl", "dck", "aqa", "bfw",  
    "onTick", "TickEvent", "autoCritEnabled", "getPhase", "POST"
]

LUYTEN_URL = "https://github.com/deathmarine/Luyten/releases/download/v0.5.4_Rebuilt_with_Latest_depenencies/luyten-0.5.4.exe"
LUYTEN_FILENAME = "luyten-0.5.4.exe"

def download_luyten():
    """Скачивает Luyten если не установлен"""
    if not os.path.exists(LUYTEN_FILENAME):
        console.print("Скачивание Luyten...")
        try:
            urllib.request.urlretrieve(LUYTEN_URL, LUYTEN_FILENAME)
            console.print("Luyten скачан успешно")
            return True
        except Exception as e:
            console.print(f"Ошибка скачивания Luyten: {e}")
            return False
    return True

def open_in_luyten(jar_path, class_file=None):
    """Открывает JAR файл в Luyten, с фокусом на конкретный CLASS файл"""
    if download_luyten():
        try:
            if class_file:
                temp_dir = tempfile.gettempdir()
                temp_file = os.path.join(temp_dir, "luyten_open.txt")
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(f"{jar_path}\n{class_file}")
                
                subprocess.run([LUYTEN_FILENAME, jar_path], check=True)
            else:
                subprocess.run([LUYTEN_FILENAME, jar_path], check=True)
            return True
        except Exception as e:
            console.print(f"Ошибка запуска Luyten: {e}")
    return False

def find_jars(path):
    if os.path.isfile(path) and path.lower().endswith(".jar"):
        return [path]
    jars = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.lower().endswith(".jar"):
                jars.append(os.path.join(root, f))
    return jars

def extract_strings_from_binary(data):
    """Извлекает читаемые строки из бинарных данных CLASS файла"""
    strings = []
    pattern = b'[\x20-\x7E]{4,}'
    matches = re.findall(pattern, data)
    for match in matches:
        try:
            string = match.decode('ascii', errors='ignore')
            if len(string) >= 4:  
                strings.append(string)
        except:
            continue
    return strings

def scan_class_content(data):
    """Ищет сигнатуры в CLASS файле"""
    detected_sigs = set()
    
    all_sigs = (list(SIGNATURES.keys()) + FORGE_SIGS + FABRIC_SIGS + LABYMOD_SIGS)
    
    for sig in all_sigs:
        if sig.encode('utf-8') in data:
            detected_sigs.add(sig)
    extracted_strings = extract_strings_from_binary(data)
    for string in extracted_strings:
        for sig in all_sigs:
            if sig in string:
                detected_sigs.add(sig)
    try:
        text_data = data.decode('utf-8', errors='ignore')
        for sig in all_sigs:
            if sig in text_data:
                detected_sigs.add(sig)
    except:
        pass
    try:
        text_data_utf16 = data.decode('utf-16', errors='ignore')
        for sig in all_sigs:
            if sig in text_data_utf16:
                detected_sigs.add(sig)
    except:
        pass
    
    return detected_sigs

def scan_jar(jar_path):
    detected_classes = {}
    detected_all = set()  
    try:
        with zipfile.ZipFile(jar_path, "r") as z:
            for name in z.namelist():
                if not name.endswith(".class"):
                    continue
                try:
                    data = z.read(name)
                    sigs = scan_class_content(data)
                    if sigs:
                        detected_classes[name] = sigs
                        detected_all.update(sigs)
                        
                except Exception as e:
                    continue
                        
        return detected_classes, detected_all
    except zipfile.BadZipFile:
        console.print(f"{os.path.basename(jar_path)} - не архив")
        return {}, set()
    except Exception as e:
        console.print(f"Ошибка при сканировании {os.path.basename(jar_path)}: {e}")
        return {}, set()

def scan_loop():
    while True:
        console.print("\n[bold cyan]Введите путь к JAR файлу или папке (или 'exit' для выхода):[/bold cyan]")
        path = input("Путь: ").strip('"')
        
        if path.lower() == "exit":
            break
            
        if not os.path.exists(path):
            console.print("[red]Путь не найден[/red]")
            continue

        jars = find_jars(path)
        if not jars:
            console.print("[yellow]JAR-файлы не найдены[/yellow]")
            continue

        found_any = False
        suspicious_files_count = 0
        clean_files = []
        suspicious_files_data = []
        
        console.print(f"[bold]Сканирование {len(jars)} файлов...[/bold]")
        
        for jar in jars:
            detected_classes, detected_all = scan_jar(jar)
            jar_name = os.path.basename(jar)
            
            if detected_all:
                found_any = True
                suspicious_files_count += 1
                suspicious_files_data.append((jar, jar_name, detected_classes))
                console.print(f"[yellow]{jar_name} - найдено сигнатур:[/yellow]")
                labymod_sigs = [sig for sig in detected_all if any(lm_sig in sig for lm_sig in ['cD()', 'cE()', 'cH()', 'dzm', 'dcl', 'dck', 'aqa', 'bfw'])]
                forge_sigs = [sig for sig in detected_all if sig in FORGE_SIGS]
                fabric_sigs = [sig for sig in detected_all if sig in FABRIC_SIGS]
                other_sigs = detected_all - set(labymod_sigs) - set(forge_sigs) - set(fabric_sigs)
                
                if labymod_sigs:
                    console.print(f"  [red]LabyMod: {', '.join(labymod_sigs)}[/red]")
                if forge_sigs:
                    console.print(f"  [red]Forge: {', '.join(forge_sigs)}[/red]")
                if fabric_sigs:
                    console.print(f"  [red]Fabric: {', '.join(fabric_sigs)}[/red]")
                if other_sigs:
                    console.print(f"  [red]Другие: {', '.join(other_sigs)}[/red]")
                    
                if detected_classes:
                    console.print("  [yellow]Подозрительные классы:[/yellow]")
                    for cls, sigs in detected_classes.items():
                        console.print(f"    {cls}: {', '.join(list(sigs)[:5])}")
            else:
                clean_files.append(jar_name)
                console.print(f"[green]{jar_name} - чистый[/green]")
                
        console.print("\n" + "="*50)
        
        if found_any:
            console.print(f"[bold red]Найдено подозрительных файлов: {suspicious_files_count}[/bold red]")
            console.print("\n[bold]Подозрительные файлы:[/bold]")
            
            for i, (jar_path, jar_name, detected_classes) in enumerate(suspicious_files_data, 1):
                console.print(f"  {i}. {jar_name}")
                if detected_classes:
                    class_list = list(detected_classes.keys())
                    if len(class_list) > 3:
                        console.print(f"     Классы: {', '.join(class_list[:3])} ... (еще {len(class_list)-3})")
                    else:
                        console.print(f"     Классы: {', '.join(class_list)}")
            
            console.print("\n[bold cyan]Для декомпиляции выберите номер файла (0 для выхода):[/bold cyan]")
            try:
                choice = input("Ваш выбор: ").strip()
                if choice == "0":
                    continue
                
                file_index = int(choice) - 1
                if 0 <= file_index < len(suspicious_files_data):
                    selected_jar_path, selected_jar_name, detected_classes = suspicious_files_data[file_index]
                    
                    if detected_classes:
                        console.print(f"\n[bold]Подозрительные классы в {selected_jar_name}:[/bold]")
                        class_list = list(detected_classes.keys())
                        for j, class_name in enumerate(class_list, 1):
                            sigs = detected_classes[class_name]
                            console.print(f"  {j}. {class_name} ({', '.join(list(sigs)[:3])})")
                        
                        console.print("  [cyan]Выберите номер класса для открытия (0 для всего JAR):[/cyan]")
                        class_choice = input("Ваш выбор: ").strip()
                        
                        if class_choice != "0":
                            try:
                                class_index = int(class_choice) - 1
                                if 0 <= class_index < len(class_list):
                                    selected_class = class_list[class_index]
                                    console.print(f"[yellow]Открытие {selected_jar_name} -> {selected_class} в Luyten...[/yellow]")
                                    open_in_luyten(selected_jar_path, selected_class)
                                else:
                                    console.print("[red]Неверный номер класса[/red]")
                            except ValueError:
                                console.print("[yellow]Открытие всего JAR файла...[/yellow]")
                                open_in_luyten(selected_jar_path)
                        else:
                            console.print(f"[yellow]Открытие {selected_jar_name} в Luyten...[/yellow]")
                            open_in_luyten(selected_jar_path)
                    else:
                        console.print(f"[yellow]Открытие {selected_jar_name} в Luyten...[/yellow]")
                        open_in_luyten(selected_jar_path)
                        
                else:
                    console.print("[red]Неверный номер[/red]")
                    
            except ValueError:
                console.print("[red]Введите число[/red]")
            except Exception as e:
                console.print(f"[red]Ошибка: {e}[/red]")
                
        else:
            console.print("[green]Подозрительные файлы не найдены[/green]")
        
        if clean_files:
            console.print(f"\n[bold green]Чистые файлы ({len(clean_files)}):[/bold green]")
            for file in clean_files:
                console.print(f"  {file}")
        else:
            console.print("\n[green]Чистые файлы: нет[/green]")

        console.print(f"\n[bold]Итог: {suspicious_files_count} подозрительных, {len(clean_files)} чистых[/bold]")

if __name__ == "__main__":
    main()