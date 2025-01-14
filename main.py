from tkinter import *
from tkinter import messagebox
import pywinstyles
from PIL import ImageTk
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, accuracy_score
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

# Create the main Tkinter window
root = Tk()
root.geometry("1270x640+0+0")

pywinstyles.change_header_color(root, color="black")

# Connect to SQLite database
conn = sqlite3.connect('users.db')

def create_tables():
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            Fname TEXT NOT NULL,
            Lname TEXT NOT NULL,
            Age INTEGER NOT NULL,
            Username TEXT PRIMARY KEY,
            Password TEXT NOT NULL
        )
    ''')
    conn.commit()

create_tables()

def show_registration_form():
    clear_frame()
    
    root.title("Login/Registration Form")
    
    fname=StringVar()
    lname=StringVar()
    age=IntVar()
    interested=StringVar()
    usern=StringVar()
    passw=StringVar()
    
    # Function to change button color on hover
    def on_enter(e):
        submit_button.config(bg="light pink")

    # Function to change button color back when mouse leaves
    def on_leave(e):
        submit_button.config(bg="sky blue")

    background_image = ImageTk.PhotoImage(file="C:/Users/Admin/OneDrive/Desktop/mini project/DE/login bg.png")

    canvas = Canvas(root)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0 ,0 , image=background_image, anchor="nw")

    canvas.create_text(290, 80, text="Registration form", fill="Black", font=('times', 20 , 'bold'))

    canvas.create_text(210,140,text="First name :-", fill="Black", font=('times', 20 , 'bold'))
    fname_en=Entry(root,textvariable=fname,font=("times",12,"bold")).place(x=300,y=130,width=130)

    canvas.create_text(210,200,text="Last name :-", fill="Black", font=('times', 20 , 'bold'))
    lname_en=Entry(root,textvariable=lname,font=("times",12,"bold")).place(x=300,y=190,width=130)

    canvas.create_text(250,260,text="Age :-", fill="Black", font=('times', 20 , 'bold'))
    age_en=Entry(root,textvariable=age,font=("times",12,"bold")).place(x=300,y=250,width=130)

    # canvas.create_text(200,320,text="Interested in :-", fill="Black", font=('times', 20 , 'bold'))
    # interest_en=Entry(root,textvariable=interested,font=("times",12,"bold")).place(x=300,y=310,width=130)
    
    canvas.create_text(210,320,text="Username :-" ,fill="Black",font=('times', 20 , 'bold'))
    usern_en=Entry(root,textvariable=usern,font=('times', 12 , 'bold')).place(x=300,y=310,width=130)
    
    canvas.create_text(215,380,text="Password :-",fill="Black",font=('times', 20 , 'bold'))
    pass_en=Entry(root,textvariable=passw,font=('times', 12 , 'bold'), show="*").place(x=300,y=370,width=130)

    submit_button = Button(root, text="Sign up",command=lambda:complete_registration(fname.get(),lname.get(),age.get(),usern.get(),passw.get()), relief="raised", font=("times", 12, "bold"), bg="sky blue")
    submit_button.place(x=250, y=420, width=80)

    # Bind events to button for hover effect
    submit_button.bind("<Enter>", on_enter)
    submit_button.bind("<Leave>", on_leave)
    
    # Create text "Sign in" and bind the event to the text
    sign_in_text = canvas.create_text(290, 470, text="Already have an account : Log in", fill="Black", font=('times', 15 , 'bold'))
    canvas.tag_bind(sign_in_text, "<Button-1>", lambda event: show_login_form())
    
    root.mainloop()
    
def complete_registration(fname,lname,age,usern,passw):
    if fname and lname and age and usern and passw:
        cursor=conn.cursor()
        cursor.execute("SELECT Username FROM Users WHERE Username=?", (usern,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        else:
            # Insert the new user if the username is unique
            cursor.execute('INSERT INTO Users(Fname, Lname, Age, Username, Password) VALUES(?, ?, ?, ?, ?)', (fname, lname, age, usern, passw))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful. Log in to continue.")
            show_login_form()
    
    else:
        messagebox.showerror("Error","Please fill all data")     
    
    
def clear_frame():                  #to destroy all the inputs
    for widget in root.winfo_children():
        widget.destroy()

def show_login_form():
    
    clear_frame()
    root.title("Login/Registration Form")
    
    usern=StringVar()
    passw=StringVar()
    
    def on_enter(e):
        submit_button.config(bg="light pink")

    def on_leave(e):
        submit_button.config(bg="sky blue")

    background_image = ImageTk.PhotoImage(file="C:/Users/Admin/OneDrive/Desktop/mini project/DE/login bg.png")
    
    canvas = Canvas(root)               #creating a transparent page (canvas)
    canvas.pack(fill="both", expand=True)
    
    canvas.create_image(0 ,0 , image=background_image, anchor="nw")
    
    canvas.create_text(290, 80, text="Login form", fill="Black", font=('times', 20 , 'bold'))
    
    canvas.create_text(210,140,text="Username :-", fill="Black", font=('times', 20 , 'bold'))
    user_en=Entry(root,textvariable=usern, font=('times', 12 , 'bold')).place(x=300,y=130,width=130)
    
    canvas.create_text(210,200,text="Password :-", fill="Black", font=('times', 20 , 'bold'))
    pass_en=Entry(root,textvariable=passw, font=('times', 12 , 'bold'), show="*").place(x=300,y=190,width=130)
    
    submit_button = Button(root, text="Login in", command=lambda: complete_login(usern.get(), passw.get()), relief="raised", font=("times", 12, "bold"), bg="sky blue")
    submit_button.place(x=250, y=240, width=80)
    
    submit_button.bind("<Enter>", on_enter)
    submit_button.bind("<Leave>", on_leave)
    
    sign_in_text = canvas.create_text(290, 290, text="Don't have an account : Sign up", fill="Black", font=('times', 15 , 'bold'))
    canvas.tag_bind(sign_in_text, "<Button-1>", lambda event: show_registration_form())

    root.mainloop()
    
def complete_login(usern,passw):
    if usern and passw:
        cursor = conn.cursor()
        cursor.execute("SELECT Username,Password FROM Users WHERE Username=?", ((usern),))
        data = cursor.fetchone()
        if data:
            username , password = data
            if usern==username and passw==password:
                messagebox.showinfo("Login Successful", "Welcome, Admin!")
                show_main_menu()
                
            else:
                messagebox.showerror("Login Failed", "Invalid password")
            
        else:
            messagebox.showerror("Error","Username doesn't exist")    
        
    else:
        messagebox.showerror("Error","Please fill all data")    
        
def abt_us():
    clear_frame()
    
    root.title("About us")
    
    menubar=Menu(root)
    root.config(menu=menubar)
    
    menubar.add_command(label="About Us", command=abt_us)
    menubar.add_command(label="Home", command=show_main_menu)
    
    background_image=ImageTk.PhotoImage(file="C:/Users/Admin/OneDrive/Desktop/mini project/DE/main bg old.png")
    canvas = Canvas(root)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0 ,0 , image=background_image, anchor="nw")
    canvas.create_text(650,50,text="TEAM MEMBERS",fill="white", font=('times', 18 , 'bold'))
    canvas.create_text(650,110,text="Yash Karnawat - 03 (GL)",fill="white", font=('times', 18 , 'bold'))
    canvas.create_text(650,140,text="Aryan Gurjar - 21",fill="white", font=('times', 18 ))
    canvas.create_text(650,170,text="Soham Phenani - 16",fill="white", font=('times', 18))
    
    
    root.mainloop()

def show_main_menu():
    clear_frame()
    
    root.title("Main Page")
    
    background_image = ImageTk.PhotoImage(file="C:/Users/Admin/OneDrive/Desktop/mini project/DE/main bg.png")
    
    menubar = Menu(root)
    root.config(menu=menubar)
    
    menubar.add_command(label="About Us", command=abt_us)
    menubar.add_command(label="Home", command=show_main_menu)
    
    def on_enter(e):
        search_button.config(bg="light pink")

    def on_leave(e):
        search_button.config(bg="sky blue")
    
    def on_enter1(e):
        visualization_button.config(bg="light pink")

    def on_leave1(e):
        visualization_button.config(bg="sky blue")
    
    canvas = Canvas(root)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0 ,0 , image=background_image, anchor="nw")
    
    # Adding "Select What You Want" label
    canvas.create_text(620, 115, text="Select What You Want", font=("Helvetica", 24), fill="black")

    # Creating Search Job button
    search_button = Button(root, text="Search Job", font=("Helvetica", 12), bd=3, relief="raised",padx=106, pady=13, command=search_job)
    search_button.place(x=167, y=312)  # Adjust the position based on your layout

    search_button.bind("<Enter>", on_enter)
    search_button.bind("<Leave>", on_leave)

    # Creating See Visualization button
    visualization_button = Button(root, text="See Visualization", font=("Helvetica", 12), bd=3, relief="raised",padx=106, pady=13, command=see_visualization)
    visualization_button.place(x=760, y=312)  # Adjust the position based on your layout

    visualization_button.bind("<Enter>", on_enter1)
    visualization_button.bind("<Leave>", on_leave1)

    root.mainloop()

def search_job():
    clear_frame()

    root.title("Job Search")

    def jobs_on_search():
        job_search1 = job_search.get()
        print(job_search1)
        
        if job_search1 == "Locomotor Disability":
            messagebox.showinfo("Locomotor Disability (loss of limb, paralysis)", "Available Jobs: Data Entry Clerk, Customer Support Agent, Content Editor, Administrative Assistant")
        
        elif job_search1 == "Learning Disability":
            messagebox.showinfo("Learning Disability", "Available Jobs: Artist, Digital Marketer, Photographer, Tailor")
        
        elif job_search1 == "Psychiatric Disability":
            messagebox.showinfo("Psychiatric Disability", "Available Jobs: Copywriter, Social Media Manager, Video Content Creator")
        
        elif job_search1 == "Deaf/Hard of Hearing":
            messagebox.showinfo("Deaf/Hard of Hearing", "Available Jobs: Graphic Designer, Software Developer, Mechanic, Artist, Chef")
        
        elif job_search1 == "Intellectual/Developmental Disability":
            messagebox.showinfo("Intellectual/Developmental Disability", "Available Jobs: Butler, Telemarketer, Library Clerk, Plumber, Delivery Guy")
        
        elif job_search1 == "Physical Disability":
            messagebox.showinfo("Physical Disability", " Available Jobs: Telemarketer, Tutor, E-commerce Manager")
        
        elif job_search1 == "Dwarfism":
            messagebox.showinfo("Dwarfism", "Available Jobs: Project Manager, Community Manager, Virtual Assistant, Chef")
        
        elif job_search1 == "Parkinson's":
            messagebox.showinfo("Parkinson's", "Available Jobs: Content Maker, Data Entry Clerk, Customer Support Agent")
        else:
            messagebox.showerror("Error", "Please select a valid disability type.")

    background_image = ImageTk.PhotoImage(file="C:/Users/Admin/OneDrive/Desktop/mini project/DE/main bg old.png")

    menubar = Menu(root)
    root.config(menu=menubar)

    menubar.add_command(label="About Us", command=abt_us)
    menubar.add_command(label="Home", command=show_main_menu)

    canvas = Canvas(root)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_image, anchor="nw")
    canvas.create_text(600, 210, text="Search for available", fill="white", font=('times', 35, 'bold'))
    canvas.create_text(600, 260, text="Job based ", fill="white", font=('times', 35, 'bold'))
    canvas.create_text(600, 310, text="on Disability", fill="white", font=('times', 35, 'bold'))

    job_search = StringVar()

    list1 = ["Locomotor Disability", "Learning Disability", "Psychiatric Disability", "Deaf/Hard of Hearing", "Intellectual/Developmental Disability", "Physical Disability", "Dwarfism", "Parkinson's"]
    
    droplist = OptionMenu(root, job_search, *list1)
    droplist.place(x=450, y=370)
    job_search.set("Select Disability")
    droplist.config(width=40, bg="white")

    but_search = Button(root, text="Search Job", command=jobs_on_search, width=12, bg="White", fg="black")
    but_search.place(x=530, y=430)

    # Binding 'Enter' key to trigger search on pressing Enter
    but_search.bind("<Return>", lambda event: jobs_on_search())

    root.mainloop()

def see_visualization():
    clear_frame()
    
    root.title("Job visualization")
    
    background_image = ImageTk.PhotoImage(file="C:/Users/Admin/OneDrive/Desktop/mini project/DE/main bg old.png")
    
    menubar = Menu(root)
    root.config(menu=menubar)
    
    menubar.add_command(label="About Us", command=abt_us)
    menubar.add_command(label="Home", command=show_main_menu)
    
    search = StringVar()
    
    canvas = Canvas(root)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0 ,0 , image=background_image, anchor="nw")
    
    def on_entry_click(event):
        if search_en.get() == "Search here...":
            search_en.delete(0, "end")  # delete all the text in the entry
            search_en.insert(0, '')      # Insert blank for user input
            search_en.config(fg='black')
            
    def on_focusout(event):
        if search_en.get() == '':
            search_en.insert(0, "Search here...")
            search_en.config(fg='black')
        
    def on_key_release(event):
        suggestions = ["Age Distribution","Experience vs. Income","Frequency of Job Titles","Gender Distribution - Bar Graph","Income Distribution by Disability Type","Proportion of Disability Types","Score Distribution by Disability Type"]
        search_text = search_en.get().lower()
        suggested_options = [option for option in suggestions if search_text in option.lower()]
        update_suggestions(suggested_options)
        
    def update_suggestions(suggestions):
        suggestion_listbox.delete(0, END)
        for suggestion in suggestions:
            suggestion_listbox.insert(END, suggestion)
        
        if suggestions:
            suggestion_listbox.place(x=420, y=search_en.winfo_y() + search_en.winfo_height(), width=280)
        else:
            suggestion_listbox.place_forget()
            
    def on_suggestion_click(event):
        if suggestion_listbox.curselection():  # Check if selection is not empty
            index = suggestion_listbox.curselection()[0]
            selected_option = suggestion_listbox.get(index)
            search_en.delete(0, END)
            search_en.insert(0, selected_option)
        
    # Search for any analysis based on ott platforms
    canvas.create_text(600, 210, text="Search for any", fill="white", font=('times', 35, 'bold'))
    canvas.create_text(600, 260, text="visualization based ", fill="white", font=('times', 35, 'bold'))
    canvas.create_text(600, 310, text="on Jobs", fill="white", font=('times', 35, 'bold'))
    
    search_en = Entry(root, textvariable=search, font=('times', 22))
    search_en.insert(0, "Search here...")
    search_en.bind('<FocusIn>', on_entry_click)
    search_en.bind('<FocusOut>', on_focusout)
    search_en.bind('<KeyRelease>', on_key_release)
    search_en.place(x=420, y=360, width=280)
    
    suggestion_listbox = Listbox(root, font=('times', 16))
    suggestion_listbox.bind('<Button-1>', on_suggestion_click)
    
    search_button = Button(root, text="Search", bg="red", font=('times', 14, 'bold'), command=lambda: error_handling_in_analysis(search.get()), relief="raised")
    search_button.place(x=700, y=360, width=150)
    
    root.mainloop()


def error_handling_in_analysis(search):
    if search:
        if search=="Gender Distribution - Bar Graph" or search=="Age Distribution" or search=="Income Distribution by Disability Type" or search=="Frequency of Job Titles" or search=="Experience vs. Income" or search=="Proportion of Disability Types" or search=="Score Distribution by Disability Type":
            analysis(search)
        else :
            messagebox.showerror("Error","Enter the valid input")
    else:
        messagebox.showerror("Error","Please enter what you want to search")


def analysis(search):
    clear_frame()
    
    global plot_canvas  # Declare plot_canvas as global variable
    
    root.title("Analysis( Visualizattion )")
    
    df = pd.read_csv("Disability_Job_Dataset.csv")

    menubar=Menu(root)
    root.config(menu=menubar)
    
    menubar.add_command(label="About Us", command=abt_us)
    menubar.add_command(label="Home", command=show_main_menu)

    def decision():
        if search == "Gender Distribution - Bar Graph":
            plot1()
        elif search == "Age Distribution":
            plot2()
        elif search == "Income Distribution by Disability Type":
            plot3()
        elif search == "Frequency of Job Titles":
            plot4()
        elif search == "Experience vs. Income":
            plot5()
        elif search == "Proportion of Disability Types":
            plot6()
        elif search == "Score Distribution by Disability Type":
            plot7()
        else:
            messagebox.showerror("Error", "Enter a valid input")


    def plot1():  # Gender Distribution - Bar Graph
        global plot_canvas
        
        gender_counts = df['Sex'].value_counts()
        plt.figure(figsize=(8, 5))
        gender_counts.plot(kind='bar', color=['pink', 'blue'])
        plt.title('Gender Distribution - Bar Graph')
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.xticks(rotation=0)
        
        if plot_canvas:
            plot_canvas.get_tk_widget().destroy()
        
        plot_canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()


    def plot2():  # Age Distribution
        global plot_canvas
        
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Age'], bins=20, kde=True)
        plt.title('Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        
        if plot_canvas:
            plot_canvas.get_tk_widget().destroy()
        
        plot_canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()


    def plot3():  # Income Distribution by Disability Type
        global plot_canvas
        
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='Disability Type', y='Income', data=df)
        plt.title('Income Distribution by Disability Type')
        plt.xlabel('Disability Type')
        plt.ylabel('Income')
        plt.xticks(rotation=45)
        
        if plot_canvas:
            plot_canvas.get_tk_widget().destroy()
        
        plot_canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()


    def plot4():  # Frequency of Job Titles
        global plot_canvas
        
        plt.figure(figsize=(14, 8))
        sns.countplot(y='Job Title', data=df, order=df['Job Title'].value_counts().index)
        plt.title('Frequency of Job Titles')
        plt.xlabel('Frequency')
        plt.ylabel('Job Title')
        
        if plot_canvas:
            plot_canvas.get_tk_widget().destroy()
        
        plot_canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()


    def plot5():  # Experience vs. Income
        global plot_canvas
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Experience', y='Income', hue='Disability Type', data=df)
        plt.title('Experience vs. Income')
        plt.xlabel('Years of Experience')
        plt.ylabel('Income')
        plt.legend(title='Disability Type', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        if plot_canvas:
            plot_canvas.get_tk_widget().destroy()
        
        plot_canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()


    def plot6():  # Proportion of Disability Types
        global plot_canvas
        
        plt.figure(figsize=(8, 8))
        df['Disability Type'].value_counts().plot.pie(autopct='%1.1f%%', startangle=140, cmap='viridis')
        plt.title('Proportion of Disability Types')
        
        if plot_canvas:
            plot_canvas.get_tk_widget().destroy()
        
        plot_canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()


    def plot7():  # Score Distribution by Disability Type
        global plot_canvas
        
        plt.figure(figsize=(12, 6))
        sns.violinplot(x='Disability Type', y='Score', data=df)
        plt.title('Score Distribution by Disability Type')
        plt.xlabel('Disability Type')
        plt.ylabel('Score')
        plt.xticks(rotation=45)
        
        if plot_canvas:
            plot_canvas.get_tk_widget().destroy()
        
        plot_canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack()

        
    def exit_plot():    
        root.quit()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    plot_canvas = None
    
    root.configure(bg='#C9E9D2')

    plot_button = Button(root, text="Plot graph", command=decision)
    plot_button.pack(pady=20)

    plot_exit=Button(root,text="Exit",command=exit_plot)
    plot_exit.place(x=730,y=20,width=50)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

    
show_login_form()