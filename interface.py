from tkinter import *
from PIL import ImageTk,Image
import os

def loadInterface():
    class Root(Tk):
        def __init__(self):
            super(Root, self).__init__()

            self.title("Python Tkinter")
            # self.minsize(500, 400)

    root = Root()
    global img

    # getting screen width and height of display
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    # setting tkinter window size
    root.geometry("%dx%d" % (width, height))
    root.title("Query Annotation")

    LabelHead = Label(root, font=("Arial", 25), text="Query Annotation")
    LabelHead.grid(row=0, column=3, padx=(250, 10), pady=(20, 50))

    #firstpanel
    LabelFirst = Label(root, font=("Arial", 25), text="Schemas")
    LabelFirst.grid(row=1,column=1)
    Lb1 = Listbox(root, height=25, bg="white" )
    # Lb1.insert(1, "Cust(..)")
    # Lb1.insert(2, "Dept(..)")
    # Lb1.insert(3, "Trans(..)")
    # Lb1.grid(row=2,column=1)
    ## update to new insert after connection - change this to take from parameter
    processed_schemas = ["Customer", "Department", "Transaction"]
    for idx, val in enumerate(processed_schemas):
        Lb1.insert(idx, val)
    Lb1.grid(row=2,column=1)

    #secondpanel
    LabelSecond = Label(root, font=("Arial", 25), text="Input Query")
    LabelSecond.grid(row=1, column=3)
    e = Text(root, width=75, borderwidth=2, height=25, bg="white" )
    e.grid(row=2,column=3)
    # e.insert(0,"Enter SQL query:")

    #Put a empty label between for gap between panel 2 and 3
    spacer1 = Label(root, text="          ")
    spacer1.grid(row=2, column=0)
    spacer2 = Label(root, text="          ")
    spacer2.grid(row=2, column=2)
    spacer3 = Label(root, text="          ")
    spacer3.grid(row=2, column=4)


    #thirdpanel
    # canvas.create_rectangle(5, 50, 100, 200, fill="blue", outline="black", state='disabled')
    LabelThird = Label(root, font=("Arial", 25), text="Query Execution Plan")
    LabelThird.grid(row=1, column=5)
    rectangle_1 = Label(root, text="For QEP Visualisation...", bg="white", fg="black", width=55, height=25)
    rectangle_1.grid(ipadx=5, ipady=5, row=2, column=5)
    # thirdpanel.grid(row=0,column=2)

    def createAnnotation(numOfAnnotation, secondLabel):
        ##delete previous texts
        # e.delete('1.0', END)
        canvas = Canvas(e, width=600, height=400)
        canvas.grid(row=1, column=1)
        queryLabel = Label(canvas, text=secondLabel)
        print(queryLabel)

        canvas.create_text(0, 0, text=secondLabel, fill="black")

        for i in range(numOfAnnotation):
            ##gets item_index for location (not yet implemented)
            canvas.create_line(500, (i*50)+20, 300, (i*60)+15, arrow=LAST)
            buttonBG = canvas.create_rectangle(400, (i*50)+10, 600, (i*50)+50, fill="white", outline="blue")
            buttonTXT = canvas.create_text(500, (i*50)+25, text="Annotations...."+str(1+i))
            canvas.tag_bind(buttonBG, "<Button-1>", btnClick)  ## when the square is clicked runs function "clicked".
            canvas.tag_bind(buttonTXT, "<Button-1>", btnClick)  ## same, but for the text.

    def loadImage():
        path = "graphical_qep.png"
        img = ImageTk.PhotoImage(Image.open(path).resize((400, 400), Image.ANTIALIAS))
        # resized = img.resize((400, 400), Image.ANTIALIAS)
        panel = Label(root, image=img)
        panel.photo = img
        panel.grid(ipadx=5, ipady=5, row=2,column=5)


    def btnClick():
        ## get inputs and selected items

        # add panel item here - to be removed...
        secondLabel = e.get("1.0",'end-1c')

        for i in Lb1.curselection():
            print(Lb1.get(i))
            firstLabel = Label(root, text=Lb1.get(i))
            firstLabel.grid(row=3,column=3)

        #get connection and run output - file should be stored for retrieval.. (call project.py to run)
        loadImage()

        ## pass in a list of annotation - in integer
        numOfAnnotation = 4;
        createAnnotation(numOfAnnotation, secondLabel)
        # panel = Label(root, image=img)
        # panel.pack(side="bottom", fill="both", expand="yes")

    #restart program..
    def btnClear():
        """Restarts the current program.
            Note: this function does not return. Any cleanup action (like
            saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, *sys.argv)
        # canvas.delete(buttonBG)
        # root.destroy()
        # root = Root()
        # root.mainloop()


    submitButton = Button(root, text="Submit!", command=btnClick)
    submitButton.grid(row=4,column=3)
    clearButton = Button(root, text="Clear", command=btnClear)
    clearButton.grid(row=4,column=3, padx=(100, 200))

    root.mainloop()

