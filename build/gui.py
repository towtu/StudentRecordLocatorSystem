import customtkinter as ctk
import sqlite3
import textwrap
import os
import ctypes
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import qrcode
from io import BytesIO

# --- 1. APP CONFIGURATION ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# --- BRANDING ---
COLOR_ACCENT = "#1A1851"        # Official Brand Color
FONT_MAIN = "Inter"             # Official Font

# UI Colors
COLOR_BG = "#FFFFFF"
COLOR_SIDEBAR = "#FFFFFF"
COLOR_TEXT_NAV = "#64748B"
COLOR_HOVER = "#F1F5F9"
COLOR_ERROR = "#DC2626"
COLOR_LINK = "#3B82F6"
COLOR_NEUTRAL = "#6c757d"
COLOR_NEUTRAL_HOVER = "#5a6268"
COLOR_SEPARATOR = "#E2E8F0"     # Light Gray for Lines

# --- LOCATION COLORS ---
COLOR_UP = "#059669"            # Emerald Green
COLOR_DOWN = "#D97706"          # Amber / Dark Yellow

DB_NAME = "students.db"

# --- 2. DATA STRUCTURE ---
UNIVERSITY_STRUCTURE = {
    "College of Information Technology and Computing": {
        "icon_path": "assets/frame0/icon_citc.png",
        "programs": [
            {"name": "Bachelor of Science in Information Technology", "db_filter": "Information Technology"},
            {"name": "Bachelor of Science in Technology Communication Management", "db_filter": "Communication Management"},
            {"name": "Bachelor of Science in Data Science", "db_filter": "Data Science"},
            {"name": "Bachelor of Science in Computer Science", "db_filter": "Computer Science"},
            {"name": "Entrepreneurial Service Unit", "db_filter": "Entrepreneurial"}
        ]
    },
    "College of Engineering and Architecture": {
        "icon_path": "assets/frame0/icon_cea.png",
        "programs": [
            {"name": "Bachelor of Science in Architecture", "db_filter": "Architecture"},
            {"name": "Bachelor of Science in Civil Engineering", "db_filter": "Civil Engineering"},
            {"name": "Bachelor of Science in Mechanical Engineering", "db_filter": "Mechanical Engineering"},
            {"name": "Bachelor of Science in Computer Engineering", "db_filter": "Computer Engineering"},
            {"name": "Bachelor of Science in Geodetic Engineering", "db_filter": "Geodetic"},
            {"name": "Bachelor of Science in Electrical Engineering", "db_filter": "Electrical Engineering"},
            {"name": "Bachelor of Science in Electronics Engineering", "db_filter": "Electronics Engineering"},
            {"name": "Masters of Engineering Program", "db_filter": "Masters of Engineering"},
            {"name": "Master of Science in Electrical Engineering", "db_filter": "MS Electrical"},
            {"name": "Master of Science in Sustainable Development", "db_filter": "Sustainable Development"},
            {"name": "Professional Science Masters in Power Systems", "db_filter": "Power Systems"},
            {"name": "Doctor of Philosophy in Energy Engineering", "db_filter": "Energy Engineering"}
        ]
    },
    "College of Science and Mathematics": {
        "icon_path": "assets/frame0/icon_csm.png",
        "programs": [
            {"name": "Bachelor of Science in Applied Mathematics", "db_filter": "Applied Mathematics"},
            {"name": "Bachelor of Science in Applied Physics", "db_filter": "Applied Physics"},
            {"name": "Bachelor of Science in Chemistry", "db_filter": "Chemistry"},
            {"name": "Bachelor of Science in Environmental Science", "db_filter": "Environmental Science"},
            {"name": "Bachelor of Science in Food Technology", "db_filter": "Food Technology"},
            {"name": "Master of Science in Applied Mathematics", "db_filter": "MS Applied Mathematics"},
            {"name": "Master of Science in Environmental Science & Technology", "db_filter": "MS Environmental"}
        ]
    },
    "College of Science and Technology Education": {
        "icon_path": "assets/frame0/icon_cste.png",
        "programs": [
            {"name": "Bachelor in Secondary Education Major in Science", "db_filter": "BSED Science"},
            {"name": "Bachelor of Secondary Education Major in Mathematics", "db_filter": "BSED Mathematics"},
            {"name": "Bachelor in Technology and Livelihood Education", "db_filter": "Livelihood Education"},
            {"name": "Bachelor in Technical-Vocational Teacher Education", "db_filter": "Vocational Teacher"},
            {"name": "Certificate of Teaching", "db_filter": "Certificate of Teaching"},
            {"name": "Master of Science in Mathematics Education", "db_filter": "MS Mathematics Education"},
            {"name": "Master of Science in Science Education", "db_filter": "Science Education"},
            {"name": "Doctor of Technology Education", "db_filter": "Doctor of Technology"}
        ]
    },
    "College of Technology": {
        "icon_path": "assets/frame0/icon_cot.png",
        "programs": [
            {"name": "Bachelor of Science in Electronics Technology", "db_filter": "Electronics Technology"},
            {"name": "Bachelor of Science in Autotronics", "db_filter": "Autotronics"},
            {"name": "Bachelor of Science in Energy Systems and Management", "db_filter": "Energy Systems"},
            {"name": "Bachelor of Science in Electro-Mechanical Technology", "db_filter": "Electro-Mechanical"},
            {"name": "Bachelor of Science in Manufacturing Engineering Tech", "db_filter": "Manufacturing Engineering"}
        ]
    },
    "College of Medicine": {
        "icon_path": "assets/frame0/icon_med.png",
        "programs": [{"name": "Doctor of Medicine", "db_filter": "Medicine"}]
    },
    "College of Nursing": {
        "icon_path": "assets/frame0/icon_nursing.png",
        "programs": [{"name": "Bachelor of Science in Nursing", "db_filter": "Nursing"}]
    },
    "Senior High School": {
        "icon_path": "assets/frame0/icon_shs.png",
        "programs": [{"name": "STEM Strand", "db_filter": "STEM"}]
    },
    "Institute of Governance, Innovations & Sustainability": {
        "icon_path": "assets/frame0/icon_igis.png",
        "programs": [{"name": "Public Administration / Governance", "db_filter": "Governance"}]
    }
}

# --- 3. HELPER FUNCTIONS ---
def smart_break_text(text):
    replacements = {
        "Bachelor of Science in": "BS",
        "Bachelor in Secondary Education": "BSED",
        "Bachelor of Secondary Education": "BSED",
        "Bachelor in": "Bachelor",
        "Master of Science in": "MS",
        "Master of Arts in": "MA",
        "Doctor of Philosophy in": "PhD",
        "Doctor of": "Doctor of",
        "Professional Science Masters": "PSM"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return textwrap.fill(text, width=25)

def format_location_display(loc_code):
    if loc_code == "UP": return "↑ Upper Floor"
    if loc_code == "DOWN": return "↓ Lower Floor"
    return loc_code

def get_absolute_path(relative_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path_a = os.path.join(script_dir, relative_path)
    path_b = os.path.join(script_dir, "..", relative_path)
    if os.path.exists(path_a): return path_a
    elif os.path.exists(path_b): return path_b
    return None

def load_icon_ctk(relative_path, size=(24, 24)):
    final_path = get_absolute_path(relative_path)
    if final_path:
        try:
            return ctk.CTkImage(light_image=Image.open(final_path), dark_image=Image.open(final_path), size=size)
        except Exception as e:
            print(f"Error loading CTk image {final_path}: {e}")
            return None
    else:
        return None

# --- 4. DATABASE FUNCTIONS ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT,
            course TEXT,
            location TEXT
        )
    """)
    conn.commit()
    conn.close()

def fetch_students(search_query="", course_filter=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    query = "SELECT student_id, name, course, location FROM students WHERE 1=1"
    params = []
    if course_filter:
        query += " AND course LIKE ?"
        params.append(f"%{course_filter}%")
    if search_query:
        query += " AND (student_id LIKE ? OR name LIKE ?)"
        params.append(f"%{search_query}%")
        params.append(f"%{search_query}%")
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "course": r[2], "loc": r[3]} for r in rows]

def save_student_to_db(sid, name, course, loc):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?)", (sid, name, course, loc))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def delete_student_from_db(sid):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE student_id = ?", (sid,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def update_student_location(sid, new_loc):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("UPDATE students SET location = ? WHERE student_id = ?", (new_loc, sid))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

# --- 5. MAIN APPLICATION ---
class LocatRApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LocatR - Student Record Locator System")
        self.geometry("1360x800")
        self.configure(fg_color=COLOR_BG)

        try:
            myappid = 'locatr.registrar.system.v1'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        icon_abs_path = get_absolute_path("assets/frame0/app-icon.png")
        if icon_abs_path:
            try:
                pil_img = Image.open(icon_abs_path)
                self.icon_photo = ImageTk.PhotoImage(pil_img)
                self.tk.call('wm', 'iconphoto', self._w, self.icon_photo)
            except Exception as e:
                print(f"Could not set window icon: {e}")

        # --- GRID LAYOUT UPDATE ---
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=0) # Separator
        self.grid_columnconfigure(2, weight=1) # Main Content
        self.grid_rowconfigure(0, weight=1)

        init_db()
        self.current_view_data = None
        
        # Load Resources
        self.loaded_icons = {}
        for college, data in UNIVERSITY_STRUCTURE.items():
             self.loaded_icons[college] = load_icon_ctk(data["icon_path"])
        
        self.full_branding_img = load_icon_ctk("assets/frame0/full_branding.png", size=(250, 60))
        
        self.setup_sidebar()
        self.setup_main_area()
        
        # --- FIX: FORCE FOCUS STEALING ---
        # This binds a click event to the main window. If you click anywhere
        # that ISN'T the search entry, it focusses the window, causing the 
        # search entry to lose focus and trigger the cleanup.
        def global_focus_handler(event):
            try:
                # Check if the clicked widget is the search entry's internal entry widget
                if event.widget != self.search_entry._entry:
                    self.focus() # Force focus to main window
            except:
                pass
        
        self.bind("<Button-1>", global_focus_handler)

        self.show_homepage()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=360, corner_radius=0, fg_color=COLOR_SIDEBAR)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # --- SEPARATOR LINE (VERTICAL) ---
        self.separator = ctk.CTkFrame(self, width=2, fg_color=COLOR_SEPARATOR)
        self.separator.grid(row=0, column=1, sticky="ns", padx=(0,0))

        # --- 1. CLICKABLE LOGO ---
        logo_btn = ctk.CTkButton(
            self.sidebar, 
            fg_color="transparent", 
            hover_color=COLOR_BG,
            command=self.show_homepage
        )
        logo_btn.pack(pady=(30, 20), padx=30, anchor="w")
        
        if self.full_branding_img:
            logo_btn.configure(text="", image=self.full_branding_img, width=250, anchor="w")
        else:
            logo_btn.configure(text="LocatR System", font=(FONT_MAIN, 24, "bold"), text_color=COLOR_ACCENT, anchor="w")

        # --- 2. USER INFO ---
        profile_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        profile_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        info_frame = ctk.CTkFrame(profile_frame, fg_color="transparent")
        info_frame.pack(side="left")
        ctk.CTkLabel(info_frame, text="Office of the University Registrar", font=(FONT_MAIN, 14, "bold"), text_color="black").pack(anchor="w")
        ctk.CTkLabel(info_frame, text="USTP CDO", font=(FONT_MAIN, 12), text_color="gray").pack(anchor="w")

        # --- 3. ADD BUTTON ---
        self.add_btn = ctk.CTkButton(
            self.sidebar, 
            text="+ Add Student",
            font=(FONT_MAIN, 14, "bold"),
            fg_color=COLOR_ACCENT,
            text_color="white",
            height=50,
            corner_radius=8,
            command=self.open_add_modal
        )
        self.add_btn.pack(fill="x", padx=30, pady=(10, 10))

        # --- 4. HOME BUTTON ---
        self.home_btn = ctk.CTkButton(
            self.sidebar,
            text="Home",
            compound="left",
            anchor="w",
            fg_color="transparent",
            text_color=COLOR_ACCENT,
            hover_color=COLOR_HOVER,
            font=(FONT_MAIN, 14, "bold"), 
            height=40,
            command=self.show_homepage
        )
        self.home_btn.pack(fill="x", padx=30, pady=(5, 5))

        # --- 5. HORIZONTAL SEPARATOR LINE ---
        self.sidebar_line = ctk.CTkFrame(self.sidebar, height=2, fg_color=COLOR_SEPARATOR)
        self.sidebar_line.pack(fill="x", padx=30, pady=(10, 15))

        # --- 6. CATEGORY LABEL ---
        ctk.CTkLabel(self.sidebar, text="ACADEMIC UNITS", text_color="gray", font=(FONT_MAIN, 11, "bold")).pack(anchor="w", padx=30, pady=(0,5))
        
        # --- 7. SCROLLABLE LIST ---
        self.nav_frame = ctk.CTkScrollableFrame(self.sidebar, width=340, fg_color="transparent", 
                                                scrollbar_button_color="white", scrollbar_button_hover_color="white")
        self.nav_frame.pack(fill="both", expand=True, pady=5)

        for college, data in UNIVERSITY_STRUCTURE.items():
            display_name = college
            if len(display_name) > 38:
                display_name = display_name[:36] + "..."
            
            icon_img = self.loaded_icons.get(college)
            
            sidebar_btn = ctk.CTkButton(
                self.nav_frame,
                text=f"  {display_name}",
                image=icon_img,
                compound="left",
                anchor="w",
                fg_color="transparent",
                text_color=COLOR_TEXT_NAV,
                hover_color=COLOR_HOVER,
                font=(FONT_MAIN, 12),
                height=45,
                command=lambda c=college: self.show_program_grid(c)
            )
            sidebar_btn.pack(fill="x", pady=2, padx=15)

    def setup_main_area(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=COLOR_BG)
        self.main_frame.grid(row=0, column=2, sticky="nsew", padx=(40, 0), pady=40)

        self.top_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.top_bar.pack(fill="x", pady=(0, 10), padx=(0, 40))

        self.search_entry = ctk.CTkEntry(
            self.top_bar,
            placeholder_text="Search Student ID or Name...",
            width=300,
            height=40,
            corner_radius=20,
            border_width=1,
            border_color="#CBD5E1",
            fg_color="white",
            text_color="black",
            font=(FONT_MAIN, 12)
        )
        self.search_entry.pack(side="right")
        self.search_entry.bind("<Return>", self.perform_search)
        
        # --- FIX: CLEAR SEARCH BAR ON FOCUS OUT ---
        def on_search_focus_out(event):
            # This deletes the text, which forces CustomTkinter to show the placeholder again
            self.search_entry.delete(0, "end")
            
        self.search_entry.bind("<FocusOut>", on_search_focus_out)

        self.sticky_header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.sticky_header.pack(fill="x", padx=(0, 40)) 

        self.content_area = ctk.CTkScrollableFrame(
            self.main_frame, 
            fg_color="transparent",
            scrollbar_button_color="#F1F5F9",        
            scrollbar_button_hover_color="#CBD5E1",  
            width=900                                
        )
        self.content_area.pack(fill="both", expand=True)

    def render_student_table_header(self, parent_frame, show_program=False):
        thead = ctk.CTkFrame(parent_frame, fg_color="transparent", height=30)
        thead.pack(fill="x", pady=(10, 5))
        
        ctk.CTkLabel(thead, text="Student ID", font=(FONT_MAIN, 12, "bold"), text_color="black", width=120, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(thead, text="Name", font=(FONT_MAIN, 12, "bold"), text_color="black", width=250, anchor="w").pack(side="left", padx=10)
        
        if show_program:
            ctk.CTkLabel(thead, text="Program", font=(FONT_MAIN, 12, "bold"), text_color="black", width=250, anchor="w").pack(side="left", padx=10)
            
        ctk.CTkLabel(thead, text="Location", font=(FONT_MAIN, 12, "bold"), text_color="black", width=120, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(thead, text="Actions", font=(FONT_MAIN, 12, "bold"), text_color="black", width=160, anchor="center").pack(side="right", padx=10)

    def render_student_row(self, parent_frame, s, show_program=False):
        row = ctk.CTkFrame(parent_frame, fg_color="white", corner_radius=6, border_width=1, border_color="#F1F5F9", height=50)
        row.pack(fill="x", pady=2, padx=(0, 20))
        
        ctk.CTkLabel(row, text=s['id'], font=(FONT_MAIN, 13), text_color=COLOR_ACCENT, width=120, anchor="w").pack(side="left", padx=10)
        
        name_btn = ctk.CTkButton(
            row, 
            text=s['name'], 
            font=(FONT_MAIN, 13, "bold"), 
            text_color=COLOR_ACCENT, 
            fg_color="transparent", 
            hover_color=COLOR_HOVER,
            anchor="w",
            width=250,
            command=lambda sid=s['id'], name=s['name']: self.open_qr_modal(sid, name)
        )
        name_btn.pack(side="left", padx=10)
        
        if show_program:
            prog_txt = s['course']
            if len(prog_txt) > 35: prog_txt = prog_txt[:32] + "..."
            ctk.CTkLabel(row, text=prog_txt, font=(FONT_MAIN, 12), text_color="gray", width=250, anchor="w").pack(side="left", padx=10)

        loc_display = format_location_display(s['loc'])
        loc_col = COLOR_UP if "UP" in s['loc'] else COLOR_DOWN
        ctk.CTkLabel(row, text=loc_display, font=(FONT_MAIN, 12), text_color=loc_col, width=120, anchor="w").pack(side="left", padx=10)

        action_frame = ctk.CTkFrame(row, fg_color="transparent", width=160)
        action_frame.pack(side="right", padx=10)
        action_frame.grid_columnconfigure(0, weight=1)
        action_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkButton(action_frame, text="Edit", width=60, height=25, fg_color="#E0A800", font=(FONT_MAIN, 11),
                      command=lambda sid=s['id'], loc=s['loc']: self.open_edit_modal(sid, loc)).grid(row=0, column=0, padx=5)
        ctk.CTkButton(action_frame, text="Delete", width=60, height=25, fg_color="#DC2626", font=(FONT_MAIN, 11),
                      command=lambda sid=s['id']: self.delete_student(sid)).grid(row=0, column=1, padx=5)

    def show_homepage(self):
        self.clear_content()
        self.current_view_data = None

        title = ctk.CTkLabel(self.sticky_header, text="Academic Units", font=(FONT_MAIN, 28, "bold"), text_color=COLOR_ACCENT)
        title.pack(anchor="w", pady=(0, 10))
        
        subtitle = ctk.CTkLabel(self.sticky_header, text="Select a college or department to view programs.", font=(FONT_MAIN, 14), text_color="gray")
        subtitle.pack(anchor="w", pady=(0, 20))

        grid_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=(0, 20))
        grid_frame.grid_columnconfigure((0,1,2), weight=1)

        colleges = list(UNIVERSITY_STRUCTURE.keys())
        for i, col_name in enumerate(colleges):
            display_text = smart_break_text(col_name)
            icon = self.loaded_icons.get(col_name)

            card = ctk.CTkButton(
                grid_frame,
                text=display_text,
                image=icon,
                compound="top",
                font=(FONT_MAIN, 13, "bold"), 
                fg_color="white",
                text_color=COLOR_ACCENT,
                border_width=1,
                border_color="#E2E8F0",
                hover_color=COLOR_HOVER,
                height=150,
                corner_radius=12,
                command=lambda c=col_name: self.show_program_grid(c)
            )
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")

    def show_program_grid(self, college_name):
        self.clear_content()
        self.current_view_data = None
        
        title = ctk.CTkLabel(self.sticky_header, text="Academic Programs", font=(FONT_MAIN, 28, "bold"), text_color=COLOR_ACCENT)
        title.pack(anchor="w", pady=(0, 10))
        
        subtitle = ctk.CTkLabel(self.sticky_header, text=college_name, font=(FONT_MAIN, 16), text_color="gray")
        subtitle.pack(anchor="w", pady=(0, 20))

        grid_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=(0, 20))
        grid_frame.grid_columnconfigure((0,1,2), weight=1)

        programs = UNIVERSITY_STRUCTURE[college_name]["programs"]

        for i, prog in enumerate(programs):
            display_text = smart_break_text(prog["name"])
            card = ctk.CTkButton(
                grid_frame,
                text=display_text,
                font=(FONT_MAIN, 13, "bold"), 
                fg_color="white",
                text_color=COLOR_ACCENT,
                border_width=1,
                border_color="#E2E8F0",
                hover_color=COLOR_HOVER,
                height=100,
                corner_radius=12,
                command=lambda p=prog: self.show_student_list(p)
            )
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")

    def show_student_list(self, program_data):
        self.clear_content()
        self.current_view_data = program_data 
        
        header_row = ctk.CTkFrame(self.sticky_header, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, 20))
        
        college_of_program = "College of Information Technology and Computing" 
        for col, data in UNIVERSITY_STRUCTURE.items():
            if any(p == program_data for p in data["programs"]):
                college_of_program = col
                break
        
        back_btn = ctk.CTkButton(header_row, text="← Back", width=80, fg_color="#E2E8F0", text_color="black", hover_color="#CBD5E1", 
                                 font=(FONT_MAIN, 12), command=lambda: self.show_program_grid(college_of_program))
        back_btn.pack(side="left", padx=(0, 15))

        prog_title = program_data["name"]
        if len(prog_title) > 50: prog_title = prog_title[:47] + "..."
        ctk.CTkLabel(header_row, text=prog_title, font=(FONT_MAIN, 20, "bold"), text_color=COLOR_ACCENT).pack(side="left")

        self.render_student_table_header(self.sticky_header, show_program=False)

        students = fetch_students(course_filter=program_data["db_filter"])

        if not students:
            ctk.CTkLabel(self.content_area, text="No students found in this program.", text_color="gray", font=(FONT_MAIN, 12)).pack(pady=20, padx=(0, 20))

        for s in students:
            self.render_student_row(self.content_area, s, show_program=False)

    def perform_search(self, event=None):
        query = self.search_entry.get()
        if not query: return
        self.clear_content()
        self.current_view_data = None
        
        ctk.CTkLabel(self.sticky_header, text=f"Search Results for: '{query}'", font=(FONT_MAIN, 20, "bold"), text_color=COLOR_ACCENT).pack(anchor="w", pady=20)
        self.render_student_table_header(self.sticky_header, show_program=True)

        students = fetch_students(search_query=query)
        if not students:
            ctk.CTkLabel(self.content_area, text="No matching students found.", text_color="gray", font=(FONT_MAIN, 12)).pack(pady=20, padx=(0, 20))
            return

        for s in students:
            self.render_student_row(self.content_area, s, show_program=True)

    # --- QR MODAL ---
    def open_qr_modal(self, sid, name):
        toplevel = ctk.CTkToplevel(self)
        toplevel.geometry("350x480")
        toplevel.title(f"QR for {sid}")
        
        if hasattr(self, 'icon_photo'):
             toplevel.after(200, lambda: toplevel.iconphoto(False, self.icon_photo))
        
        toplevel.configure(fg_color="white")
        toplevel.attributes("-topmost", True)

        ctk.CTkLabel(toplevel, text="Student Record QR", font=(FONT_MAIN, 18, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 10))

        qr_data = f"Student ID: {sid}\nName: {name}"
        qr_pil_img = None 
        
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_pil_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            qr_ctk_img = ctk.CTkImage(light_image=qr_pil_img, dark_image=qr_pil_img, size=(220, 220))
            
            ctk.CTkLabel(toplevel, text="", image=qr_ctk_img).pack(pady=10)
            ctk.CTkLabel(toplevel, text=name, font=(FONT_MAIN, 14, "bold"), text_color="black").pack(pady=(10,0))
            ctk.CTkLabel(toplevel, text=sid, font=(FONT_MAIN, 12), text_color="gray").pack()

        except Exception as e:
            ctk.CTkLabel(toplevel, text=f"Error generating QR: {e}", text_color="red").pack()
            return

        def save_qr_code():
            if qr_pil_img is None:
                messagebox.showerror("Error", "QR code image not generated.")
                return

            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile=f"QR_{sid}_{name.replace(' ', '_')}.png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )

            if file_path:
                try:
                    qr_pil_img.save(file_path)
                    messagebox.showinfo("Success", f"QR Code saved to:\n{file_path}")
                except Exception as e:
                    messagebox.showerror("Save Error", f"Failed to save file: {e}")

        save_btn = ctk.CTkButton(toplevel, text="💾 Save QR Code (PNG)", fg_color=COLOR_UP, hover_color="#047857", width=220, command=save_qr_code)
        save_btn.pack(pady=(15, 5))
        ctk.CTkButton(toplevel, text="Close", fg_color=COLOR_NEUTRAL, hover_color=COLOR_NEUTRAL_HOVER, width=220, command=toplevel.destroy).pack(pady=(5, 20))

    # --- MODALS ---
    def open_add_modal(self):
        toplevel = ctk.CTkToplevel(self)
        toplevel.geometry("450x650") 
        toplevel.title("Add Student")
        if hasattr(self, 'icon_photo'):
             toplevel.after(200, lambda: toplevel.iconphoto(False, self.icon_photo))
             
        toplevel.configure(fg_color="white")
        toplevel.attributes("-topmost", True)

        ctk.CTkLabel(toplevel, text="Add New Student", font=(FONT_MAIN, 22, "bold"), text_color=COLOR_ACCENT).pack(pady=(20, 5))

        def create_entry(label_text):
            ctk.CTkLabel(toplevel, text=label_text, text_color="gray", font=(FONT_MAIN, 12), anchor="w").pack(fill="x", padx=40, pady=(2,0)) 
            entry = ctk.CTkEntry(toplevel, fg_color="#F8FAFC", border_width=1, border_color="#E2E8F0", text_color="black", height=35, font=(FONT_MAIN, 12))
            entry.pack(fill="x", padx=40, pady=(2, 0)) 
            err = ctk.CTkLabel(toplevel, text="", text_color=COLOR_ERROR, font=(FONT_MAIN, 10), anchor="w")
            err.pack(fill="x", padx=40, pady=(0, 0))
            return entry, err

        entry_id, err_id = create_entry("Student ID")
        entry_name, err_name = create_entry("Full Name")

        ctk.CTkLabel(toplevel, text="College", text_color="gray", font=(FONT_MAIN, 12), anchor="w").pack(fill="x", padx=40, pady=(2,0)) 
        college_names = list(UNIVERSITY_STRUCTURE.keys())
        
        # --- FIX: ROBUST HOVER LOGIC FOR COMBOBOX ---
        combo_college = ctk.CTkComboBox(
            toplevel, 
            values=college_names, 
            height=35, 
            border_color="#E2E8F0", 
            fg_color="#F8FAFC", 
            text_color="black", 
            dropdown_fg_color="white", 
            dropdown_text_color="black", 
            font=(FONT_MAIN, 12),
            state="readonly",
            button_color="#CBD5E1",
            button_hover_color="#1A1851"
        )
        combo_college.pack(fill="x", padx=40, pady=(2, 0))
        combo_college.set("Select College") 

        # Bind Hand Cursor to EVERY part of the combobox (Frame, Entry, Canvas)
        def set_hand(e):
            combo_college.configure(cursor="hand2")
            combo_college._entry.configure(cursor="hand2")
            combo_college._canvas.configure(cursor="hand2")
        def set_arrow(e):
            combo_college.configure(cursor="")
            combo_college._entry.configure(cursor="")
            combo_college._canvas.configure(cursor="")
            
        combo_college.bind("<Enter>", set_hand)
        combo_college.bind("<Leave>", set_arrow)
        combo_college._entry.bind("<Enter>", set_hand)
        combo_college._entry.bind("<Leave>", set_arrow)
        combo_college._canvas.bind("<Enter>", set_hand)
        combo_college._canvas.bind("<Leave>", set_arrow)

        ctk.CTkLabel(toplevel, text="Program", text_color="gray", font=(FONT_MAIN, 12), anchor="w").pack(fill="x", padx=40, pady=(5,0)) 
        
        combo_program = ctk.CTkComboBox(
            toplevel, 
            values=[], 
            height=35, 
            border_color="#E2E8F0", 
            fg_color="#F8FAFC", 
            text_color="black", 
            dropdown_fg_color="white", 
            dropdown_text_color="black", 
            font=(FONT_MAIN, 12),
            state="readonly",
            button_color="#CBD5E1",
            button_hover_color="#1A1851"
        )
        combo_program.pack(fill="x", padx=40, pady=(2, 0))
        combo_program.set("Select College First")
        
        # Bind Hand Cursor to Program Dropdown too
        def set_hand_prog(e):
            combo_program.configure(cursor="hand2")
            combo_program._entry.configure(cursor="hand2")
            combo_program._canvas.configure(cursor="hand2")
        def set_arrow_prog(e):
            combo_program.configure(cursor="")
            combo_program._entry.configure(cursor="")
            combo_program._canvas.configure(cursor="")

        combo_program.bind("<Enter>", set_hand_prog)
        combo_program.bind("<Leave>", set_arrow_prog)
        combo_program._entry.bind("<Enter>", set_hand_prog)
        combo_program._entry.bind("<Leave>", set_arrow_prog)
        combo_program._canvas.bind("<Enter>", set_hand_prog)
        combo_program._canvas.bind("<Leave>", set_arrow_prog)

        err_prog = ctk.CTkLabel(toplevel, text="", text_color=COLOR_ERROR, font=(FONT_MAIN, 10), anchor="w")
        err_prog.pack(fill="x", padx=40)

        def update_programs(choice):
            selected_college = choice
            if selected_college in UNIVERSITY_STRUCTURE:
                programs_list = [p["name"] for p in UNIVERSITY_STRUCTURE[selected_college]["programs"]]
                combo_program.configure(values=programs_list)
                combo_program.set(programs_list[0])
            else:
                combo_program.configure(values=[])
                combo_program.set("No Programs Found")

        combo_college.configure(command=update_programs)

        def validate_inputs(event=None):
            sid = entry_id.get().strip()
            if len(sid) > 0 and (not sid.isdigit() or len(sid) > 10):
                err_id.configure(text="❌ ID must be 10 digits (Numbers only)")
            elif len(sid) > 0 and len(sid) != 10:
                err_id.configure(text="⚠️ Must be exactly 10 digits")
            else:
                err_id.configure(text="")

            name = entry_name.get()
            if len(name) > 0 and not name[0].isupper():
                 err_name.configure(text="⚠️ Capitalize first letter")
            else:
                 err_name.configure(text="")

        entry_id.bind("<KeyRelease>", validate_inputs)
        entry_name.bind("<KeyRelease>", validate_inputs)

        ctk.CTkLabel(toplevel, text="Location", text_color="gray", font=(FONT_MAIN, 12), anchor="w").pack(fill="x", padx=40, pady=(5,2)) 
        loc_var = ctk.StringVar(value="UP")
        radio_frame = ctk.CTkFrame(toplevel, fg_color="transparent")
        radio_frame.pack(fill="x", padx=40)
        ctk.CTkRadioButton(radio_frame, text="Upper Floor", variable=loc_var, value="UP", text_color="black", font=(FONT_MAIN, 12)).pack(side="left", padx=10)
        ctk.CTkRadioButton(radio_frame, text="Lower Floor", variable=loc_var, value="DOWN", text_color="black", font=(FONT_MAIN, 12)).pack(side="left", padx=10)

        def save_action():
            sid = entry_id.get().strip()
            name = entry_name.get().strip()
            prog = combo_program.get()
            loc = loc_var.get()
            
            name = name.title()

            if len(sid) != 10 or not sid.isdigit():
                err_id.configure(text="❌ Cannot Save: Invalid ID")
                return
            
            if prog == "Select College First" or prog == "" or prog == "No Programs Found":
                err_prog.configure(text="❌ Please select a valid program")
                return

            if save_student_to_db(sid, name, prog, loc):
                messagebox.showinfo("Success", "Student Added")
                toplevel.destroy()
                if self.current_view_data: self.show_student_list(self.current_view_data)
            else:
                messagebox.showerror("Error", "Student ID already exists.")

        ctk.CTkButton(toplevel, text="Save Student", fg_color=COLOR_ACCENT, height=45, font=(FONT_MAIN, 14, "bold"), command=save_action).pack(fill="x", padx=40, pady=20)

    def open_edit_modal(self, sid, current_loc):
        toplevel = ctk.CTkToplevel(self)
        toplevel.geometry("300x250")
        toplevel.title("Edit Location")
        if hasattr(self, 'icon_photo'):
             toplevel.after(200, lambda: toplevel.iconphoto(False, self.icon_photo))

        toplevel.configure(fg_color="white")
        toplevel.attributes("-topmost", True)

        ctk.CTkLabel(toplevel, text=f"Edit Location for {sid}", font=(FONT_MAIN, 16, "bold"), text_color=COLOR_ACCENT).pack(pady=20)

        normalized_loc = "UP" if "UP" in current_loc or "Upper" in current_loc else "DOWN"
        loc_var = ctk.StringVar(value=normalized_loc)
        
        ctk.CTkRadioButton(toplevel, text="Upper Floor", variable=loc_var, value="UP", text_color="black").pack(pady=10)
        ctk.CTkRadioButton(toplevel, text="Lower Floor", variable=loc_var, value="DOWN", text_color="black").pack(pady=10)

        def update_action():
            if update_student_location(sid, loc_var.get()):
                messagebox.showinfo("Updated", "Location updated.")
                toplevel.destroy()
                if self.current_view_data: 
                    self.show_student_list(self.current_view_data)
                else:
                    self.perform_search()
        
        ctk.CTkButton(toplevel, text="Update", fg_color=COLOR_ACCENT, command=update_action).pack(pady=20)

    def delete_student(self, sid):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student {sid}?"):
            delete_student_from_db(sid)
            if self.current_view_data: 
                self.show_student_list(self.current_view_data)
            else:
                self.perform_search()

    def clear_content(self):
        # Clear sticky header widgets
        for widget in self.sticky_header.winfo_children():
            widget.destroy()
        # Clear scrollable content widgets
        for widget in self.content_area.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = LocatRApp()
    app.mainloop()