# LocatR - Student Location Management System

**Requested by the University Registrar**

LocatR is a desktop application designed to manage student records, including their ID, name, course, and location. This project was developed in Python using Tkinter for the GUI and SQLite for data storage. The system allows adding, editing, deleting, and searching students efficiently, with a clean and intuitive interface.

---

## Features

- **Add Students:** Input student ID, name, course, and location. The location can be set to `UP` or `DOWN` using radio buttons.
- **Edit Students:** Modify existing student details. Ensures unique student IDs.
- **Delete Students:** Remove student records with confirmation prompt.
- **Search Students:** Search by Student ID or Name dynamically.
- **Scrollable List:** View all students in a scrollable, organized table.
- **Input Validation:**
  - Student ID must be exactly 10 digits and unique.
  - Name and course cannot contain numbers.
- **SQLite Database:** Stores student information persistently.
- **Custom UI Design:** Uses Tkinter Designer-generated layout and custom images for buttons and entries.
- **DPI Awareness:** Automatically adjusts for high-DPI screens on Windows.

---

## Screenshots

![Main Window](build\assets\frame0\main.png)  
![Add Student Window](build\assets\frame0\add.png)  
![Edit Student Window](build\assets\frame0\edit.png)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/LocatR.git
   cd LocatR

   ```

2. **Install Dependencies:**

   ```bash
    pip install pillow

   ```

3. **Run the Application:**
   ```bash
    python main.py
   ```

## Dependencies

- **Python 3.9+**
- **Tkinter** (comes with Python standard library)
- **Pillow** (for image handling)
- **SQLite3** (comes with Python standard library)

## Notes

- This project was specifically requested by the University Registrar to manage student location data efficiently.
- All UI elements are dynamically rendered and support high-DPI displays on Windows.
- Ensure the assets/ folder remains in the same path relative to main.py to avoid missing images.

## Author

**Joseph T. Pendon Jr.**
University Student | Software Developer
