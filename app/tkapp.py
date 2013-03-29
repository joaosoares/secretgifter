
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        # Create objects for program
        self.people = List()
       # people.SaveList()
       # Test().List(people)
       
        self.createWidgets()

    def createWidgets(self):
        self.LOAD = tk.Button(self)
        self.LOAD["text"] = "Load participants"
        self.LOAD["command"] = self.loadFile
        self.LOAD.pack({"side":"left"})
        
        self.START = tk.Button(self, text="Start Draw",
                        command=self.startDraw )
        self.START.pack()
        self.SEND = tk.Button(self, text="")

    def loadFile(self):
        filename = tkFileDialog.askopenfile(filetypes=[("csv","*.csv")])
        self.people.LoadFromCSV(filename)
    
    def startDraw(self):
        new_draw = Draw(self.people.GetParticipants())
        Test().Draw(new_draw)


