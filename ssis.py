import os
import csv
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import ttk


class Student:
    #initialize new Student object
    def __init__ (self,std_id:str,last_name: str, first_name:str, middle_name:str, year:int, gender:str, course_code:str) -> None:
        self.std_id = std_id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.year = year
        self.gender = gender
        self.course_code = course_code
    
def read_courses (csv_file_path: str) -> dict: 
        #initialize empty dict para sa course
        courses = {}
        try:
            with open(csv_file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        courses[row[0]] = row[1] #populate the dict. with course code and course title 
        except FileNotFoundError:
            print("Error: could not find or open 'student_courses.csv' file ")
        except Exception as e:
            print("Error occured while reading 'student_course.csv'",e)
        return courses
    
def read_students(csv_file_path: str) -> list:
        #initialize empty dict for the student data
        students = []
        try:
            with open(csv_file_path, mode = 'r') as file:
                reader = csv.reader(file)
                next(reader,None)
                for row in reader:
                    students.append(row) #append each row
        except FileNotFoundError:
            print("Error: Could not find or open 'student_data.csv' file")
        except Exception as e:
            print("Error occured while reading 'student_data.csv' ", e)
        return students
    
def add_student(courses, std_id, last_name, first_name, middle_name, year, gender, course_code, csv_file_path_students):
        try:
            if course_code.strip(): #check if course code is provided
                if course_code.upper() in (code.upper() for code in courses): #check if its in course dict
                    status = "Enrolled"
                else:
                    status = "Not Available"
            else:
                    status = "Not Enrolled"
            
            with open(csv_file_path_students, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == std_id:
                        return "ID number already Exists, student not added"  # ID number exist

            #write student data
            with open(csv_file_path_students, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([std_id, last_name, first_name, middle_name, year, gender,course_code])

            return status
        except Exception as e:
            print("Error occured while adding students", e)
            return "Error"
        
def sort_student_data(csv_file_path_students: str):
    try:
        #open csv file and read the stuudent data dict
        with open(csv_file_path_students, 'r') as file:
            data = list(csv.reader(file))
            
            if len(data) < 2: #check if its <2
                print("Data length is less than 2. No sorting needed.")
                return
            
            #extract header and data rows
            header = data[0]
            data = data[1:]
            print("Data length before sorting:", len(data))  
            
            # sort data by id no.
            data.sort(key=lambda x: x[0])
            data.insert(0, header) 

        # write sorted data back to csv
        with open(csv_file_path_students, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except FileNotFoundError:
        print("Error: Could not find or open 'student_data.csv' file.")
    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("Error occurred while sorting student data:", e)

def main_window():
    #get the file path...
    current_directory = os.path.dirname(__file__)
    csv_file_path_students = os.path.join(current_directory, 'student_data.csv')
    csv_file_path_courses = os.path.join(current_directory, 'student_courses.csv')

    sort_student_data(csv_file_path_students) #sort :<
    
    #read the courses and student 
    courses = read_courses(csv_file_path_courses)
    students = read_students(csv_file_path_students)

    #make main windowww
    main_window = tk.Tk()
    main_window.geometry("450x300")
    main_window.title("Main Menu")
    main_window.resizable(False, False)

    frame = tk.Frame(main_window, width=933, height=531, bg="#800000")
    frame.pack_propagate(False)
    frame.pack()
    
    def open_add_student_window(): #function to add studentz
        main_window.withdraw()
        add_student_window(courses)

    def open_student_list_window(): #function for student lizt
        main_window.withdraw()
        student_list_window(students, csv_file_path_students)

    def open_courses_window(): #function to open coursezz
        main_window.withdraw()
        courses_window(courses, csv_file_path_courses)

    
    welcome_label = tk.Label(frame, text="Welcome to Student Information System", font=("Montserrat", 13,"bold"),fg="#FFFFFF", bg="#800000")
    welcome_label.pack()

    #buttonz for the windowz
    add_button = tk.Button(main_window, text="Add Student", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=open_add_student_window)
    add_button.place(x=120, y=50, width=200, height=38)

    list_button = tk.Button(main_window, text="Student List", font=("Montserrat",10), bg="#1A1515",fg="#FFFFFF", bd=0,command=open_student_list_window)
    list_button.place(x=120, y=100, width=200, height=38)

    courses_button = tk.Button(main_window, text="Available Courses",font=("Montserrat",10), bg="#1A1515",fg="#FFFFFF", bd=0, command=open_courses_window)
    courses_button.place(x=120, y=150, width=200, height=38)

    exit_button = tk.Button(main_window, text="Exit",font=("Montserrat",10),bg="#1A1515",fg="#FFFFFF", bd=0, command=main_window.destroy)
    exit_button.place(x=120, y=200, width=200, height=38)

    main_window.mainloop()

def add_student_window(courses):
    #create a new toplevel window for adding a student
    add_student_window = tk.Toplevel()  
    add_student_window.geometry("850x531")
    add_student_window.title("Add Student")
    add_student_window.resizable(False, False)

    frame = tk.Frame(add_student_window, width=933, height=531, bg="#800000")
    frame.pack_propagate(False)
    frame.pack()

    input_label = tk.Label(frame, text="Input Student Information", font=("Montserrat", 15,"bold"),fg="#FFFFFF", bg="#800000")
    input_label.pack()
    
    labels = [
        "Student ID", "Last Name", "First Name", "Middle Name", "Year Level", "Gender", "Course Code"
    ]

    label_positions = [
        (36, 63), (36, 149), (304, 149), (572, 149), (88, 243), (440, 238), (36, 329)
    ]

    for i, (label_text, (x, y)) in enumerate(zip(labels, label_positions)):
        label = tk.Label(frame, text=label_text, font=("Montserrat", 10), bg="#800000", fg="white")
        label.place(x=x, y=y) 

    #entry fields for the input
    entry_positions = [
        (23, 96), (23, 185), (292, 185), (561, 185), (75, 276), (40, 350) # Added position for the Course Code entry field
    ]

    entry_fields = []
    for (x, y) in entry_positions:
        entry = tk.Entry(frame, font=("Montserrat", 10), bg="#D9D9D9")
        entry.place(x=x, y=y, width=249)
        entry_fields.append(entry)

    #dropdown for the gender opt
    gender_options = ["Female", "Male", "Others"]
    gender_var = tk.StringVar(add_student_window)
    gender_var.set(gender_options[0])  

    gender_label = tk.Label(frame, text="Gender", font=("Montserrat", 10), bg="#800000", fg="white")
    gender_label.place(x=440, y=238)

    gender_dropdown = tk.OptionMenu(frame, gender_var, *gender_options)
    gender_dropdown.config(font=("Montserrat", 10), bg="#D9D9D9", width=15)
    gender_dropdown.place(x=440, y=260)

    #function to save student info
    def save_student():
        try:
            #get the input values
            student_id, last_name, first_name, middle_name, year, course_code = [entry.get() for entry in entry_fields[:6]]  # Updated to fetch 6 entries
            gender = gender_var.get()

            #get the current directory and path
            current_directory = os.path.dirname(__file__)
            csv_file_path_students = os.path.join(current_directory, 'student_data.csv')

            # when adding a student get the status
            status = add_student(courses, student_id, last_name, first_name, middle_name, year, gender, course_code, csv_file_path_students)
            messagebox.showinfo("Status", f"Student added. Status: {status}")  # Show status
            add_student_window.destroy()
            main_window()  #refresh main window
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    #save the student info and add it to csv
    save_button = tk.Button(frame, text="Save", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=save_student)
    save_button.place(x=650, y=468, width=130, height=38)

    add_student_window.mainloop()

def student_list_window(students, csv_file_path_students):
    #new window for the student list
    student_list_window = tk.Tk()
    student_list_window.geometry("2000x700")
    student_list_window.title("Student List")

    frame = tk.Frame(student_list_window, width=400, height=300)
    frame.pack(fill=tk.BOTH, expand=True)

    list_label = tk.Label(frame, text="Student List", font=("Helvetica", 13),bg="#800000",fg="#FFFFFF")
    list_label.pack(fill=tk.X)

    #treeview widget to display data
    tree = ttk.Treeview(frame, columns=("Student ID", "Last Name", "First Name", "Middle Name", "Year Level", "Gender", "Course Code"), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    #set headings for columns
    tree.heading("Student ID", text="Student ID")
    tree.heading("Last Name", text="Last Name")
    tree.heading("First Name", text="First Name")
    tree.heading("Middle Name", text="Middle Name")
    tree.heading("Year Level", text="Year Level")
    tree.heading("Gender", text="Gender")
    tree.heading("Course Code", text="Course Code")

    try:
        for i, student in enumerate(students): #for every student insert a row in the treeview
            tree.insert("", tk.END, iid=i, values=student)
    except FileNotFoundError:
        messagebox.showerror("Error", "Could not find or open 'student_data.csv' file.")

    #edit student info
    def edit_student():
        selected_item = tree.selection()
        if selected_item:
            try:
                index = int(selected_item[0])  # get index of the selected item
                if 0 <= index < len(students):
                    print("Selected index:", index)  # print the selected index for debugging
                    edit_student_window(index, students, csv_file_path_students, student_list_window)
                else:
                    messagebox.showerror("Error", "Invalid index.")
            except ValueError:
                messagebox.showerror("Error", "Invalid selection.")
        else:
            messagebox.showerror("Error", "No student selected.")


    #edit button
    edit_button = tk.Button(frame, text="Edit", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=edit_student)
    edit_button.pack(side=tk.BOTTOM)

    student_list_window.mainloop()


def edit_student_window(index, students, csv_file_path_students, previous_window=None):
    #function to save changes made sa edit student window
    def save_changes():
        try:
            #check if index is in valid range
            if 0 <= index < len(students):
                #this update the student info with the values from the entry fields
                students[index] = [
                    entry_fields[i].get() if i < len(entry_fields) else '' for i in range(5)  #this updates id,name,year 
                ] + [
                    gender_var.get(),  # get gender
                    course_code_entry.get().upper() if course_code_entry else ''  # then course code
                ]
                # put the updated student info in the csv file
                with open(csv_file_path_students, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(students)
                
                messagebox.showinfo("Success", "Changes saved successfully.")
                edit_student_window.destroy()
                if previous_window:
                    previous_window.destroy()  #destroy previous student list window
                student_list_window(students, csv_file_path_students)  # Open new student list window
            else:
                messagebox.showerror("Error", "Invalid index.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    #create new toplevel window for edi student , details are same with add students
    edit_student_window = tk.Toplevel()  
    edit_student_window.geometry("850x531")
    edit_student_window.title("Edit Student")
    edit_student_window.resizable(False, False)

    frame = tk.Frame(edit_student_window, width=933, height=531, bg="#800000")
    frame.pack_propagate(False)
    frame.pack()

    input_label = tk.Label(frame, text="Edit Student Information", font=("Montserrat", 15,"bold"),fg="#FFFFFF", bg="#800000")
    input_label.pack()

    labels = [
        "Student ID", "Last Name", "First Name", "Middle Name", "Year Level", "Gender", "Course Code"
    ]

    label_positions = [
        (36, 63), (36, 149), (304, 149), (572, 149), (88, 243), (440, 238), (36, 329)
    ]

    for i, (label_text, (x, y)) in enumerate(zip(labels, label_positions)):
        label = tk.Label(frame, text=label_text, font=("Montserrat", 10), bg="#800000", fg="white")
        label.place(x=x, y=y) 

    entry_positions = [
        (23, 96), (23, 185), (292, 185), (561, 185), (75, 276)
    ]

    entry_fields = []
    for (x, y), value in zip(entry_positions, students[index]):
        entry = tk.Entry(frame, font=("Montserrat", 10), bg="#D9D9D9")
        entry.insert(0, value)
        entry.place(x=x, y=y, width=249)
        entry_fields.append(entry)

    gender_options = ["Female", "Male", "Others"]
    gender_var = tk.StringVar(edit_student_window)
    gender_var.set(students[index][5])  

    gender_label = tk.Label(frame, text="Gender", font=("Montserrat", 10), bg="#800000", fg="white")
    gender_label.place(x=440, y=243)

    gender_dropdown = tk.OptionMenu(frame, gender_var, *gender_options)
    gender_dropdown.config(font=("Montserrat", 10), bg="#D9D9D9", width=17)
    gender_dropdown.place(x=440, y=268)

    course_code_label = tk.Label(frame, text="Course Code", font=("Montserrat", 10), bg="#800000", fg="white")
    course_code_label.place(x=36, y=329)

    course_code_entry = tk.Entry(frame, font=("Montserrat", 10), bg="#D9D9D9")
    course_code_entry.insert(0, students[index][6])  
    course_code_entry.place(x=36, y=360, width=249)

    save_button = tk.Button(frame, text="Save Changes", font=("Montserrat", 10), bg="#1A1515", fg="#FFFFFF", bd=0, command=save_changes)
    save_button.place(x=650, y=468, width=130, height=38)

    edit_student_window.mainloop()


def courses_window(courses, csv_file_path_courses):

    def add_course_window():
        def add_course():
            course_code = course_code_entry.get().strip()
            course_name = course_name_entry.get().strip()

            if course_code in courses:
                messagebox.showerror("Error",f"Course with code {course_code} already exists.")
                return

    #create window for courses
    courses_window = tk.Tk()
    courses_window.geometry("300x400")
    courses_window.title("Courses")

    frame = tk.Frame(courses_window, width=400, height=300)
    frame.pack(fill=tk.BOTH, expand=True)

    list_label = tk.Label(frame, text="Available Courses", font=("Montserrat", 12), bg="#800000", fg="#FFFFFF")
    list_label.pack(fill=tk.X)

    #treeview for the courses
    tree = ttk.Treeview(frame, columns=("Course Code", "Course Name"), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    tree.heading("Course Code", text="Course Code")
    tree.heading("Course Name", text="Course Name")

    try:
        for code, name in courses.items():
            tree.insert("", tk.END, values=(code, name))

    except FileNotFoundError:
        messagebox.showerror("Error", "Could not find or open 'student_courses.csv' file.")

    courses_window.mainloop()

if __name__ == "__main__": #call main to open main window
    main_window()