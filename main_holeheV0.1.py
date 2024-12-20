#Splash Screen - start
try:
    import pyi_splash #type: ignore
    pyi_splash.update_text('UI Loading ...')
except:
    pass

import sys
import sqlite3
import subprocess
import holehe

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, QDialog, QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QCursor, QPixmap

class MainWindow(QMainWindow):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('OSINT Holehe Tool')
        self.setGeometry(500, 200, 800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.98)       
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1F1F1F;
                border-radius: 10px;
                border: 1px solid #7F7F7F;
            }
            QPushButton {
                background-color: rgba(41, 128, 185, 1);
                border: none;
                border-radius: 10px;
                font-size: 16px;
                color: white;
                font-weight : Bold;
                padding: 10px;
                text-align: center;
                padding-left: 20px;
                padding-right: 20px;
            }
            QPushButton:hover {
                background-color: #256e9d;
                           color: #fffff0;
            }

        """)
        self.oldPos = self.pos()

        #Font Family
        font9 = QFont("Roboto", 9, QFont.Normal)
        font11 = QFont("Roboto", 11, QFont.Normal)
        font11Bold = QFont("Roboto", 10, QFont.Bold)
        font12Bold = QFont("Roboto", 12, QFont.Bold)

        #titlebar
        self.title_bar = QWidget(self)
        self.title_bar.setGeometry(0, 0, 800, 36)
        self.title_bar.setStyleSheet("""
            QWidget {
                background-color: #121212;
                border-top: 1px solid #7F7F7F;
                border-left: 1px solid #7F7F7F;
                border-right: 1px solid #7F7F7F;
                border-bottom: 1px solid #121212;
                border-top-right-radius: 10px;           
                border-top-left-radius: 10px;
                border-bottom-right-radius: 0px;
                border-bottom-left-radius: 0px;
                }
            """)
        
        #titlebar-icon
        self.title_dot = QWidget(self)
        self.title_dot.setGeometry(15 , 13, 15, 15)
        self.title_dot.setStyleSheet("background-color: #428FC7; border-radius: 7px; ")

        # Titlebar-title
        self.label0 = QLabel(self)
        self.label0.setObjectName("Titlebar")
        self.label0.setGeometry(320, 8, 300, 25)
        self.label0.setFont(font12Bold)
        self.label0.setAutoFillBackground(False)
        self.label0.setText("OSINT Holehe Tool")
        self.label0.setStyleSheet("QLabel { color: #E8E8E8; }")

        # Title_2
        self.label2 = QLabel(self)
        self.label2.setObjectName("Title_version")
        self.label2.setGeometry(40, 8, 180, 25)
        self.label2.setFont(font9)
        self.label2.setAutoFillBackground(False)
        self.label2.setText("Version 0.1")
        self.label2.setStyleSheet("QLabel { color: white; }")

        # Minimize Button
        self.minimize_button = QPushButton('_', self)
        self.minimize_button.setGeometry(700, 1, 50, 35)
        self.minimize_button.setProperty("cursor", QCursor(Qt.PointingHandCursor))
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #191919;
                border: none;
                font-size: 16px;
                font-weight: bold;
                color: #FFFFFF;
                border-top-right-radius: 0;
                border-top-left-radius: 0;
                border-bottom-right-radius: 0;
                border-bottom-left-radius: 0;
                padding: 0;
                margin: 0;
            }
            QPushButton:hover {
                background-color: #292929;
            }
        """)
        self.minimize_button.raise_()

        # Close Button
        self.close_button = QPushButton('X', self)
        self.close_button.setGeometry(749, 1, 50, 35)
        self.close_button.setProperty("cursor", QCursor(Qt.PointingHandCursor))
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(200, 0, 0, 0.6);
                border: none;
                font-size: 16px;
                font-weight: bold;
                color: #E8E8E8;
                border-top-right-radius: 10px;           
                border-top-left-radius: 0;
                border-bottom-right-radius: 0;
                border-bottom-left-radius: 0;
                padding: 0;
                margin: 0;
            }
            QPushButton:hover {
                background-color: rgba(200, 0, 0, 1);
            }
        """)

        # Email Input
        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(40, 60, 380, 40)
        self.email_input.setPlaceholderText('Enter email address')
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
            }
        """)

        # Submit Button
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.setGeometry(450, 60, 100, 40)
        self.submit_button.clicked.connect(self.check_email)

        # Result Box
        self.result_box = QTextEdit(self)
        self.result_box.setGeometry(40, 120, 720, 440)
        self.result_box.setReadOnly(True)
        self.result_box.setStyleSheet(""" 
            QTextEdit {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                color: white;
                font-size: 14px;
            }
        """)
        try:  
            # Logo
            self.logo = QLabel(self)
            self.logo.setGeometry(220, 160, 340, 340) 
            self.logo.setPixmap(QPixmap('logo.png').scaled(340, 340))
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.2)
            self.logo.setGraphicsEffect(opacity_effect)
            self.logo.lower()
        except:
            pass

        # View DB Button
        self.view_db_button = QPushButton('View Saved DB', self)
        self.view_db_button.setProperty("cursor", QCursor(Qt.PointingHandCursor))
        self.view_db_button.setGeometry(580, 60, 180, 40)
        self.view_db_button.clicked.connect(self.view_db)

        self.init_db()

        

    def init_db(self):
        self.conn = sqlite3.connect('holehe_emails.db')
        self.cursor = self.conn.cursor()
        # Create a base table with email column if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS emails (email TEXT)''')
        self.conn.commit()

    def check_email(self):
        email = self.email_input.text()
        if email:
            try:
                self.result_box.setText('Fetching Data... Please wait...')
                QApplication.processEvents()
                result = subprocess.run(['holehe', email], capture_output=True, text=True)
                filtered_output = self.filter_results(result.stdout)
                self.result_box.setText(self.format_results(email, filtered_output))
                self.save_to_db(email, filtered_output)
            except Exception as e:
                self.result_box.setText(f"Error: {str(e)}")
        else:
            self.result_box.setText('Please enter an email address.')
    def format_results(self, email, results):
        lines = results.split('\n')
        used = []
        not_used = []
        rate_limit = []
    
        for line in lines:
            if '[+]' in line:
                if 'Email used' in line:
                    continue
                used.append(line.replace('[+]', '').strip())
            elif '[-]' in line:
                not_used.append(line.replace('[-]', '').strip())
            elif '[x]' in line:
                rate_limit.append(line.replace('[x]', '').strip())
    
        html = f"""
        <h3>Entered Email: {email}</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>Email Used</th>
                <th>Email Not Used</th>
                <th>Rate Limit</th>
            </tr>
            <tr>
                <td>
                    <ul>
                        {''.join(f'<li>{site}</li>' for site in used)}
                    </ul>
                </td>
                <td>
                    <ul>
                        {''.join(f'<li>{site}</li>' for site in not_used)}
                    </ul>
                </td>
                <td>
                    <ul>
                        {''.join(f'<li>{site}</li>' for site in rate_limit)}
                    </ul>
                </td>
            </tr>
        </table>
        """
        return html

    def save_to_db(self, email, result):
        # Extract websites and their statuses
        results_dict = {line.split(' ')[1]: line.split(' ')[0] for line in result.split('\n') if line}

        # Create columns if they do not exist
        existing_columns = self.get_existing_columns()
        for website in results_dict.keys():
            if website not in existing_columns:
                try:
                    self.cursor.execute(f'''ALTER TABLE emails ADD COLUMN "{website}" TEXT''')
                except sqlite3.OperationalError as e:
                    print(f"An error occurred: {e}")

        # Prepare the insert statement
        columns = ', '.join([f'"{website}"' for website in results_dict.keys()])
        placeholders = ', '.join(['?' for _ in results_dict.keys()])
        sql = f'INSERT INTO emails (email, {columns}) VALUES (?, {placeholders})'

        try:
            # Insert the email and results
            self.cursor.execute(sql, [email] + list(results_dict.values()))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Error: This email already exists in the database.")


    def get_existing_columns(self):
        # Get the list of existing columns in the emails table
        self.cursor.execute("PRAGMA table_info(emails)")
        return [info[1] for info in self.cursor.fetchall()]

    def view_db(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Saved Emails')
        dialog.setGeometry(100, 100, 600, 400)

        table = QTableWidget(dialog)
        table.setGeometry(10, 10, 580, 380)

        self.cursor.execute('SELECT * FROM emails')
        rows = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]

        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)

        table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, item in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(item))

        dialog.exec_()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

    def filter_results(self, output):
        lines = output.split('\n')
        cleaned_lines = []
        skip_lines = False
        for line in lines:
            if "Twitter :" in line or "Github :" in line or "For BTC Donations :" in line:
                skip_lines = True
                continue
            if skip_lines and line.startswith('*' * 10):
                skip_lines = False
                continue
            if not skip_lines and ('[x]' in line or '[+]' in line or '[-]' in line or 'Email used' in line or 'Rate limit' in line):
                cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)

if __name__ == '__main__':
    app = QApplication(sys.argv)
        #Splash Screen - close
    try:
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
    except:
        pass 
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())