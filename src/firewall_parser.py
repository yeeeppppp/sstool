def main():
     print("Функция выполняется...")
import win32com.client
import os

def get_firewall_rules():
    fw_policy = win32com.client.Dispatch('HNetCfg.FwPolicy2')
    rules = fw_policy.Rules

    all_rules = []
    for rule in rules:
        rule_dict = {}
        try:
            rule_dict['Name'] = rule.Name
        except AttributeError:
            rule_dict['Name'] = ''
        try:
            rule_dict['DisplayName'] = getattr(rule, 'DisplayName', '')
        except AttributeError:
            rule_dict['DisplayName'] = ''
        try:
            rule_dict['Enabled'] = str(rule.Enabled)
        except AttributeError:
            rule_dict['Enabled'] = ''
        try:
            rule_dict['Action'] = str(rule.Action)
        except AttributeError:
            rule_dict['Action'] = ''
        try:
            rule_dict['Direction'] = 'Inbound' if rule.Direction == 1 else 'Outbound'
        except AttributeError:
            rule_dict['Direction'] = ''
        try:
            rule_dict['Profiles'] = rule.Profiles
        except AttributeError:
            rule_dict['Profiles'] = ''
        try:
            rule_dict['Program'] = rule.ApplicationName
        except AttributeError:
            rule_dict['Program'] = ''
        try:
            rule_dict['Protocol'] = rule.Protocol
        except AttributeError:
            rule_dict['Protocol'] = ''
        try:
            rule_dict['LocalPorts'] = rule.LocalPorts
        except AttributeError:
            rule_dict['LocalPorts'] = ''
        try:
            rule_dict['RemotePorts'] = rule.RemotePorts
        except AttributeError:
            rule_dict['RemotePorts'] = ''
        try:
            rule_dict['RemoteAddresses'] = rule.RemoteAddresses
        except AttributeError:
            rule_dict['RemoteAddresses'] = ''
        try:
            rule_dict['LocalAddresses'] = rule.LocalAddresses
        except AttributeError:
            rule_dict['LocalAddresses'] = ''
        try:
            rule_dict['EdgeTraversal'] = str(rule.EdgeTraversal)
        except AttributeError:
            rule_dict['EdgeTraversal'] = ''
        try:
            rule_dict['EdgeTraversalPolicy'] = rule.EdgeTraversalPolicy
        except AttributeError:
            rule_dict['EdgeTraversalPolicy'] = ''

        if hasattr(rule, 'Direction') and rule.Direction == 1:
            all_rules.append(rule_dict)

    return all_rules

def save_rules_to_csv(rules, filename):
    import csv
    if not rules:
        print("Нет правил для записи.")
        return
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fieldnames = rules[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rule in rules:
            writer.writerow(rule)

def main():
    rules = get_firewall_rules()

    target_files = [
        "Nursultan.exe",
        "Delta.exe",
        "Deltaclient.exe",
        "1.16.5.exe",
        "Beta 1.16.5.exe",
        "Alpha 1.16.5.exe",
        "Celestial.exe",
        "Takker.exe",
        "Catlavan.exe",
        "DeltaLoader.exe",
        "NTFLoader.exe",
        "TelamonCleaner",
        "Wexside.exe",
        "FLauncher.exe",
        "NewLauncher.exe",
        "Beta1.16.5.exe",
        "Alpha1.16.5.exe",
        "ExLoader.exe",
        "Exloader.exe",
        "ExtremeInjector.exe",
        "extremeinjector.exe",
        "Fakker.exe"
    ]

    filtered_rules = []
    for rule in rules:
        program = rule.get('Program', '')
        if program:
            for filename in target_files:
                if filename.lower() in program.lower():
                    filtered_rules.append(rule)
                    break
    save_rules_to_csv(rules, 'C:/output/firewall_rules_all.csv')
    print("Все правила сохранены в 'C:/output/firewall_rules_all.csv'.")

    save_rules_to_csv(filtered_rules, 'C:/output/firewall_target_files.csv')
    print("Целевые правила сохранены в 'C:/output/firewall_target_files.csv'.")

if __name__ == '__main__':
    main()