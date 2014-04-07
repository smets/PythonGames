# Quiz
class Quiz(object):
    def __init__(self, questions):
        self.Questions = questions
        self.Score = 0
    def startQuiz(self):
        for i in range(0,3):
            print "Question "+(i+1)
            self.Questions[i].ask()
            self.Score += self.Questions.isRight
        self.printData()
    def printData(self):
        print "The results are in!"
        print "Total Score: "+self.Score
        for i in range(0,3):
            print "Question "+(i+1)
            print self.Questions[i]
