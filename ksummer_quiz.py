# Quiz Taker
# Kaci Summerton
# Steven Mets

class Question(object):

    def __init__(self, question, answers, correct):
        self.question = question
        self.answers = answers
        self.correct = correct
        self.attempt = 0
        self.isRight = 0

    def __str__(self):
        rep = "\tAttempts: " + str(self.attempt) + "\tScore: " + str(self.isRight)
        return rep

    def ask(self):
        num = 0
        self.attempt += 1
        print(self.question)
        for answer in self.answers:
            num += 1
            print("\t" + str(num) + ". " + answer)
        cont =  True
        while cont:
            choice = input("\nAnswer:  ")
            try:
                int(choice)
                cont = False
            except ValueError:
                print("Invalid input. Please choose a number.")
        if (int(choice) - 1) != self.correct:
            if self.attempt >= 2:
                print("Incorrect.")
            else:
                print("Incorrect. Please try again.")
                self.ask()
        else:
            self.isRight = 1

class Quiz(object):
    
    def __init__(self, questions):
        self.Questions = questions
        self.Score = 0
    def startQuiz(self):
        for i in range(len(self.Questions)):
            print("\nQuestion " + str((i+1)))
            self.Questions[i].ask()
            self.Score += self.Questions[i].isRight
        self.printData()
    def printData(self):
        print("\nThe results are in!")
        print("\nTotal Score:  " + str(self.Score))
        for i in range(len(self.Questions)):
            print("Question "+ str((i+1)))
            print(self.Questions[i])
    

            
# main

# initalize variables

questions = [None,None,None,None]

question = "Which of the following most accurately describes a computer program?"
answers = [None, None, None, None]
answers[0] = "A collection of objects, all of the same type"
answers[1] = "A collection of objects of different type"
answers[2] = "A list of instructions for objects to perform certain actions"
answers[3] = "A set of instructions telling the computer how to perform tasks"
correct = 3;
    
questions[0] = Question(question, answers, correct)
question = "What is an algorithm?"
answers[0] = "A collection of objects, all of the same type"
answers[1] = "A sequence of steps that are going to help you complete a task"
answers[2] = "A list of instructions to perform certain actions"
answers[3] = "All of the above"
correct = 1;
 
questions[1] = Question(question, answers, correct)
question = "What are variables?"
answers[0] = "Variables are used to store data in a program"
answers[1] = "Variables are used to represent the data"
answers[2] = "Each variables have a unique name"
answers[3] = "All of the above"
correct = 3;
questions[2] = Question(question, answers, correct)

question = "How did we use variables in our app?"
answers[0] = "We used variables to make the block editor bigger"
answers[1] = "We used variables to store 'count'"
answers[2] = "We used variables to eliminate loops"
answers[3] = "We used variables to solve a problem"
correct = 1;
questions[3] = Question(question, answers, correct)

take = True
quiz = Quiz(questions)
while take:
    quiz.startQuiz()
    choice = input("Would you like to take the quiz again? [Y/N]:  ")
    if choice == "N":
        take = False
    elif choice == "Y":
        take = True
    else:
        print("Invalid choice. Exiting quiz.")
        take = False

input("\n\nPress the enter key to exit.")
