from tkinter import *
from tkinter import font as tkFont
from PIL import ImageTk, Image
import os
import project

submit_button_pressed = False


def loadInterface(processed_schemas):
    class Root(Tk):
        def __init__(self):
            super(Root, self).__init__()

            self.title("Python Tkinter")
            # self.minsize(500, 400)

    global img, root, message_label, listbox_schemas, input_text, canvas, submit_button
    root = Root()

    # getting screen width and height of display
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    # setting tkinter window size
    root.geometry("%dx%d" % (width, height))
    root.title("Query Annotator")

    label_head = Label(root, font=("Helvetica", 25), text="Query Annotator")
    label_head.grid(row=0, column=3, padx=(250, 10), pady=(20, 50))

    # first panel
    label_first = Label(root, font=("Helvetica", 20), text="Schemas")
    label_first.grid(row=1,column=1)
    listbox_schemas = Listbox(root, height=25, bg="white")

    for idx, val in enumerate(processed_schemas):
        listbox_schemas.insert(idx, val)
    listbox_schemas.grid(row=2,column=1)

    canvas = Canvas(root, width=600, height=400, borderwidth=2, bg="white")
    canvas.grid(row=2, column=3)

    # second panel
    label_second = Label(root, font=("Helvetica", 20), text="Input Query")
    label_second.grid(row=1, column=3)
    input_text = Text(canvas, width=45, borderwidth=2, height=25, font=('Helvetica', 10))
    canvas.create_window(0, 0, window=input_text, anchor="nw", tag='input_text')

    spacer1 = Label(root, text="       ")
    spacer1.grid(row=2, column=0)
    spacer2 = Label(root, text="       ")
    spacer2.grid(row=2, column=2)
    spacer3 = Label(root, text="       ")
    spacer3.grid(row=2, column=4)

    # third panel
    # canvas.create_rectangle(5, 50, 100, 200, fill="blue", outline="black", state='disabled')
    label_third = Label(root, font=("Helvetica", 20), text="Query Execution Plan")
    label_third.grid(row=1, column=5)
    rectangle_1 = Label(root, text="", bg="white", fg="black", width=55, height=25)
    rectangle_1.grid(ipadx=5, ipady=5, row=2, column=5)

    # bottom row
    message_label = Label(root, text='Please select the schema and enter your query.', font=('Helvetica', 16))
    message_label.grid(row=3, column=3)
    submit_button = Button(root, text="Submit!", command=lambda: btnClick(), width=10, height=1)
    submit_button.grid(row=4, column=3)
    helvetica14 = tkFont.Font(family='Helvetica', size=14)
    submit_button['font'] = helvetica14

    root.mainloop()


def loadImage():
    global panel
    path = "graphical_qep.png"
    img = ImageTk.PhotoImage(Image.open(path).resize((400, 400), Image.ANTIALIAS))
    # resized = img.resize((400, 400), Image.ANTIALIAS)
    panel = Label(root, image=img, bg='white')
    panel.photo = img
    panel.grid(ipadx=5, ipady=5, row=2,column=5)


def removeImage():
    global panel
    panel.config(image='')


def btnClick():
    global submit_button_pressed, input_text
    if not submit_button_pressed:
        ## get inputs and selected items

        # add panel item here - to be removed...
        sql_query = input_text.get("1.0",'end-1c')
        selected_schema = None

        for i in listbox_schemas.curselection():
            print(listbox_schemas.get(i))
            selected_schema = listbox_schemas.get(i)

        if selected_schema is None:
            message_label.config(text='Please select a schema!')
        else:
            print('first:', selected_schema)
            print(sql_query)
            project.process_query(selected_schema, sql_query)
    else:
        canvas.delete('annotations')
        submit_button.config(text='Annotate!')
        input_text = Text(canvas, width=45, borderwidth=2, height=25, font=('Helvetica', 10))
        canvas.create_window(0, 0, window=input_text, anchor="nw", tag='input_text')
        message_label.config(text='Please enter another query.')
        submit_button_pressed = not submit_button_pressed
        removeImage()


def create_annotation(annotations):
    for i in range(len(annotations)):
        ##gets item_index for location (not yet implemented)
        canvas.create_line(500, (i*50)+20, 300, (i*60)+15, arrow=LAST, tag='annotations')
        buttonBG = canvas.create_rectangle(400, (i*50)+10, 600, (i*50)+50, fill="white", outline="blue", tag='annotations')
        buttonTXT = canvas.create_text(500, (i*50)+25, text=annotations[i].construct_annotation_string(), tag='annotations')
        canvas.tag_bind(buttonBG, "<Button-1>", btnClick)  ## when the square is clicked runs function "clicked".
        canvas.tag_bind(buttonTXT, "<Button-1>", btnClick)  ## same, but for the text.
    # canvas.update()


def display_message(message):
    message_label.config(text=message)


# displays graphical QEP and changes button text
def display_query_success(sql_query):
    global submit_button_pressed
    loadImage()
    canvas.delete('input_text')
    canvas.create_text(5, 5, text=sql_query, anchor='nw', font=('Helvetica', 10), tag='annotations', width=325)
    submit_button.config(text='New Query')
    message_label.config(text='Query Annotated!')
    submit_button_pressed = not submit_button_pressed
