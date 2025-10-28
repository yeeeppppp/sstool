import winreg
import csv
import os
import string
output_dir = r'C:\output'
os.makedirs(output_dir, exist_ok=True)

registry_paths = [
    {
        'name': 'OpenPidSaveMRU',
        'path': r'Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU',
        'root': winreg.HKEY_CURRENT_USER,
        'filename': 'OpenPidSaveMRU.csv'
    },
    {
        'name': 'PrefetchEnable',
        'path': r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters',
        'root': winreg.HKEY_LOCAL_MACHINE,
        'filename': 'PrefetchEnable.csv'
    },
    {
        'name': 'RecentDocs',
        'path': r'Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs',
        'root': winreg.HKEY_CURRENT_USER,
        'filename': 'RecentDocs.csv'
    },
    {
        'name': 'NetworkHistory',
        'path': r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters',
        'root': winreg.HKEY_LOCAL_MACHINE,
        'filename': 'NetworkHistory.csv'
    },
    {
        'name': 'PcaSvcCheck',
        'path': r'Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store',
        'root': winreg.HKEY_CURRENT_USER,
        'filename': 'PcaSvcCheck.csv'
    }
]
def root_name(root):
    names = {
        winreg.HKEY_CURRENT_USER: 'HKEY_CURRENT_USER',
        winreg.HKEY_LOCAL_MACHINE: 'HKEY_LOCAL_MACHINE',
        winreg.HKEY_CLASSES_ROOT: 'HKEY_CLASSES_ROOT',
        winreg.HKEY_USERS: 'HKEY_USERS',
        winreg.HKEY_CURRENT_CONFIG: 'HKEY_CURRENT_CONFIG'
    }
    return names.get(root, str(root))

def value_type_str(value_type):
    types = {
        winreg.REG_SZ: 'REG_SZ',
        winreg.REG_DWORD: 'REG_DWORD',
        winreg.REG_BINARY: 'REG_BINARY',
        winreg.REG_MULTI_SZ: 'REG_MULTI_SZ',
        winreg.REG_EXPAND_SZ: 'REG_EXPAND_SZ',
    }
    return types.get(value_type, str(value_type))
def extract_readable_string(data, min_length=4):
    max_str = ''
    current_str = ''
    for byte in data:
        c = chr(byte)
        if c in string.printable and c not in '\r\n\t':
            current_str += c
        else:
            if len(current_str) > len(max_str):
                max_str = current_str
            current_str = ''
    if len(current_str) > len(max_str):
        max_str = current_str
    if len(max_str) >= min_length:
        return max_str
    return ''
def smart_decode(value, value_type, section_name, key_name):
    if section_name == 'OpenPidSaveMRU' and value_type == winreg.REG_BINARY:
        readable = extract_readable_string(value)
        if readable:
            return f"Название файла: {readable}"
        else:
            return f"Hex: {value.hex()}"
    if value_type == winreg.REG_BINARY:
        readable = extract_readable_string(value)
        if readable:
            return f"Название файла: {readable}"
        else:
            return f"Hex: {value.hex()}"
    elif value_type in (winreg.REG_SZ, winreg.REG_EXPAND_SZ):
        return value
    elif value_type == winreg.REG_MULTI_SZ:
        return "; ".join(value)
    elif value_type == winreg.REG_DWORD:
        return str(value)
    else:
        return str(value)
def parse_registry(root, path, section_name):
    results = []
    try:
        with winreg.OpenKey(root, path) as key:
            index = 0
            while True:
                try:
                    name, value, vtype = winreg.EnumValue(key, index)
                    decoded_value = smart_decode(value, vtype, section_name, name)
                    results.append({
                        'RegistryPath': f"{root_name(root)}\\{path}",
                        'Parameter': name,
                        'Type': value_type_str(vtype),
                        'Value': decoded_value
                    })
                    index += 1
                except OSError:
                    break
            sub_index = 0
            while True:
                try:
                    sub_name = winreg.EnumKey(key, sub_index)
                    sub_path = f"{path}\\{sub_name}"
                    results.extend(parse_registry(root, sub_path, section_name))
                    sub_index += 1
                except OSError:
                    break
    except:
        pass
    return results
for entry in registry_paths:
    print(f"Обрабатываю {entry['name']} по пути {entry['path']}...")
    data = parse_registry(entry['root'], entry['path'], entry['name'])
    filename = os.path.join(output_dir, entry['filename'])
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['RegistryPath', 'Parameter', 'Type', 'Value'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f'Файл {filename} сохранён. ({len(data)} записей)')

print('Все файлы сохранены в C:/output.')

