import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QTextEdit, QLabel, 
                             QStackedWidget, QMessageBox, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt

# --- MODERN DESIGN STYLE SHEET (QSS) ---
STYLE_SHEET = """
QWidget {
    background-color: #F7FAFC;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #2D3748;
}

QLabel#titleLabel {
    font-size: 26px;
    font-weight: bold;
    color: #1A365D;
    margin-bottom: 5px;
}

QLabel#subtitleLabel {
    font-size: 14px;
    color: #718096;
    margin-bottom: 20px;
}

/* Title Input Box and Text Editor */
QLineEdit, QTextEdit {
    background-color: white;
    border: 2px solid #E2E8F0;
    border-radius: 8px;
    padding: 12px;
    font-size: 15px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 2px solid #3182CE;
}

/* Standard Buttons */
QPushButton {
    background-color: #3182CE;
    color: white;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #2B6CB0;
}
QPushButton#successBtn {
    background-color: #38A169;
}
QPushButton#successBtn:hover {
    background-color: #2F855A;
}
QPushButton#dangerBtn {
    background-color: #E53E3E;
}
QPushButton#dangerBtn:hover {
    background-color: #C53030;
}

/* Row Inline Delete Button (Trash Can) */
QPushButton#rowDeleteBtn {
    background-color: transparent;
    border: none;
    font-size: 18px;
    padding: 5px 10px;
}
QPushButton#rowDeleteBtn:hover {
    background-color: #FED7D7; /* Light red background on hover */
    border-radius: 6px;
}

/* Note List Design */
QListWidget {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 5px;
}
QListWidget::item {
    background-color: #FFFFFF;
    border-bottom: 1px solid #EDF2F7;
    margin-bottom: 4px;
    border-radius: 6px;
}
QListWidget::item:hover {
    background-color: #F7FAFC;
}
QListWidget::item:selected {
    background-color: #EBF8FF;
}
"""

# --- 1. MY NOTES SCREEN (MAIN DASHBOARD) ---
class MyNotesScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("📝 My Notebook")
        title.setObjectName("titleLabel")
        subtitle = QLabel("Manage and view your daily notes.")
        subtitle.setObjectName("subtitleLabel")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        self.notes_list_widget = QListWidget()
        layout.addWidget(self.notes_list_widget)
        
        layout.addSpacing(15)
        
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Add New Note")
        self.view_btn = QPushButton("📖 Read Note")
        self.view_btn.setStyleSheet("background-color: #4A5568;")
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.view_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        self.add_btn.clicked.connect(self.go_to_editor)
        self.view_btn.clicked.connect(self.view_note)
        self.notes_list_widget.itemDoubleClicked.connect(self.view_note)

    def go_to_editor(self):
        self.main_window.note_editor_screen.clear_editor()
        self.main_window.setCurrentIndex(1)

    def load_notes_to_list(self):
        self.notes_list_widget.clear()
        
        for idx, note in enumerate(self.main_window.notes_storage):
            # 1. Create an empty list item
            item = QListWidgetItem(self.notes_list_widget)
            
            # 2. Design the custom container (Widget) to place inside the row
            row_widget = QWidget()
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(10, 10, 10, 10)
            
            # 3. Note title and date (Left Side)
            item_text = f"📌  <b>{note['title']}</b> \t\t <span style='color:gray;'>({note['date']})</span>"
            lbl = QLabel(item_text)
            
            # 4. Trash Can Button (Right Side)
            del_btn = QPushButton("🗑️")
            del_btn.setObjectName("rowDeleteBtn")
            del_btn.setCursor(Qt.PointingHandCursor) # Change mouse cursor to hand pointer
            
            # Trigger delete function when the trash can is clicked (Pass the target index)
            del_btn.clicked.connect(lambda checked, i=idx: self.delete_note(i))
            
            # 5. Place elements in the row layout (Label to the left, button to the right)
            row_layout.addWidget(lbl)
            row_layout.addStretch() # Automatically fill the space between them
            row_layout.addWidget(del_btn)
            
            row_widget.setLayout(row_layout)
            
            # 6. Adjust the height of the list item based on our custom widget and add it
            item.setSizeHint(row_widget.sizeHint())
            self.notes_list_widget.setItemWidget(item, row_widget)
            
            item.setData(Qt.UserRole, idx)

    def delete_note(self, index):
        # Ask the user for confirmation before deleting
        reply = QMessageBox.question(self, 'Delete Note', 
                                     "Are you sure you want to delete this note?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Delete the note from the storage list
            del self.main_window.notes_storage[index]
            # Redraw the list on the screen
            self.load_notes_to_list()

    def view_note(self):
        selected_item = self.notes_list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Selection Error", "Please select a note from the list to read!")
            return
            
        note_index = selected_item.data(Qt.UserRole)
        note_data = self.main_window.notes_storage[note_index]
        
        self.main_window.note_editor_screen.open_existing_note(note_data)
        self.main_window.setCurrentIndex(1)


# --- 2. WRITING / EDITOR SCREEN ---
class NoteEditorScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        layout.addWidget(QLabel("<b>Note Title:</b>"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter a title...")
        layout.addWidget(self.title_input)
        
        layout.addSpacing(10)
        
        layout.addWidget(QLabel("<b>Your Note:</b>"))
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Type your thoughts here...")
        layout.addWidget(self.content_input)
        
        layout.addSpacing(15)
        
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("🔙 Cancel")
        self.cancel_btn.setObjectName("dangerBtn")
        
        self.save_btn = QPushButton("💾 Save Note")
        self.save_btn.setObjectName("successBtn")
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        self.cancel_btn.clicked.connect(self.back_to_main)
        self.save_btn.clicked.connect(self.save_note)

    def clear_editor(self):
        self.title_input.clear()
        self.content_input.clear()

    def open_existing_note(self, note):
        self.title_input.setText(note["title"])
        self.content_input.setText(note["content"])

    def save_note(self):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, "Validation Error", "A note must have a title!")
            return
            
        current_time = datetime.now().strftime("%H:%M - %d/%m/%Y")
        new_note = {
            "title": title,
            "content": content,
            "date": current_time
        }
        
        self.main_window.notes_storage.append(new_note)
        self.main_window.my_notes_screen.load_notes_to_list()
        self.back_main_success()

    def back_to_main(self):
        self.main_window.setCurrentIndex(0)

    def back_main_success(self):
        QMessageBox.information(self, "Success", "Your note has been successfully saved!")
        self.main_window.setCurrentIndex(0)


# --- MAIN APPLICATION MANAGER ---
class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎯 Fluent Note App")
        self.resize(700, 550)
        self.setStyleSheet(STYLE_SHEET)
        
        self.notes_storage = []
        
        self.my_notes_screen = MyNotesScreen(self)
        self.note_editor_screen = NoteEditorScreen(self)
        
        self.addWidget(self.my_notes_screen)
        self.addWidget(self.note_editor_screen)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())