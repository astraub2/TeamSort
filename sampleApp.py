#sample app

from Tkinter import *
import webbrowser

class Application(Frame):

    def say_hi(self):
        print "hi there, everyone!"
    def callback(self):
        webbrowser.open_new(r"http://www.google.com")

    def userinput(self):
        a = raw_input(self.E1.get())
        print a

    #def getSize(self):
        

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "right"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

        self.LINK = Button(self)
        self.LINK["text"] = "Google Hyperlink"
        self.LINK["command"] = self.callback
        self.LINK.pack({"side": "left"})

        # self.label1 = Label( root, text="Group Size:")
        # self.E1 = Entry(root, bd =5)
        # self.label1.pack({"side": "bottom"})
        # self.E1.pack({"side": "bottom"})
        self.label1 = Label( root, text="Group Size:")
        self.E1 = Entry(root, bd =5)
        self.label1.pack({"side": "left"})
        self.E1.pack({"side": "left"})

        self.submit = Button(self)
        self.submit["text"] = "Submit"
        self.submit["command"] = self.userinput
        self.submit.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()