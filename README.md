# 🎯 Fluent Note App - A Modern PyQt5 Note Management System

Fluent Note App is a sleek, modern, and intuitive GUI-based desktop application designed for efficient daily note management. Developed as a final project for the **COM206** course, this application prioritizes a fluid user experience without relying on complex backend databases.

---

## 👤 Student Information
* **Name:** Almila Kocaağaoğlu
* **Student Number:** 230417379
* **Course:** COM206 - Final Project Submission

---

## ❓ Problem Statement & Objective
* **Problem Statement:** How can we efficiently manage, store, and view daily notes in a user-friendly, modern desktop environment without relying on complex backend databases?
* **Objective:** To design an in-memory, GUI-based notebook application that allows users to seamlessly add, read, and delete notes using an intuitive interface driven by the PyQt5 framework.

---

## ✨ Features
* **Modern UI/UX:** Styled completely using custom QSS (Qt Style Sheets) featuring a clean, responsive, and minimalist interface.
* **State Management:** Fluid screen transitions between the Main Dashboard and the Note Editor using `QStackedWidget`.
* **In-Memory Architecture:** Utilizes temporary RAM storage structured via Python dictionaries inside a central session list for swift data manipulation.
* **Interactive List Widget:** Notes are displayed dynamically with embedded timestamps and dedicated, hover-responsive trash bin icons for intuitive single-click deletions.
* **Safety Dialogs:** Built-in `QMessageBox` confirmations to protect users against accidental note deletion.

---

## 🛠️ Methodology & Technical Details

### Control Flow
1. **Start Program:** Launches into the Main Dashboard (`MyNotesScreen`) where all existing notes are dynamically rendered into a custom `QListWidget`.
2. **Add Note:** Navigates to the `NoteEditorScreen`. Validates inputs, captures the precise system timestamp, appends the data to memory, and refreshes the dashboard view.
3. **Read Note:** Double-clicking an item or selecting a note and clicking "Read Note" loads existing data directly into the fields for viewing.
4. **Delete Note:** Clicking the trash icon triggers a confirmation prompt; upon approval, the item is dropped from the collection by index, and the UI re-renders instantly.
5. **Exit:** Terminating the application clears the temporary runtime memory state.

### Tech Stack
* **Language:** Python 3
* **GUI Framework:** PyQt5
* **Core Modules:** `QtWidgets` (`QStackedWidget`, `QListWidget`, `QMessageBox`), `QtCore` (`Qt`), `datetime`

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python installed on your Mac, along with the PyQt5 library. You can install the framework via terminal:

```bash
pip install PyQt5
