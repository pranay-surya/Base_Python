import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from tkinter import ttk 
import pymysql

# --- DATABASE CREDENTIALS ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "college"

# ==========================================================
#                         MAIN APPLICATION CLASS
# ==========================================================

class StudentManagementApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.button_font = tkfont.Font(family='Helvetica', size=12)

        self.title("Student Management System")
        self.geometry("1000x700") 

        # --- 1. GLOBAL HEADER FRAME ---
        header_frame = tk.Frame(self, bg='red', pady=15)
        header_frame.pack(fill='x') # Fills the top of the main window

        # Header Line 
        tk.Label(
            header_frame, 
            text="PRIYADARSHINI COLLEGE OF ENGINEERING", 
            font=('Helvetica', 20, 'bold'), 
            bg='red', 
            fg='white'
        ).pack(pady=(5, 2))

        # Header Line 2
        tk.Label(
            header_frame, 
            text="STUDENT MANAGEMENT SYSTEM", 
            font=('Helvetica', 16, 'bold'), 
            bg='red', 
            fg='white'
        ).pack(pady=(2, 5))
        # -------------------------------------------------------------------

        # --- 2. PAGE CONTAINER FRAME (Sits below the header) ---
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True) # Takes up remaining space
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Ensure the order is correct and all pages are included
        for F in (LoginPage, MainMenuPage, StudentMenuPage, AddStudentPage, DeleteStudentPage, MarksMenuPage, ListStudentPage, SearchStudentPage, MarksEntryPage, ListMarksPage, DeleteMarksPage, EditMarksPage, SearchMarksPage, ReportCardPage, ChangePasswordPage): 
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name in ["ListStudentPage", "SearchStudentPage", "ListMarksPage", "EditMarksPage", "SearchMarksPage"]:
            if hasattr(frame, 'refresh_list'): 
                frame.refresh_list()
        frame.tkraise()

    def create_db_connection(self):
        try:
            conn = pymysql.connect(
                host=DB_HOST, 
                user=DB_USER, 
                password=DB_PASSWORD, 
                db=DB_NAME
            )
            return conn
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")
            return None

# ==========================================================
#                         PAGE DEFINITIONS 
# (MainMenuPage header removed; LoginPage padding adjusted)
# ==========================================================

# 1. LOGIN PAGE (Removed old header, adjusted positioning)
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # --- Centered Login Panel ---
        # rely adjusted to 0.5 to keep it centered *within the page container*
        login_panel = tk.Frame(self, padx=30, pady=30, bd=2, relief=tk.RIDGE)
        login_panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label = tk.Label(login_panel, text="LOGIN PORTAL", font=controller.title_font)
        label.pack(pady=20)

        tk.Label(login_panel, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(login_panel, width=40)
        self.username_entry.pack(pady=9, ipady=5) 

        tk.Label(login_panel, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(login_panel, width=40, show="*")
        self.password_entry.pack(pady=9, ipady=5) 

        tk.Button(login_panel, text="Login",bg='red',fg='white', command=self.verify_login, font=controller.button_font).pack(pady=20)

        
    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT * FROM User_pass WHERE User = %s AND Pass = %s"
                cursor.execute(query, (username, password))
                if cursor.fetchone():
                    messagebox.showinfo("Login Success", "Welcome to the system!")
                    self.controller.show_frame("MainMenuPage")
                else:
                    messagebox.showerror("Login Failed", "Incorrect Username or Password.")
            except pymysql.Error as e:
                messagebox.showerror("Database Error", f"Login query failed: {e}")
            finally:
                conn.close()

# 2. MAIN MENU PAGE (Removed local header)
class MainMenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # The global header is now handled in StudentManagementApp.__init__

        tk.Label(self, text="MAIN MENU", font=controller.title_font).pack(pady=50) 
        
        tk.Button(self, text="STUDENT MENU", command=lambda: controller.show_frame("StudentMenuPage"), font=controller.button_font, width=25).pack(pady=10)
        tk.Button(self, text="MARK ENTRY MENU", command=lambda: controller.show_frame("MarksMenuPage"), font=controller.button_font, width=25).pack(pady=10)
        tk.Button(self, text="REPORT CARD", command=lambda: controller.show_frame("ReportCardPage"), font=controller.button_font, width=25).pack(pady=10)
        
        tk.Button(self, text="CHANGE PASSWORD", command=lambda: controller.show_frame("ChangePasswordPage"), font=controller.button_font, width=25).pack(pady=10)
        
        tk.Button(self, text="EXIT", command=controller.destroy, font=controller.button_font, width=25, bg='red', fg='white').pack(pady=30)

# 3. STUDENT MENU PAGE
class StudentMenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="STUDENT MENU", font=controller.title_font).pack(pady=30)
        tk.Button(self, text="ADD NEW STUDENT", command=lambda: controller.show_frame("AddStudentPage"), font=controller.button_font, width=30).pack(pady=10)
        tk.Button(self, text="DELETE STUDENT RECORD", command=lambda: controller.show_frame("DeleteStudentPage"), font=controller.button_font, width=30).pack(pady=10)
        tk.Button(self, text="LIST ALL STUDENTS", command=lambda: controller.show_frame("ListStudentPage"), font=controller.button_font, width=30).pack(pady=10)
        tk.Button(self, text="SEARCH STUDENT", command=lambda: controller.show_frame("SearchStudentPage"), font=controller.button_font, width=30).pack(pady=10)
        tk.Button(self, text="BACK TO MAIN MENU", command=lambda: controller.show_frame("MainMenuPage"), font=controller.button_font, bg='red', fg='white', width=30).pack(pady=30)

# 4. ADD STUDENT PAGE
class AddStudentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="ADD NEW STUDENT", font=controller.title_font).pack(pady=20)
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)
        labels = ["Roll Number:", "Name:", "Gender (M/F):", "DOB (YYYY-MM-DD):", "Address:", "Phone Number:", "Course:", "Section:"]
        self.entries = {}
        for i, text in enumerate(labels):
            tk.Label(form_frame, text=text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            simple_key = text.split(':')[0].split('(')[0].strip().replace(' ', '_')
            self.entries[simple_key] = entry 
        tk.Button(self, text="Save Student", command=self.add_new_student_db, font=controller.button_font).pack(pady=10)
        tk.Button(self, text="BACK TO STUDENT MENU", command=lambda: controller.show_frame("StudentMenuPage"), font=controller.button_font, bg='red', fg='white').pack(pady=10)
    def clear_fields(self):
        for entry_widget in self.entries.values():
            entry_widget.delete(0, tk.END)
    def add_new_student_db(self):
        try:
            roll_input = self.entries["Roll_Number"].get().strip()
            phone_input = self.entries["Phone_Number"].get().strip()
            
            if not roll_input or not phone_input or not roll_input.isdigit() or not phone_input.isdigit():
                raise ValueError("Roll Number and Phone Number fields cannot be empty.")
                
            trno = int(roll_input)
            tphone = int(phone_input)
            
            tname = self.entries["Name"].get()
            tgender = self.entries["Gender"].get()
            tdob = self.entries["DOB"].get()
            taddress = self.entries["Address"].get()
            tcourse = self.entries["Course"].get()
            tsec = self.entries["Section"].get()
        except ValueError:
            messagebox.showerror("Input Error", "Roll Number and Phone Number must be valid integers and cannot be empty.")
            return
        if not all([tname, tgender, tdob, taddress, tcourse, tsec]):
             messagebox.showerror("Input Error", "All fields must be filled.")
             return
        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                q = "INSERT INTO Student VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (trno, tname, tgender, tdob, taddress, tphone, tcourse, tsec)
                cursor.execute(q, val)
                conn.commit()
                messagebox.showinfo("Success", "Student information saved successfully!")
                self.clear_fields()
            except pymysql.IntegrityError:
                messagebox.showerror("DB Error", "Error: Roll Number might already exist or data integrity violation.")
            except pymysql.Error as e:
                messagebox.showerror("DB Error", f"Database insertion failed: {e}")
            finally:
                conn.close()

# 5. DELETE STUDENT PAGE
class DeleteStudentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="DELETE STUDENT RECORD", font=controller.title_font).pack(pady=40)
        tk.Label(self, text="Enter Roll Number to Delete:").pack(pady=5)
        self.roll_entry = tk.Entry(self, width=30)
        self.roll_entry.pack(pady=5)
        tk.Button(self, text="Delete Record", command=self.delete_student_db, font=controller.button_font, bg='red', fg='white').pack(pady=20)
        tk.Button(self, text="BACK TO STUDENT MENU", command=lambda: controller.show_frame("StudentMenuPage"), font=controller.button_font, bg='red', fg='white').pack(pady=10)
    def delete_student_db(self):
        try:
            roll_input = self.roll_entry.get().strip()
            if not roll_input or not roll_input.isdigit(): raise ValueError("Invalid Roll Number.")
            roll_no = int(roll_input)
        except ValueError:
            messagebox.showerror("Input Error", "Roll Number must be an integer and cannot be empty.")
            return
        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Student WHERE Roll_no = %s", (roll_no,))
                if not cursor.fetchone():
                    messagebox.showerror("Error", f"Student with Roll Number {roll_no} not found.")
                    return
                if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete student {roll_no}?"):
                    cursor.execute("DELETE FROM Student WHERE Roll_no = %s", (roll_no,))
                    conn.commit()
                    messagebox.showinfo("Success", "Student record successfully deleted!")
                    self.roll_entry.delete(0, tk.END)
            except pymysql.Error as e:
                messagebox.showerror("DB Error", f"Deletion failed: {e}")
            finally:
                conn.close()

# 6. LIST STUDENT PAGE
class ListStudentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="LIST OF ALL STUDENTS", font=controller.title_font).pack(pady=20)
        table_frame = tk.Frame(self)
        table_frame.pack(pady=10, padx=10, fill='both', expand=True)
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        self.tree = ttk.Treeview(table_frame, columns=('Roll_no', 'Name', 'Gender', 'DOB', 'Address', 'Phone_no', 'Course', 'Section'),
                                 show='headings', yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        columns = {'Roll_no': 80, 'Name': 150, 'Gender': 70, 'DOB': 100, 'Address': 180, 'Phone_no': 120, 'Course': 100, 'Section': 70}
        for col, width in columns.items():
            self.tree.heading(col, text=col.replace('_', ' '))
            self.tree.column(col, width=width, anchor='center')
        tk.Button(self, text="BACK TO STUDENT MENU", command=lambda: controller.show_frame("StudentMenuPage"), font=controller.button_font, bg='red', fg='white').pack(pady=10)
    def refresh_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Roll_no, Name, Gender, DOB, Address, Phone_no, Course, Section FROM Student")
                records = cursor.fetchall()
                for row in records:
                    self.tree.insert('', tk.END, values=row)
            except pymysql.Error as e:
                messagebox.showerror("DB Error", f"Failed to fetch student list: {e}")
            finally:
                conn.close()

# 7. SEARCH STUDENT PAGE
class SearchStudentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="SEARCH STUDENT RECORD", font=controller.title_font).pack(pady=20)
        controls_frame = tk.Frame(self)
        controls_frame.pack(pady=10)
        self.search_var = tk.StringVar(value="Roll_no")
        tk.Label(controls_frame, text="Search By:").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(controls_frame, text="Roll Number", variable=self.search_var, value="Roll_no").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(controls_frame, text="Name", variable=self.search_var, value="Name").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(controls_frame, text="Course", variable=self.search_var, value="Course").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(controls_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=10)
        tk.Button(controls_frame, text="Search", command=self.execute_search, font=controller.button_font).pack(side=tk.LEFT, padx=10)
        table_frame = tk.Frame(self)
        table_frame.pack(pady=10, padx=10, fill='both', expand=True)
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        self.tree = ttk.Treeview(table_frame, columns=('Roll_no', 'Name', 'Gender', 'DOB', 'Address', 'Phone_no', 'Course', 'Section'), show='headings', yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        columns = {'Roll_no': 80, 'Name': 150, 'Gender': 70, 'DOB': 100, 'Address': 180, 'Phone_no': 120, 'Course': 100, 'Section': 70}
        for col, width in columns.items():
            self.tree.heading(col, text=col.replace('_', ' '))
            self.tree.column(col, width=width, anchor='center')
        tk.Button(self, text="BACK TO STUDENT MENU", command=lambda: controller.show_frame("StudentMenuPage"), font=controller.button_font, bg='red', fg='white').pack(pady=10)
        self.execute_search(initial_load=True) 
    def clear_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
    def execute_search(self, initial_load=False):
        self.clear_treeview()
        search_term = self.search_entry.get().strip()
        search_by = self.search_var.get()
        if not initial_load and not search_term:
            messagebox.showwarning("Input Required", "Please enter a value to search.")
            return
        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT Roll_no, Name, Gender, DOB, Address, Phone_no, Course, Section FROM Student"
                params = []
                if not initial_load:
                    if search_by in ["Roll_no", "Phone_no"]:
                        try:
                            if not search_term or not search_term.isdigit(): raise ValueError("Invalid")
                            search_val = int(search_term)
                            query += f" WHERE {search_by} = %s"
                            params = [search_val]
                        except ValueError:
                            messagebox.showerror("Input Error", f"Search term for {search_by} must be a number.")
                            return
                    else:
                        query += f" WHERE {search_by} LIKE %s"
                        params = [f"%{search_term}%"]
                cursor.execute(query, tuple(params))
                records = cursor.fetchall()
                if not records and not initial_load:
                    messagebox.showinfo("Search Result", "No student records found matching your criteria.")
                for row in records:
                    self.tree.insert('', tk.END, values=row)
            except pymysql.Error as e:
                messagebox.showerror("DB Error", f"Failed to execute search: {e}")
            finally:
                conn.close()
    def refresh_list(self):
        self.search_entry.delete(0, tk.END)
        self.search_var.set("Roll_no")
        self.execute_search(initial_load=True)

# 14. MARKS MENU PAGE
class MarksMenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="MARKS ENTRY MENU", font=controller.title_font).pack(pady=30)

        tk.Button(self, text="MARKS ENTRY", command=lambda: controller.show_frame("MarksEntryPage"), font=controller.button_font, width=30).pack(pady=10)
        tk.Button(self, text="DELETE MARKS ENTRY", command=lambda: controller.show_frame("DeleteMarksPage"), font=controller.button_font, width=30).pack(pady=10)
        tk.Button(self, text="EDIT MARKS ENTRY", command=lambda: controller.show_frame("EditMarksPage"), font=controller.button_font, width=30).pack(pady=10)
        tk.Button(self, text="SEARCH MARKS ENTRY", command=lambda: controller.show_frame("SearchMarksPage"), font=controller.button_font, width=30).pack(pady=10)
        tk.Button(self, text="LIST MARKS", command=lambda: controller.show_frame("ListMarksPage"), font=controller.button_font, width=30).pack(pady=10)

        tk.Button(self, text="BACK TO MAIN MENU", command=lambda: controller.show_frame("MainMenuPage"), font=controller.button_font, bg='red', fg='white', width=30).pack(pady=30)


# 8. MARKS ENTRY PAGE
class MarksEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="STUDENT MARKS ENTRY", font=controller.title_font).pack(pady=20)
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)
        labels = ["Roll Number:", "English:", "Maths:", "Biology:", "Chemistry:", "CS:"]
        self.entries = {}
        for i, text in enumerate(labels):
            tk.Label(form_frame, text=text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            simple_key = text.split(':')[0].strip().replace(' ', '_')
            self.entries[simple_key] = entry 
        tk.Button(self, text="Save Marks", command=self.marks_entry_db, font=controller.button_font).pack(pady=10)
        tk.Button(self, text="BACK TO MARKS MENU", command=lambda: controller.show_frame("MarksMenuPage"), font=controller.button_font, bg='red', fg='white').pack(pady=10)
    def clear_fields(self):
        for entry_widget in self.entries.values():
            entry_widget.delete(0, tk.END)
    def calculate_grade(self, percentage):
        if percentage >= 80: return 'A'
        elif percentage >= 60: return 'B'
        elif percentage >= 40: return 'C'
        else: return 'F'
    def marks_entry_db(self):
        try:
            roll_input = self.entries["Roll_Number"].get().strip()
            if not roll_input or not roll_input.isdigit(): raise ValueError("Roll Number invalid.")
            rno = int(roll_input)
            
            m_eng = int(self.entries["English"].get().strip())
            m_maths = int(self.entries["Maths"].get().strip())
            m_bio = int(self.entries["Biology"].get().strip())
            m_chem = int(self.entries["Chemistry"].get().strip())
            m_cs = int(self.entries["CS"].get().strip())
        except ValueError:
            messagebox.showerror("Input Error", "Roll Number and all Subject Scores must be valid numbers and cannot be empty.")
            return
        total = m_eng + m_maths + m_bio + m_chem + m_cs
        percentage = total * 100 / 500
        grade = self.calculate_grade(percentage)
        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                q = """
                INSERT INTO marks_1 (Roll_no, English, Maths, Biology, Chemistry, CS, Total, Percentage, Grade)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                val = (rno, m_eng, m_maths, m_bio, m_chem, m_cs, total, percentage, grade)
                cursor.execute(q, val)
                conn.commit()
                messagebox.showinfo("Success", f"Marks saved successfully for Roll {rno}. Grade: {grade}")
                self.clear_fields()
            except pymysql.IntegrityError:
                messagebox.showerror("DB Error", "Error: Roll Number might not exist in Student table or marks already entered (Duplicate Key).")
            except pymysql.Error as e:
                messagebox.showerror("DB Error", f"Database insertion failed: {e}")
            finally:
                conn.close()

# 9. LIST MARKS PAGE
class ListMarksPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="LIST OF STUDENT MARKS", font=controller.title_font).pack(pady=20)
        table_frame = tk.Frame(self)
        table_frame.pack(pady=10, padx=10, fill='both', expand=True)
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        columns = ['Roll_no', 'English', 'Maths', 'Biology', 'Chemistry', 'CS', 'Total', 'Percentage', 'Grade']
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        column_widths = {'Roll_no': 80, 'Total': 80, 'Percentage': 100, 'Grade': 70}
        for col in columns:
            width = column_widths.get(col, 80)
            self.tree.heading(col, text=col.replace('_', ' '))
            self.tree.column(col, width=width, anchor='center')
        tk.Button(self, text="BACK TO MARKS MENU", command=lambda: controller.show_frame("MarksMenuPage"), font=controller.button_font, bg='red', fg='white').pack(pady=10)
    def refresh_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Roll_no, English, Maths, Biology, Chemistry, CS, Total, Percentage, Grade FROM marks_1")
                records = cursor.fetchall()
                for row in records:
                    row_list = list(row)
                    if row_list[7] is not None:
                        row_list[7] = f"{row_list[7]:.2f}" 
                    self.tree.insert('', tk.END, values=row_list)
            except pymysql.Error as e:
                messagebox.showerror("DB Error", f"Failed to fetch marks list: {e}. Check your 'marks_1' table columns and privileges.")
            finally:
                conn.close()

# 10. DELETE MARKS PAGE
class DeleteMarksPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="DELETE MARKS ENTRY", font=controller.title_font).pack(pady=40)
        tk.Label(self, text="Enter Roll Number to Delete Marks:").pack(pady=5)
        self.roll_entry = tk.Entry(self, width=30)
        self.roll_entry.pack(pady=5)
        delete_btn = tk.Button(self, text="Delete Marks Record", command=self.delete_marks_db, font=controller.button_font, bg='red', fg='white').pack(pady=20)
        tk.Button(self, text="BACK TO MARKS MENU", command=lambda: controller.show_frame("MarksMenuPage"), font=controller.button_font, bg='red', fg='white').pack(pady=10)
    def delete_marks_db(self):
        try:
            roll_input = self.roll_entry.get().strip()
            if not roll_input or not roll_input.isdigit(): raise ValueError("Invalid Roll Number.")
            roll_no = int(roll_input)
        except ValueError:
            messagebox.showerror("Input Error", "Roll Number must be an integer and cannot be empty.")
            return
        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Roll_no FROM marks_1 WHERE Roll_no = %s", (roll_no,))
                if not cursor.fetchone():
                    messagebox.showerror("Error", f"Marks record for Roll Number {roll_no} not found.")
                    return
                if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete marks for student {roll_no}?"):
                    q = "DELETE FROM marks_1 WHERE Roll_no = %s"
                    cursor.execute(q, (roll_no,))
                    conn.commit()
                    messagebox.showinfo("Success", "Marks record successfully deleted!")
                    self.roll_entry.delete(0, tk.END) 
            except pymysql.Error as e:
                messagebox.showerror("DB Error", f"Deletion failed: {e}")
            finally:
                conn.close()

# 11. EDIT MARKS PAGE
class EditMarksPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.current_roll = None 

        tk.Label(self, text="EDIT MARKS ENTRY", font=controller.title_font).pack(pady=20)

        lookup_frame = tk.Frame(self)
        lookup_frame.pack(pady=10)
        tk.Label(lookup_frame, text="Enter Roll Number to Edit:").pack(side=tk.LEFT, padx=5)
        self.roll_entry = tk.Entry(lookup_frame, width=15)
        self.roll_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(lookup_frame, text="Lookup", command=self.lookup_student_marks, font=controller.button_font).pack(side=tk.LEFT, padx=10)

        self.form_frame = tk.Frame(self)
        
        labels = ["English:", "Maths:", "Biology:", "Chemistry:", "CS:"]
        self.entries = {}
        for i, text in enumerate(labels):
            tk.Label(self.form_frame, text=text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(self.form_frame, width=15)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            simple_key = text.split(':')[0].strip()
            self.entries[simple_key] = entry 

        self.update_btn = tk.Button(self, text="Update Marks", command=self.update_marks_db, font=controller.button_font, state=tk.DISABLED)
        self.back_btn = tk.Button(self, text="BACK TO MARKS MENU", command=lambda: controller.show_frame("MarksMenuPage"), font=controller.button_font, bg='red', fg='white')
        
        self.update_btn.pack(pady=10)
        self.back_btn.pack(pady=10)
        
    def refresh_list(self):
        self.roll_entry.delete(0, tk.END)
        self.form_frame.pack_forget()
        self.update_btn.config(state=tk.DISABLED)
        self.current_roll = None
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def calculate_grade(self, percentage):
        if percentage >= 80: return 'A'
        elif percentage >= 60: return 'B'
        elif percentage >= 40: return 'C'
        else: return 'F'

    def lookup_student_marks(self):
        self.form_frame.pack_forget() 
        self.update_btn.config(state=tk.DISABLED)
        self.current_roll = None
        
        try:
            roll_input = self.roll_entry.get().strip()
            if not roll_input or not roll_input.isdigit(): raise ValueError("Invalid Roll Number.")
            roll_no = int(roll_input)
        except ValueError:
            messagebox.showerror("Input Error", "Roll Number must be an integer and cannot be empty.")
            return

        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT English, Maths, Biology, Chemistry, CS FROM marks_1 WHERE Roll_no = %s", (roll_no,))
                record = cursor.fetchone()

                if record:
                    self.current_roll = roll_no
                    self.form_frame.pack(pady=10)
                    
                    subject_keys = ["English", "Maths", "Biology", "Chemistry", "CS"]
                    for i, key in enumerate(subject_keys):
                        self.entries[key].delete(0, tk.END)
                        self.entries[key].insert(0, record[i])
                    
                    self.update_btn.config(state=tk.NORMAL)
                    messagebox.showinfo("Success", f"Marks loaded for Roll {roll_no}. Edit and click Update.")
                else:
                    messagebox.showerror("Error", f"Marks record for Roll Number {roll_no} not found.")

            except pymysql.Error as e:
                messagebox.showerror("DB Error", f"Lookup failed: {e}")
            finally:
                conn.close()

    def update_marks_db(self):
        if not self.current_roll:
            messagebox.showerror("Error", "Please lookup a Roll Number first.")
            return
            
        try:
            m_eng = int(self.entries["English"].get().strip())
            m_maths = int(self.entries["Maths"].get().strip())
            m_bio = int(self.entries["Biology"].get().strip())
            m_chem = int(self.entries["Chemistry"].get().strip())
            m_cs = int(self.entries["CS"].get().strip())
        except ValueError:
            messagebox.showerror("Input Error", "All subject scores must be valid numbers.")
            return

        total = m_eng + m_maths + m_bio + m_chem + m_cs
        percentage = total * 100 / 500
        grade = self.calculate_grade(percentage)

        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                q = """
                UPDATE marks_1 SET 
                English = %s, Maths = %s, Biology = %s, Chemistry = %s, CS = %s, 
                Total = %s, Percentage = %s, Grade = %s 
                WHERE Roll_no = %s
                """
                val = (m_eng, m_maths, m_bio, m_chem, m_cs, total, percentage, grade, self.current_roll)
                
                cursor.execute(q, val)
                conn.commit()
                messagebox.showinfo("Success", f"Marks for Roll {self.current_roll} updated successfully!")
                
                self.roll_entry.delete(0, tk.END)
                self.form_frame.pack_forget()
                self.update_btn.config(state=tk.DISABLED)
                self.current_roll = None

            except pymysql.Error as e:
                messagebox.showerror("DB Error", f"Update failed: {e}")
            finally:
                conn.close()

# 12. SEARCH MARKS PAGE
class SearchMarksPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="SEARCH MARKS ENTRY", font=controller.title_font).pack(pady=20)
        
        controls_frame = tk.Frame(self)
        controls_frame.pack(pady=10)
        
        tk.Label(controls_frame, text="Enter Roll Number:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(controls_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(controls_frame, text="Search", command=self.execute_search, font=controller.button_font).pack(side=tk.LEFT, padx=10)
        tk.Button(controls_frame, text="Show All", command=lambda: self.execute_search(initial_load=True), font=controller.button_font).pack(side=tk.LEFT, padx=10)

        table_frame = tk.Frame(self)
        table_frame.pack(pady=10, padx=10, fill='both', expand=True)

        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        columns = ['Roll_no', 'English', 'Maths', 'Biology', 'Chemistry', 'CS', 'Total', 'Percentage', 'Grade']
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree.pack(side='left', fill='both', expand=True)

        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')

        column_widths = {'Roll_no': 80, 'Total': 80, 'Percentage': 100, 'Grade': 70}
        for col in columns:
            width = column_widths.get(col, 80)
            self.tree.heading(col, text=col.replace('_', ' '))
            self.tree.column(col, width=width, anchor='center')
            
        tk.Button(self, text="BACK TO MARKS MENU", command=lambda: controller.show_frame("MarksMenuPage"), font=controller.button_font, bg='red', fg='white').pack(pady=10)
        
        self.refresh_list() 

    def clear_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
    def execute_search(self, initial_load=False):
        self.clear_treeview()
        search_term = self.search_entry.get().strip()
        
        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                if initial_load or not search_term:
                    query = "SELECT Roll_no, English, Maths, Biology, Chemistry, CS, Total, Percentage, Grade FROM marks_1"
                    params = ()
                else:
                    query = "SELECT Roll_no, English, Maths, Biology, Chemistry, CS, Total, Percentage, Grade FROM marks_1 WHERE Roll_no = %s"
                    
                    try:
                        if not search_term or not search_term.isdigit(): raise ValueError("Invalid")
                        search_val = int(search_term)
                        params = (search_val,)
                    except ValueError:
                        messagebox.showerror("Input Error", "Roll Number must be an integer.")
                        return

                cursor.execute(query, params)
                records = cursor.fetchall()

                if not records and not initial_load:
                    messagebox.showinfo("Search Result", f"No marks found for Roll Number {search_term}.")
                    
                for row in records:
                    row_list = list(row)
                    if row_list[7] is not None:
                        row_list[7] = f"{row_list[7]:.2f}" 
                    self.tree.insert('', tk.END, values=row_list)

            except pymysql.Error as e:
                messagebox.showerror("DB Error", f"Failed to execute search: {e}")
            finally:
                conn.close()

    def refresh_list(self):
        self.search_entry.delete(0, tk.END)
        self.execute_search(initial_load=True)

# 13. REPORT CARD PAGE
class ReportCardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.report_labels = {} 
        self.subject_labels = {} 
        
        self.subject_names = ["English", "Maths", "Biology", "Chemistry", "CS"]

        # Note: The 'PRIYADARSHANI COLLEGE OF ENGG - REPORT CARD' title remains here for page context
        tk.Label(self, text="REPORT CARD", font=controller.title_font).pack(pady=20)
        
        # --- Lookup Frame ---
        lookup_frame = tk.Frame(self)
        lookup_frame.pack(pady=10)
        tk.Label(lookup_frame, text="Enter Roll Number:").pack(side=tk.LEFT, padx=5)
        self.roll_entry = tk.Entry(lookup_frame, width=15)
        self.roll_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(lookup_frame, text="Generate Report", command=self.generate_report, font=controller.button_font).pack(side=tk.LEFT, padx=10)

        # --- Report Output Area (COMPACTED) ---
        self.output_frame = tk.Frame(self, padx=5, pady=15, bd=2, relief=tk.GROOVE) 
        self.output_frame.pack(pady=15, fill='x', padx=400) 

        # --- Student Details (Name, Roll, Course, Section) ---
        tk.Label(self.output_frame, text="STUDENT DETAILS", font=('Arial', 11, 'bold')).pack(pady=(5, 5))
        details_frame = tk.Frame(self.output_frame)
        details_frame.pack(pady=5, fill='x')
        
        details_frame.grid_columnconfigure(1, weight=1)
        details_frame.grid_columnconfigure(3, weight=1)

        labels = ["Roll:", "Name:", "Course:", "Section:"]
        keys = ["Roll_no", "Name", "Course", "Section"]
        
        for i, (text, key) in enumerate(zip(labels, keys)):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(details_frame, text=text, anchor='e').grid(row=row, column=col, padx=10, pady=2, sticky='e')
            data_label = tk.Label(details_frame, text="---", font=('Arial', 9, 'bold'), anchor='e')
            data_label.grid(row=row, column=col+1, padx=5, sticky='w')
            self.report_labels[key] = data_label
            
        # --- Subject-wise Marks (VERTICAL LAYOUT) ---
        tk.Label(self.output_frame, text="SUBJECT MARKS", font=('Arial', 11, 'bold')).pack(pady=(10, 5))
        subjects_frame = tk.Frame(self.output_frame, bd=1, relief=tk.GROOVE, padx=5, pady=5)
        subjects_frame.pack(pady=5, fill='x', padx=20)

        # Configure columns for Subject and Marks
        subjects_frame.grid_columnconfigure(0, weight=1) # Subject Name
        subjects_frame.grid_columnconfigure(1, weight=1) # Marks

        # Add Header Row
        tk.Label(subjects_frame, text="Subject", font=('Arial', 9, 'bold', 'underline')).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        tk.Label(subjects_frame, text="Marks", font=('Arial', 9, 'bold', 'underline')).grid(row=0, column=1, sticky='e', padx=5, pady=2)

        # Data Rows
        for i, name in enumerate(self.subject_names):
            tk.Label(subjects_frame, text=f"{name}:", anchor='w').grid(row=i + 1, column=0, padx=10, pady=1, sticky='w')
            
            data_label = tk.Label(subjects_frame, text="---", font=('Arial', 9), anchor='e')
            data_label.grid(row=i + 1, column=1, padx=10, pady=1, sticky='e')
            self.subject_labels[name] = data_label
            
        # --- Grade and Percentage Summary ---
        tk.Label(self.output_frame, text="PERFORMANCE SUMMARY", font=('Arial', 11, 'bold')).pack(pady=(15, 5))
        summary_frame = tk.Frame(self.output_frame)
        summary_frame.pack(pady=5, fill='x')
        
        summary_frame.grid_columnconfigure(1, weight=1)
        
        summary_labels = ["Total Marks Obtained:", "Percentage:", "Grade:"]
        summary_keys = ["Total", "Percentage", "Grade"]
        
        for i, (text, key) in enumerate(zip(summary_labels, summary_keys)):
            tk.Label(summary_frame, text=text, anchor='w').grid(row=i, column=0, padx=10, pady=2, sticky='w')
            data_label = tk.Label(summary_frame, text="---", font=('Arial', 9, 'bold'), anchor='w')
            data_label.grid(row=i, column=1, padx=10, sticky='w')
            self.report_labels[key] = data_label


        tk.Button(self, text="BACK TO MAIN MENU", command=lambda: controller.show_frame("MainMenuPage"), font=controller.button_font, bg='red', fg='white').pack(pady=10)

        self.clear_report()

    def clear_report(self):
        """Clears all displayed report data."""
        self.roll_entry.delete(0, tk.END)
        for label in self.report_labels.values():
            label.config(text="---")
        for label in self.subject_labels.values():
            label.config(text="---")

    def generate_report(self):
        """Fetches and displays the student's report card data."""
        roll_input = self.roll_entry.get().strip()
        self.clear_report() 

        try:
            if not roll_input: raise ValueError("Roll Number is empty.")
            if not roll_input.isdigit(): raise ValueError("Roll Number must be a digit.")
            roll_no = int(roll_input)
        except ValueError:
            messagebox.showerror("Input Error", "Roll Number must be an integer and cannot be empty.")
            return

        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Fetch Student Name, Course, Section
                student_query = "SELECT Name, Course, Section FROM Student WHERE Roll_no = %s"
                cursor.execute(student_query, (roll_no,))
                student_detail = cursor.fetchone()
                if not student_detail:
                    messagebox.showerror("Error", f"Student {roll_no} not found.")
                    return
                
                # Fetch Marks using actual subject names
                marks_columns = ", ".join(self.subject_names) 
                
                marks_query = f"SELECT Total, Percentage, Grade, {marks_columns} FROM marks_1 WHERE Roll_no = %s"
                cursor.execute(marks_query, (roll_no,))
                marks_record = cursor.fetchone() 
                
                if not marks_record:
                    messagebox.showerror("Error", f"Marks record for Roll Number {roll_no} not found in marks_1 table.")
                    return
                
                # --- Update Student Details ---
                self.report_labels['Roll_no'].config(text=str(roll_no))
                self.report_labels['Name'].config(text=student_detail[0])
                self.report_labels['Course'].config(text=student_detail[1])
                self.report_labels['Section'].config(text=student_detail[2])

                # --- Update Subject-wise Marks ---
                for i, key in enumerate(self.subject_names):
                    self.subject_labels[key].config(text=str(marks_record[i + 3]))

                # --- Update Results Summary ---
                self.report_labels['Total'].config(text=str(marks_record[0]))
                self.report_labels['Percentage'].config(text=f"{marks_record[1]:.2f} %")
                self.report_labels['Grade'].config(text=marks_record[2])

                self.roll_entry.delete(0, tk.END) 

            except pymysql.Error as e:
                messagebox.showerror("DB Error", f"Failed to generate report: {e}")
            except Exception as e:
                messagebox.showerror("Processing Error", f"An error occurred: {e}")
            finally:
                conn.close()

# 15. CHANGE PASSWORD PAGE
class ChangePasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="CHANGE PASSWORD", font=controller.title_font).pack(pady=40)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Current Username:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.username_entry = tk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        tk.Label(form_frame, text="Old Password:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.old_pass_entry = tk.Entry(form_frame, width=30, show="*")
        self.old_pass_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        tk.Label(form_frame, text="New Password:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.new_pass_entry = tk.Entry(form_frame, width=30, show="*")
        self.new_pass_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        tk.Button(self, text="Update Password", command=self.update_password_db, font=controller.button_font).pack(pady=20)
        tk.Button(self, text="BACK TO MAIN MENU", command=lambda: controller.show_frame("MainMenuPage"), font=controller.button_font, bg='red', fg='white').pack(pady=10)

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.old_pass_entry.delete(0, tk.END)
        self.new_pass_entry.delete(0, tk.END)

    def update_password_db(self):
        username = self.username_entry.get().strip()
        old_password = self.old_pass_entry.get().strip()
        new_password = self.new_pass_entry.get().strip()

        if not (username and old_password and new_password):
            messagebox.showerror("Input Error", "All fields must be filled.")
            return
        
        if old_password == new_password:
            messagebox.showerror("Input Error", "New password cannot be the same as the old password.")
            return

        conn = self.controller.create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # 1. Verify old password and username exist
                verify_query = "SELECT * FROM User_pass WHERE User = %s AND Pass = %s"
                cursor.execute(verify_query, (username, old_password))

                if cursor.fetchone():
                    # 2. Update password
                    update_query = "UPDATE User_pass SET Pass = %s WHERE User = %s"
                    cursor.execute(update_query, (new_password, username))
                    conn.commit()
                    messagebox.showinfo("Success", "Password updated successfully! Please login with your new password.")
                    self.clear_fields()
                    self.controller.show_frame("LoginPage") # Send user back to login
                else:
                    messagebox.showerror("Update Failed", "Invalid Username or Old Password.")
                
            except pymysql.Error as e:
                messagebox.showerror("Database Error", f"Password update failed: {e}")
            finally:
                conn.close()

if __name__ == "__main__":
    app = StudentManagementApp()
    app.mainloop()