# Mad Lib
# Create a story based on user input
from tkinter import *

class Application(Frame):
    """ GUI application that creates a story based on user input. """
    def __init__(self, master):
        """ Initialize Frame. """
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """ Create widgets to get story information and to display story. """
        # create instruction label
        self.instrLbl = Label(self,
            text = "Enter information for a new story"
            ).grid(row = 0, column = 0, columnspan = 2, sticky = W)

        # create a label and text entry for the name of a person
        self.personLbl = Label(self,
                            text = "Person: "
                            ).grid(row = 1, column = 0, sticky = W)
        self.person_ent = Entry(self)
        self.person_ent.grid(row = 1, column = 1, sticky = W)

        # Select a Pronoun (Added)
        self.pronounLbl = Label(self,
              text = "Pronoun: "
              ).grid(row = 1, column = 2, sticky = W)
        self.pronoun = StringVar()
        self.pronoun.set(None)
        
        pronouns = ["he", "she"]
        columnOffset = 0
        self.pronounRad = [None,None]
        for pro in pronouns:
            self.pronounRad[columnOffset] = Radiobutton(self,
                                                        text = pro,
                                                        variable = self.pronoun,
                                                        value = pro
                                                        ).grid(row = 1, column = 3+columnOffset, sticky = W)
            columnOffset += 1
        # Input a Place (Added)
        self.placeLbl = Label(self,
                                text = "A Place: "
                                ).grid(row = 2,column = 0, sticky = W)
        self.placeEnt = Entry(self)
        self.placeEnt.grid(row = 2, column = 1, sticky = W)

        # First Noun (Added)
        self.noun1Lbl = Label(self,
                                text = "Noun: "
                                ).grid(row = 3,column = 0, sticky = W)
        self.noun1Ent = Entry(self)
        self.noun1Ent.grid(row = 3, column = 1, sticky = W)

        # Verb (Added)
        self.verbLbl = Label(self,
                                text = "Verb: "
                                ).grid(row = 4,column = 0, sticky = W)
        self.verbEnt = Entry(self)
        self.verbEnt.grid(row = 4, column = 1, sticky = W)

        # Select Adjectives (Added)
        self.adjLbl = Label(self,
                                text = "Adjective: "
                                ).grid(row = 5,column = 0, sticky = W)

        adjectives = ["powerful","lame", "studly"]
        self.adjVars = [BooleanVar(),BooleanVar(),BooleanVar()]
        
        self.adjCheckBoxes = [None,None,None]
        index = 0
        offset = 0
        for adj in adjectives:
            self.adjCheckBoxes[index] = Checkbutton(self,
                                                    text = adjectives[index],
                                                    variable = self.adjVars[index]
                                                    ).grid(row = 5, column = 1+index+offset, sticky = W)
            index+=1
            if index == 2:
                offset =1


    
        # Input Emotion (Added)
        self.emotionLbl = Label(self,
                                text = "Emotion: "
                                ).grid(row = 2,column = 4, sticky = W)
        self.emotionEnt = Entry(self)
        self.emotionEnt.grid(row = 2, column = 5, sticky = W)

        #Have another noun (Added)
        self.noun2Lbl = Label(self,
                                text = "Another Noun: "
                                ).grid(row = 3,column = 4, sticky = W)
        self.noun2Ent = Entry(self);
        self.noun2Ent.grid(row = 3, column = 5, sticky = W)

        # And a container to put it in (Added)
        self.containerLbl = Label(self,
                                text = "A Container: "
                                ).grid(row = 4,column = 4, sticky = W)
        self.containerEnt = Entry(self)
        self.containerEnt.grid(row = 4, column = 5, sticky = W)

        #This is the same as before, just generate the story
        self.storyButton = Button(self,
                                  text = "Click for a story",
                                  command = self.tell_story
                                  ).grid(row = 6, column = 0, columnspan = 6)

        self.story_txt = Text(self, width = 75, height = 10, wrap = WORD)
        self.story_txt.grid(row= 7, column = 0, columnspan = 6)
        
    def tell_story(self):
        """ Fill text box with new story based on user input. """
        #I changed the story generator,
        #Now it uses search/replace to put the new words into the story
        #Instead of putting in the words as you build the story
        story="<Person> was walking through the <Place> "
        story+="one day when <Pro> saw a huge <Noun1>. <Pro_Cap> decided to "
        story+="<Verb> the <Noun1> to prove how <Adj> <Pro> was, "
        story+="but <Pro> failed. In a fit of <Emotion>, <Pro> took a "
        story+="<Noun2> out of <Pro_Pos> <Container> and smashed the <Noun1> to pieces."

        story = story.replace("<Person>", self.person_ent.get());
        story = story.replace("<Pro>", self.pronoun.get());
        story = story.replace("<Place>", self.placeEnt.get())
        story = story.replace("<Noun1>", self.noun1Ent.get())
        story = story.replace("<Verb>", self.verbEnt.get());
        story = story.replace("<Emotion>", self.emotionEnt.get());
        story = story.replace("<Noun2>", self.noun2Ent.get());
        story = story.replace("<Container>",self.containerEnt.get());

        if self.pronoun.get() == "he":
            story = story.replace("<Pro_Cap>","He")
            story = story.replace("<Pro_Pos>", "his")
        if self.pronoun.get() == "she":
            story = story.replace("<Pro_Cap>","She");
            story = story.replace("<Pro_Pos>", "her");

        adjs = "";
        #powerful
        if self.adjVars[0].get():
            adjs += "powerful"
        #lame
        if self.adjVars[1].get():
            if self.adjVars[0].get():
                if self.adjVars[2].get():
                    adjs+= ", "
                if not self.adjVars[2].get():
                    adjs+=" and "
            adjs+= "lame"
        #studly
        if self.adjVars[2].get():
            if self.adjVars[0].get() or self.adjVars[1].get():
                adjs+= " and "
            adjs += "studly"

        story = story.replace("<Adj>", adjs)
        
        # display the story
        self.story_txt.delete(0.0, END)
        self.story_txt.insert(0.0, story)

# main
root = Tk()
root.title("Mad Lib")
app = Application(root)
root.mainloop()
