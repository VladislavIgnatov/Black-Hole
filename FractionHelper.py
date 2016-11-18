import tkinter as tk
import operator
import sqlite3

# Set Operators for use in Solver window
ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

# Finale Project
# CIS 4930 Advanced Python Fall 2016
# Author: Vladislav Ignatov
# Date: 11/3/2016

class App(tk.Tk):

    def __init__(self, *args, **kwargs):

    	#Initialize tkinter
        tk.Tk.__init__(self, *args, **kwargs)

        # Title for the Login Window 
       	self.wm_title("Fraction Helper")

        #Initialize the defualt frame and then pack it.
        container = tk.Frame(self)
        container.pack()

        #Initialize the defualt grid weight for row and column.
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #database stuff
        print("Connecting to database")
        sqlite_file = 'fshdb.sqlite'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        print ('Database connected')
        try:
           c.execute('CREATE TABLE results (ID text, Addition real, Subtraction real, Multiplication real, Division real, Average real)')
        except sqlite3.OperationalError:
           print("Results table exists")
        try:
           c.execute('CREATE TABLE users (ID text PRIMARY KEY, Pass text)')
        except sqlite3.OperationalError:
           print("Table already exists")
        try:
           c.execute("INSERT INTO users (ID, Pass) VALUES ('admin', 'passmin')")
        except sqlite3.IntegrityError:
           print("That ID already exists")

        conn.commit()
        conn.close()

        # Username after it has been validated
        self.username = ""

        # Frame Dictionary holds (LoginWindow, MainWindow, SolverWindow, QuizzerWindow, ViewResultsWindow, RegisterWindow)
        self.frames = {}

        for F in (LoginWindow, MainWindow, SolverWindow, QuizzerWindow, ViewResultsWindow, RegisterWindow):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Sets the staring frame as loginwindow
        self.show_frame("LoginWindow")

    # Sets the frame as what ever is passed in
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LoginWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Space in the grid
        label = tk.Label(self, text="")
        label.grid(row=0, column=1)

		# Lable for Username and Password
        username_lable = tk.Label(self, text="Username: ")
        username_lable.grid(row=1, column=1)
        password_lable = tk.Label(self, text="Password: ")
        password_lable.grid(row=2, column=1)

        # Entry for Username and Password
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=2)
        self.username_entry.focus_set()
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.grid(row=2, column=2)

		# Space in the grid
        label = tk.Label(self, text="")
        label.grid(row=3, column=1)

        # Login button
        Login_Button = tk.Button(self, text="Login", width=10,
        	 command = self.Login_Clicked)
        Login_Button.grid(row=4, column=2)

        #Register button for new user
        Register_Button = tk.Button(self, text="New User", width=10,
        	 command = lambda: controller.show_frame("RegisterWindow"))
        Register_Button.grid(row=5, column=2)

        # Exit button to get out of application
        Exit_button = tk.Button(self, text="Exit", width=10, command=self.quit)
        Exit_button.grid(row=6, column=2)

    # Login function
    def Login_Clicked(self):
    	# Sets the username and password to username_get and password_get as Strings
    	username_get = self.username_entry.get()
    	password_get = self.password_entry.get()

    	# Check if there is input.
    	if (username_get == "" or password_get == ""):
    		ErrorboxGeneratpr("Error: No Input is given. Username or Password is missing.")
    	else:
    		# TODO implement Login DataBase verification
                conn = sqlite3.connect('fshdb.sqlite')
                c = conn.cursor()
                c.execute("SELECT ID FROM users WHERE ID = ?", (username_get,))
                data=c.fetchall()
                if len(data) == 0:
                   ErrorboxGeneratpr ("User name does not exist")
                else:
                   c.execute("SELECT Pass FROM users WHERE ID = ?", (username_get,))        
                   datas = c.fetchone()
                   if datas[0] != password_get:
                      ErrorboxGeneratpr("Password incorrect")
                   else:
    		      # Set the username if valid for later refrence in quizzer and viewresults
                      self.controller.username = username_get

    		      # If in DB goes to MainWindow
                      self.controller.show_frame("MainWindow")
                conn.close()

class MainWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="MAIN WINDOW")
        label.pack(side="top", fill="x", pady=10)

        Solverbutton = tk.Button(self, text="Solver", width=10,
        	command=lambda: controller.show_frame("SolverWindow"))
        Solverbutton.pack()
        Quizzerbutton = tk.Button(self, text="Quizzer", width=10,
        	command=lambda: controller.show_frame("QuizzerWindow"))
        Quizzerbutton.pack()
        ViewResultsbutton = tk.Button(self, text="View Results", width=10,
        	command=lambda: controller.show_frame("ViewResultsWindow"))
        ViewResultsbutton.pack()

        # Exit button to get out of application
        Quit_button = tk.Button(self, text="Quit", width=10, command=self.quit)
        Quit_button.pack()

class SolverWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Solver Window")
        label.grid(row=0, column=3)

        # Space in the grid
        label = tk.Label(self, text="")
        label.grid(row=1, column=3)

        # (x1/x2) first fraction
       	self.x1 = tk.Entry(self, width = 6)
        self.x1.grid(row=2, column=0)
        label = tk.Label(self, text="/", borderwidth=2)
        label.grid(row=2, column=1)
        self.x2 = tk.Entry(self, width = 6)
        self.x2.grid(row=2, column=2)

        # Creat the List box and insert into it (+,-,*,/)
        self.operator_input = tk.Listbox(self, height=4 , width=5)
        self.operator_input.grid(row=2, column=3)
        self.operator_input.insert(1,"+")
        self.operator_input.insert(2,"-")
        self.operator_input.insert(3,"*")
        self.operator_input.insert(4,"/")

        # (y1/y2) second fraction 
        self.y1 = tk.Entry(self, width = 6)
        self.y1.grid(row=2, column=4)
        label = tk.Label(self, text="/")
        label.grid(row=2, column=5)
        self.y2 = tk.Entry(self, width = 6)
        self.y2.grid(row=2, column=6)

        # Space in the grid
        label = tk.Label(self, text="")
        label.grid(row=3, column=3)

        # Answer : label
        label = tk.Label(self, text="Answer: ")
        label.grid(row=4, column=4)

        # Button to solve
        button = tk.Button(self, text="Solve", width = 10,
                           command=self.SolverFunction)
        button.grid(row=4, column=3)

  		# Button back to the MainWindow.
        button = tk.Button(self, text="MainWindow", width = 10,
                           command=lambda: controller.show_frame("MainWindow"))
        button.grid(row=5, column=3)

    def SolverFunction(self):
    	try:
    		# Sets the operator from the list
    		oper = self.operator_input.get(self.operator_input.curselection())

    		# Set all the numbers from the inputs for the fraction and convert to int.
    		w1 = int(self.x1.get())
    		w2 = int(self.x2.get())
    		z1 = int(self.y1.get())
    		z2 = int(self.y2.get())

    		# TODO fix how to represent the result
    		op_func = ops[oper]
    		w = w1 / w2
    		z = z1 / z2
    		reuslt = op_func(w, z)
    		label = tk.Label(self, text= str(reuslt))
    		label.grid(row=4, column=6)
    	except ValueError:
    		ErrorboxGeneratpr("Error: Please enter Only numbers in the inputs.")
    	except tk.TclError:
    		ErrorboxGeneratpr("Error: Please select an operator.")
    	except ZeroDivisionError:
    		ErrorboxGeneratpr("Error: You can not divide by zero.")

class QuizzerWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="QuizzerWindow")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="MainWindow",
                           command=lambda: controller.show_frame("MainWindow"))
        button.pack()

class ViewResultsWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #TODO using (controller.username) Show table of the users results.
        label = tk.Label(self, text="ViewResultsWindow")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="MainWindow",
                           command=lambda: controller.show_frame("MainWindow"))
        button.pack()

class RegisterWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Space in the grid
        label = tk.Label(self, text="")
        label.grid(row=0, column=1)

		# Lable for Username and Password
        username_lable = tk.Label(self, text="Username: ")
        username_lable.grid(row=1, sticky=tk.E)
        password_lable = tk.Label(self, text="Password: ")
        password_lable.grid(row=2, sticky=tk.E)
        password_lable = tk.Label(self, text="Verify Password: ")
        password_lable.grid(row=3, sticky=tk.E)

        # Entry for Username and Password
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1)
        self.password1_entry = tk.Entry(self)
        self.password1_entry.grid(row=2, column=1)
        self.password2_entry = tk.Entry(self)
        self.password2_entry.grid(row=3, column=1)

		# Space in the grid
        label = tk.Label(self, text="")
        label.grid(row=4, column=1)

        # Login button
        CreatUser_Button = tk.Button(self, text="Creat Account", width=12,
        	 command=self.NewUserCreation)
        CreatUser_Button.grid(columnspan=2)

        # Exit button to get out of application
        Exit_button = tk.Button(self, text="Exit", width=12, command=self.quit)
        Exit_button.grid(columnspan=2)


    def NewUserCreation(self):
    	# Sets the username and password as Strings
    	username_get = self.username_entry.get()
    	password1_get = self.password1_entry.get()
    	password2_get = self.password2_entry.get()

    	# Check if there is input.
    	if (username_get == "" or password1_get == "" or password2_get == ""):
    		ErrorboxGeneratpr("Error: No Input is given. Username or Password is missing.")
    	else:
           data = None
           conn = sqlite3.connect('fshdb.sqlite')
           c = conn.cursor()
           c.execute("SELECT ID FROM users WHERE ID = ?", (username_get,))
           data=c.fetchone()
           if data:
              ErrorboxGeneratpr("Username already in use.")
           elif password2_get == password1_get:
              c.execute("INSERT INTO users (ID, Pass) VALUES (?, ?)", (username_get, password1_get))
              self.controller.username = username_get
              self.controller.show_frame("MainWindow")
              conn.commit()
              conn.close()
           else:
              ErrorboxGeneratpr("The passwords you have entered do not match.")

def ErrorboxGeneratpr(tmp):
	# Creates window.
	ErrorWindow = tk.Toplevel()

	# Set title for ErrorWindow.
	ErrorWindow.title("Error")

	# Set size of ErrorWindow
	ErrorWindow.geometry("%dx%d%+d%+d" % (300, 100, 150, 125))

	# Creates the Message Lable and packs it.
	msg = tk.Message(ErrorWindow, text=tmp, width = 200)
	msg.pack()

	# Creates the Button and packs it.
	button = tk.Button(ErrorWindow, text="Ok", width=12, command=ErrorWindow.destroy)
	button.pack()

if __name__ == "__main__":
    app = App()
app.mainloop()
