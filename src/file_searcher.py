import os
import csv
import string

keywords = [
    "impact", "wurst", "bleachhack", "aristois", "huzuni", "skillclient", "inertia", "ares", "sigma", "meteor",
    "liquidbounce", "nurik", "nursultan", "celestial", "calestial", "celka", "expensive", "neverhook", "excellent",
    "wexside", "wildclient", "minced", "deadcode", "akrien", "nursultan", "jigsaw", "future", "jessica", "dreampool",
    "norules", "konas", "richclient", "rusherhack", "thunderhack", "moonhack", "doomsday", "nightware", "ricardo",
    "extazyy", "troxill", "antileak", "arbuz", ".akr", ".wex", "dauntiblyat", "rename_me_please", "editme", "takker",
    "fuzeclient", "wisefolder", "flauncher", "vec.dll", "USBOblivion.exe", "Feather", "delta", "venus", "baritone",
    "spambot", "CleanCut", "spam_bot", "inventory_walk", "player_highlighter", "aimbot", "freecam", "bedrock_breaker_mode",
    "viaversion", "double_hotbar", "elytra_swap", "armor_hotswap", "smart_moving", "chest", "savesearcher",
    "topkautobuy", "topkaautobuy", "tweakeroo", "mob_hitbox", "librarian_trade_finder", "sacurachorusfind",
    "autoattack", "entity_outliner", "invmove", "viabackwards", "viarewind", "viafabric", "viaforge", "viaproxy",
    "vialoader", "viamcp", "hitbox", "elytrahack", "DiamondSim", "ForgeHax", "clientcommands", "Control-Tweaks",
    "SwingThroughGrass", "CutThrough", "Haruka", "NewLauncher", "Blade", "Hachclient", "Inertia", "Fleuger",
    "Exloader", "NTFLoader"
]

def search_keywords_and_save():
    results = []

    output_dir = "C:/output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "SStool.csv")

    drives = []
    for drive_letter in string.ascii_uppercase:
        drive_path = f"{drive_letter}:\\"
        if os.path.exists(drive_path):
            drives.append(drive_path)
    user_profile = os.environ.get('USERPROFILE', '')
    desktop_path = os.path.join(user_profile, 'Desktop')
    downloads_path = os.path.join(user_profile, 'Downloads')
    documents_path = os.path.join(user_profile, 'Documents')
    user_dirs = [desktop_path, downloads_path, documents_path]

    appdata_dirs = ["Roaming", "Local", "LocalLow"]
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            try:
                folder_name = os.path.basename(root).lower()
                for keyword in keywords:
                    if folder_name.startswith(keyword.lower()):
                        results.append({"path": root, "match": keyword, "location": "Drive"})
            except Exception:
                continue
        for folder in appdata_dirs:
            appdata_path = os.path.join(os.environ.get('APPDATA', ''), folder)
            if os.path.exists(appdata_path):
                for root, dirs, files in os.walk(appdata_path):
                    try:
                        folder_name = os.path.basename(root).lower()
                        for keyword in keywords:
                            if folder_name.startswith(keyword.lower()):
                                results.append({"path": root, "match": keyword, "location": "AppData"})
                    except Exception:
                        continue
    for user_dir in user_dirs:
        if os.path.exists(user_dir):
            for root, dirs, files in os.walk(user_dir):
                try:
                    folder_name = os.path.basename(root).lower()
                    for keyword in keywords:
                        if folder_name.startswith(keyword.lower()):
                            results.append({"path": root, "match": keyword, "location": "UserFolder"})
                except Exception:
                    continue

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f) 
        writer.writerow(["Found Path", "Matched Keyword", "Location"])
        for item in results:
            writer.writerow([item["path"], item["match"], item["location"]])

    print(f"Результаты сохранены в {output_file}")

if __name__ == "__main__":
    search_keywords_and_save()