import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

class SpaceScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPACE-SCANNER")
        self.setFixedSize(800, 600)

        self.init_ui()

    def init_ui(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(20, 20, 20))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Button, QColor(40, 40, 40))
        palette.setColor(QPalette.ButtonText, Qt.white)

        self.setPalette(palette)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.logo_label = QLabel("🚀 SPACE‑SCANNER 🚀", self)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.logo_label.setStyleSheet("color: cyan;")
        self.main_layout.addWidget(self.logo_label)

        QTimer.singleShot(2000, self.show_menu)

    def show_menu(self):
        self.logo_label.deleteLater()

        header = QLabel("Выберите функцию:", self)
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 20))
        header.setStyleSheet("color: lightgreen; margin-bottom: 20px;")
        self.main_layout.addWidget(header)

    
        button_style = """
            QPushButton {
                background-color: #1E90FF;
                color: white;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #63b3ed;
            }
            QPushButton:pressed {
                background-color: #1570a5;
            }
        """

        btn_texts = [
            "🔍 Поиск файлов по ключевым словам",
            "🛡️ Проверка неподписанных файлов",
            "💾 Выгрузка данных в CSV",
            "🗑️ Проверка удаления корзины"
        ]

        commands = [
            self.func_search_files,
            self.func_check_unsigned,
            self.func_export_csv,
            self.func_check_recycle_bin
        ]

        for text, cmd in zip(btn_texts, commands):
            btn = QPushButton(text)
            btn.setStyleSheet(button_style)
            btn.setFixedHeight(50)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(cmd)
            self.main_layout.addWidget(btn)


        self.main_layout.addStretch()

    def func_search_files(self):
        QMessageBox.information(self, "Функция", "Запущен поиск файлов по ключевым словам")

    def func_check_unsigned(self):
        QMessageBox.information(self, "Функция", "Проверка неподписанных файлов")

    def func_export_csv(self):
        QMessageBox.information(self, "Функция", "Экспорт данных в CSV")

    def func_check_recycle_bin(self):
        QMessageBox.information(self, "Функция", "Проверка корзины")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpaceScanner()
    window.show()
    sys.exit(app.exec_())
