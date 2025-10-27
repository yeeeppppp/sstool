import subprocess
import os
import csv
import datetime

def get_current_user_sid():
    command = 'powershell -Command "[System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value"'
    sid = subprocess.check_output(command, shell=True).decode().strip()
    return sid

def get_files_in_recycle_bin(recycle_path):
    if not os.path.exists(recycle_path):
        print(f"Папка по пути {recycle_path} не найдена.")
        return []

    files_data = []
    for root, dirs, files in os.walk(recycle_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                stat = os.stat(file_path)
                # Получение времени создания или последнего изменения
                ctime = datetime.datetime.fromtimestamp(stat.st_ctime)
                mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
                files_data.append({
                    'file_name': filename,
                    'full_path': file_path,
                    'created_time': ctime.strftime('%Y-%m-%d %H:%M:%S'),
                    'modified_time': mtime.strftime('%Y-%m-%d %H:%M:%S')
                })
            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {e}")
    return files_data

def save_to_csv(data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file_name', 'full_path', 'created_time', 'modified_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    user_sid = get_current_user_sid()
    recycle_path = fr"C:\$Recycle.Bin\{user_sid}"

    files = get_files_in_recycle_bin(recycle_path)
    output_csv_path = r"C:\output\trash.csv"
    save_to_csv(files, output_csv_path)
    print(f"Данные успешно сохранены в {output_csv_path}")

if __name__ == "__main__":
    main()