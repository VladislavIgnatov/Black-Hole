# Black-Hole
Requirements
Login window with login or new user creation. Accepted login brings the main window. Initially, accept any password. After everything else is working, add user authentication.
Main window: buttons for Solver, Quizzer, View Results and Quit.
Solver window: fields for the user to enter two fractions and an operator and a solve button. Pressing the button shows the answer. Also, buttons for new equation and quit
Quizzer window: presents equations to solve. The user chooses the operator, then an equation is presented with randomly chosen nonzero numerator and positive denominator. The user enters her answer and it is checked. The score for this question is 1.0 for correct and reduced answer, 0.5 for correct value but not reduced and 0.0 otherwise. Could also have a button to show the solution (but only if the user has entered her own answer)
View Results window: shows, for each operator and all operators, the user's averages vs average for all users. How to show scores as bar charts: https://plot.ly/python/bar-charts/
Database fields: userid VARCHAR(10) operator VARCHAR(1) score FLOAT
Basic tutorial on SQL: http://www.sqlcourse2.com/intro2.html
Fraction format: entry box for numerator, '/' character, entrybox for denominator
