import subprocess
from colorama import init, Fore, Style

init(autoreset=True)
services = ["PcaSvc", "EventLog", "Bam", "AppInfo", "DPS"]

def check_service(service_name):
    """
    Проверяет статус службы.
    Возвращает строку: 'Запущена', 'Не запущена', or 'Служба не найдена'.
    """
    try:
        cmd = ["powershell", "-Command", f"Get-Service -Name '{service_name}' | Select-Object -Property Status"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        
        if "Running" in output:
            return "Запущена", Fore.GREEN
        elif "Stopped" in output:
            return "Не запущена", Fore.RED
        else:
            return "Статус неизвестен", Fore.YELLOW
    except subprocess.CalledProcessError:
        return "Служба не найдена", Fore.RED

print(f"{'Статус служб на системе:':^40}\n")
for service in services:
    status_text, color = check_service(service)
    print(f"Служба '{service}': {color}{status_text}{Style.RESET_ALL}")