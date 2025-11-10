def main():
     print("Функция выполняется...")
import win32evtlog
import csv
import os

server = 'localhost'

filters = {
    'Application': [3079],  # EventID 3079 в Application
    'Security': [1102]      # EventID 1102 в Security
}

output_dir = r"C:\output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_path = os.path.join(output_dir, "filtered_events.csv")

def fetch_filtered_events(log_type, event_ids):
    filtered_events = []
    try:
        handle = win32evtlog.OpenEventLog(server, log_type)
        flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        while True:
            events = win32evtlog.ReadEventLog(handle, flags, 0)
            if not events:
                break
            for event in events:
                event_id_masked = event.EventID & 0xFFFF
                if event_id_masked in event_ids:
                    filtered_events.append((log_type, event))
        win32evtlog.CloseEventLog(handle)
    except Exception as e:
        print(f"Ошибка при чтении журнала {log_type}: {e}")
    return filtered_events

all_events = []

for log_type, event_ids in filters.items():
    print(f"Чтение журнала {log_type} с EventID {event_ids}...")
    events = fetch_filtered_events(log_type, event_ids)
    print(f"Найдено {len(events)} событий в {log_type}")
    all_events.extend(events)

with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['LogType', 'TimeGenerated', 'SourceName', 'EventID', 'EventCategory', 'ComputerName', 'Strings']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for log_type, event in all_events:
        inserts = event.StringInserts
        if isinstance(inserts, list):
            inserts_str = "; ".join(inserts)
        elif inserts:
            inserts_str = str(inserts)
        else:
            inserts_str = ''
        writer.writerow({
            'LogType': log_type,
            'TimeGenerated': str(event.TimeGenerated),
            'SourceName': event.SourceName,
            'EventID': event.EventID & 0xFFFF,
            'EventCategory': event.EventCategory,
            'ComputerName': event.ComputerName,
            'Strings': inserts_str
        })

print(f"Фильтрованные события сохранены в {output_path}")