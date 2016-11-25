import tkinter as tk
import operator
import sqlite3
from fractions import Fraction
import random
import matplotlib.pyplot as plt
import numpy as np


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
           c.execute('CREATE TABLE results (ID text, Operator text, Average real)')
        except sqlite3.OperationalError:
           print("Results table exists")
        try:
           c.execute('CREATE TABLE users (ID text PRIMARY KEY, Pass text)')
        except sqlite3.OperationalError:
           print("Table initialized")
        try:
           c.execute("INSERT INTO users (ID, Pass) VALUES ('admin', 'passmin')")
        except sqlite3.IntegrityError:
           print("Admin verified")

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
        ViewResultsbutton = tk.Button(self, text="View Scores", width=10,
        	command=self.graph)
        ViewResultsbutton.pack()

        # Exit button to get out of application
        Quit_button = tk.Button(self, text="Quit", width=10, command=self.quit)
        Quit_button.pack()

    def graph(self):
        objects = ('Addition', 'AddAll', 'Subtraction', 'SubAll', 'Multiplication', 'MultiAll', 'Division', 'DivAll', 'OverAll', 'OverAllAll')
        horiz = np.arange(len(objects))
        sumAdds, sumSubts, sumMults, sumDivs, sumOps = (0,0,0,0,0)
        numAdds, numSubts, numMults, numDivs, numOps = (0,0,0,0,0)
        sumAddsAll, sumSubtsAll, sumMultsAll, sumDivsAll, sumOpsAll = (0,0,0,0,0)
        numAddsAll, numSubtsAll, numMultsAll, numDivsAll, numOpsAll = (0,0,0,0,0)
        usr = self.controller.username
        dbQuery = "SELECT * FROM results WHERE ID = '" + usr + "'"
        sqlite_file = 'fshdb.sqlite'
        conn = sqlite3.connect(sqlite_file)
        d = conn.execute(dbQuery)
        for row in d:
            if (row[1] == '+'):
                sumAdds += row[2]
                numAdds += 1
            elif (row[1] == '-'):
                sumSubts += row[2]
                numSubts += 1
            elif (row[1] == '*'):
                sumMults += row[2]
                numMults += 1
            elif (row[1] == '/'):
                sumDivs += row[2]
                numDivs += 1
            sumOps += row[2]
            numOps += 1
        db2Query = 'SELECT * FROM results'
        f = conn.execute(db2Query)
        for row in f:
            if (row[1] == '+'):
                sumAddsAll += row[2]
                numAddsAll += 1
            elif (row[1] == '-'):
                sumSubtsAll += row[2]
                numSubtsAll += 1
            elif (row[1] == '*'):
                sumMultsAll += row[2]
                numMultsAll += 1
            elif (row[1] == '/'):
                sumDivsAll += row[2]
                numDivsAll += 1
            sumOpsAll += row[2]
            numOpsAll += 1
       
        conn.close()

        if numAdds == 0: numAdds = 1
        if numSubts == 0: numSubts = 1
        if numMults == 0: numMults = 1
        if numDivs == 0: numDivs = 1
        if numOps == 0: numOps = 1
        if numAddsAll == 0: numAddsAll = 1
        if numSubtsAll == 0: numSubtsAll = 1
        if numMultsAll == 0: numMultsAll = 1
        if numDivsAll == 0: numDivsAll = 1
        if numOpsAll == 0: numOpsAll = 1

        scores = [sumAdds / numAdds, sumAddsAll/numAddsAll, sumSubts / numSubts, sumSubtsAll / numSubtsAll, sumMults / numMults, sumMultsAll / numMultsAll, sumDivs / numDivs, sumDivsAll / numDivsAll, sumOps / numOps, sumOpsAll / numOpsAll]
        plt.bar(horiz, scores, align='center', alpha=0.5)
        plt.xticks(horiz, objects, rotation='vertical')
        plt.ylabel('Average')
        plt.title('Quiz Averages')
        plt.show()        

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
        
        # Title for window and spacer after
        tk.Label(self, text="Quizzer Window").pack()
        tk.Label(self, text="").pack()
        
        # Create the main frame for our equation and answer
        mainFrame = tk.Frame(self)
        mainFrame.pack()
        
        # First fraction
        self.firstFraction = tk.Label(self, text="")
        self.firstFraction.grid(row=2, column=0, in_=mainFrame)
        
        # List of operators to choose
        self.operator_input = tk.Listbox(self, height=4 , width=3)
        self.operator_input.grid(row=2, column=1, in_=mainFrame)
        self.operator_input.insert(1,"+")
        self.operator_input.insert(2,"-")
        self.operator_input.insert(3,"*")
        self.operator_input.insert(4,"/")
        
        # Second fraction
        self.secondFraction = tk.Label(self, text="")
        self.secondFraction.grid(row=2, column=2, in_=mainFrame)
        
        # Equal sign
        label = tk.Label(self, text="=")
        label.grid(row=2, column=3, in_=mainFrame)
        
        ### Answer views
        # Answer numerator
        self.numerator = tk.Entry(self, width=5)
        self.numerator.grid(row=2, column=4, in_=mainFrame)
        
        # Answer fraction sign
        label = tk.Label(self, text="/", borderwidth=2)
        label.grid(row=2,column=5, in_=mainFrame)
        
        # Answer denominator
        self.denominator = tk.Entry(self, width=5)
        self.denominator.grid(row=2, column=6, in_=mainFrame)
        
        ## Results Label
        self.resultsLabel = tk.Label(self, text="")
        self.resultsLabel.grid(row=3, column=0, columnspan=6, in_=mainFrame)
        
        #### Final buttons, with spacer above
        # Answer submit button
        tk.Label(self, text="").pack()
        button = tk.Button(self, text="Submit Answer",
                           command=self.QuizzerSubmitAnswer)
        button.pack()

        # Put the button to go back to main window
        button = tk.Button(self, text="MainWindow",
                           command=lambda: controller.show_frame("MainWindow"))
        button.pack()
        
        #### Get our fractions
        self.QuizzerSetRandomEquation()
        
    def QuizzerSetRandomEquation(self):
        # TODO: How large should these get? Isn't the program meant to be for kids learning fractions....figured it shouldn't be too high
        self.numer1 = random.randint(1,20)
        self.denom1 = random.randint(1,20)
        
        self.numer2 = random.randint(1,20)
        self.denom2 = random.randint(1,20)
        
        self.frac1 = Fraction(self.numer1,self.denom1)
        self.frac2 = Fraction(self.numer2,self.denom2)
        
        self.firstFraction['text'] = self.frac1
        self.secondFraction['text'] = self.frac2
    
    def QuizzerSubmitAnswer(self):
        try:
            # Get all our data from the user's selections and put answer into fraction
            selectedOperator = self.operator_input.get(self.operator_input.curselection())
            ansNumer = int(self.numerator.get())
            ansDenom = int(self.denominator.get())
            givenAnswer = Fraction("{0}/{1}".format(ansNumer, ansDenom))
            
            # Calculate the correct answer
            operator = ops[selectedOperator]
            correctAnswer = operator(self.frac1,self.frac2)
            
            # If they match then they at least get 0.5 points. Just need to check if they match exactly
            # TODO: If an answer is supposed to be reduced to 2, should it be required to enter 2/1 for full points or should 6/3 be accepted as well?
            resultMessage = ""
            points = 0.0
            if givenAnswer == correctAnswer:
                if ansNumer == correctAnswer.numerator and ansDenom == correctAnswer.denominator:
                    resultMessage = "Correct - good job!"
                    points = 1
                else:
                    resultMessage = "Partially Correct. Answer needs to be reduced. Correct answer is {0}".format(correctAnswer)
                    points = 0.5
            else:
                resultMessage = "Incorrect. Correct answer is {0}. Try another one!".format(correctAnswer)
                
            self.resultsLabel['text'] = resultMessage
            self.QuizzerSaveResultsToDatabase(selectedOperator, points)
            
            # Now reset to a new equation
            self.numerator['text'] = ""
            self.denominator['text'] = ""
            self.QuizzerSetRandomEquation()
        except ValueError:
            ErrorboxGeneratpr("Error: Please enter only integers for your answer.")
        except tk.TclError:
            ErrorboxGeneratpr("Error: Please select an operator.")
        self.denominator.delete(0, 'end')
        self.numerator.delete(0, 'end')
        
    def QuizzerSaveResultsToDatabase(self, points, operator):
        sqlite_file = 'fshdb.sqlite'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute("INSERT INTO results (ID, Operator, Average) VALUES (?,?,?)", (self.controller.username, points, operator,))
        conn.commit()
        conn.close()
        print("Save results for username '{0}'".format(self.controller.username), operator, points,)


class ViewResultsWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #TODO using (controller.username) Show table of the users results.
        label = tk.Label(self, text="ViewResultsWindow")
        label.pack(side="top", fill="x", pady=10)


        
        view = tk.Button(self, text='Show Scores', command=self.graph)
        view.pack()

        button = tk.Button(self, text="MainWindow",
                           command=lambda: controller.show_frame("MainWindow"))
        button.pack()
    def graph(self):
        objects = ('Addition', 'Subtraction', 'Multiplication', 'Division', 'OverAll')
        horiz = np.arange(len(objects))
        scores = [90, 80, 55, 75, 35]
        plt.bar(horiz, scores, align='center', alpha=0.5)
        plt.xticks(horiz, objects)
        plt.ylabel('Average')
        plt.title('Quiz Averages')
        plt.show()

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
