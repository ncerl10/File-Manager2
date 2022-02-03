from tkinter import *
import os
from datetime import datetime
from tkinter import filedialog
from pathlib import Path
from tkinter import ttk
import time

#importing necessary libraries and modules

root = Tk() #creating the screen
root.title("File manager") #editing the tile of the screen
root.geometry("700x300") #changing the dimension of the screen
root.config(bg="black")

path = ""
file_chosen = False
label_error = Label(root)

def validate(y,m,d): #year, month, day
    Output = 1
    if d.isdigit() and m.isdigit() and y.isdigit():
        dINT = int(d)
        mINT = int(m)

        if dINT < 32 and dINT > 0 and mINT < 13 and mINT > 0:
            Output = 0
    return Output

        
    
def confirm():
    def start():
        delcount = 0
        p = Path(path)
        length = len(list(p.glob("**/*")))
        count = 0
        for item in p.glob("**/*"):
            count += 1
            if var1.get() == 1:
                if clicked5.get() == "is" and item.suffix != e_file_type.get():
                    continue
                elif clicked5.get() == "is not" and item.suffix == e_file_type.get():
                    continue
            if var2.get() == 1:
                size = float(e_file_size.get()) * 1000 ** (sizes.index(clicked1.get())+1)
                if clicked2.get() == "Greater than" and item.stat().st_size < size:
                    continue
                elif clicked2.get() == "Less than" and item.stat().st_size > size:
                    continue
            if var3.get() == 1:
                create_date = datetime.fromtimestamp(item.stat().st_ctime)
                create_date = str(create_date)
                create_year = int(create_date[:4])
                create_month = int(create_date[5:7])
                create_day = int(create_date[8:10])
                create_hour = int(create_date[11:13])
                create_minute = int(create_date[14:16])
                create_second = int(create_date[17:19])
                print(create_date, create_year, e_year1.get())
                if clicked3.get() == "Before" and int(e_year1.get()) < create_year:
                    continue
                elif clicked3.get() == "Before" and int(e_month1.get()) < create_month:
                    continue
                elif clicked3.get() == "Before" and int(e_day1.get()) < create_day:
                    continue
                if clicked3.get() == "After" and int(e_year1.get()) > create_year:
                    continue
                elif clicked3.get() == "After" and int(e_month1.get()) > create_month:
                    continue
                elif clicked3.get() == "After" and int(e_day1.get()) > create_day:
                    continue
            if var4.get() == 1:
                modify_date = datetime.fromtimestamp(item.stat().st_mtime)
                modify_date = str(modify_date)
                modify_year = int(modify_date[:4])
                modify_month = int(modify_date[5:7])
                modify_day = int(modify_date[8:10])
                modify_hour = int(modify_date[11:13])
                modify_minute = int(modify_date[14:16])
                modify_second = int(modify_date[17:19])
                if clicked4.get() == "Before" and int(e_year2.get()) < modify_year:
                    continue
                elif clicked4.get() == "Before" and int(e_month2.get()) < modify_month:
                    continue
                elif clicked4.get() == "Before" and int(e_day2.get()) < modify_day:
                    continue
                if clicked4.get() == "After" and int(e_year2.get()) > modify_year:
                    continue
                elif clicked4.get() == "After" and int(e_month2.get()) > modify_month:
                    continue
                elif clicked4.get() == "After" and int(e_day2.get()) > modify_day:
                    continue
            if var5.get() == 1:
                access_date = datetime.fromtimestamp(item.stat().st_atime)
                access_date = str(access_date)
                access_year = int(access_date[:4])
                access_month = int(access_date[5:7])
                access_day = int(access_date[8:10])
                access_hour = int(access_date[11:13])
                access_minute = int(access_date[14:16])
                access_second = int(access_date[17:19])
                if clicked5.get() == "Before" and int(e_year3.get()) < access_year:
                    continue
                elif clicked5.get() == "Before" and int(e_month3.get()) < access_month:
                    continue
                elif clicked5.get() == "Before" and int(e_day3.get()) < access_day:
                    continue
                if clicked5.get() == "After" and int(e_year3.get()) > access_year:
                    continue
                elif clicked5.get() == "After" and int(e_month3.get()) > access_month:
                    continue
                elif clicked5.get() == "After" and int(e_day3.get()) > access_day:
                    continue
            delcount += 1
            os.remove(item)
        
        done = Toplevel() #creates a window to tell the user that files have been deleted
        label_done = Label(done, text= str(delcount)+ " files have been deleted")
        button_done = Button(done, text="Ok", command=done.destroy)
        label_done.pack()
        button_done.pack()

    global label_error
    global file_chosen
    label_error.destroy()
    if file_chosen == False: #checks if the user has selected a file
        label_error = Label(root, text="Please choose a file", fg="red")
        label_error.grid(row=7, column=0, columnspan=2)
        return
    if var1.get() == 0 and var2.get() == 0 and var3.get() == 0 and var4.get() == 0 and var5.get() == 0: #checks if the user has selected at least one checkbox
        label_error = Label(root, text="Please choose at least one requirement", fg="red")
        label_error.grid(row=7, column=0, columnspan=3)
        return
    if var1.get() == 1 and e_file_type.get() == "": #checks if the user has inputed their file type
        label_error = Label(root, text="Please input a file type", fg="red")
        label_error.grid(row=7, column=0, columnspan=2)
        return
    if var1.get() == 1 and e_file_type.get()[0] != ".": #checks if the file type is inputed in the correct format
        label_error = Label(root, text="File type has to  with a .", fg="red")
        label_error.grid(row=7, column=0, columnspan=2)
        return
    if var2.get() == 1 and e_file_size.get() == "": #checks if the user has inputed their file size
        label_error = Label(root, text="Please input a file size", fg="red")
        label_error.grid(row=7, column=0, columnspan=2)
        return
    if var2.get() == 1 and e_file_size.get().isalpha(): #checks if the file size inputed is a number
        label_error = Label(root, text="Invalid input for file size", fg="red")
        label_error.grid(row=7, column=0, columnspan=2)
        return
    if var2.get() == 1: #check if the file size inputed is a positive number
        if float(e_file_size.get()) < 0: 
            label_error = Label(root, text="Invalid input for file size", fg="red")
            label_error.grid(row=7, column=0, columnspan=2)
            return
    if var3.get() == 1: #check if the creation date is inputed in the correct format
        if validate(e_year1.get(),e_month1.get(),e_day1.get()):
            label_error = Label(root, text="Invalid input for creation date", fg="red")
            label_error.grid(row=7, column=0, columnspan=2)
            return
    if var4.get() == 1: #check if the modification date is inputed in the correct format
        if validate(e_year2.get(),e_month2.get(),e_day2.get()):
            label_error = Label(root, text="Invalid input for modification date", fg="red")
            label_error.grid(row=7, column=0, columnspan=2)
            return
    if var5.get() == 1: #check if the accessed date is inputed in the correct format
        if validate(e_year3.get(),e_month3.get(),e_day3.get()):
            label_error = Label(root, text="Invalid input for accessed date", fg="red")
            label_error.grid(row=7, column=0, columnspan=2)
            return

    window = Toplevel() #creates a window to confirm if the user wants to start deleting files
    label = Label(window, text="Are you sure you want to start deleting files?")
    button_yes = Button(window, text="Yes", command=start)
    button_no = Button(window, text="No", command=window.destroy)
    label.grid(row=0, column=0, columnspan=2)
    button_yes.grid(row=1, column=0)
    button_no.grid(row=1, column=1)

def check(): #creates window to confirm if the user wants to quit the app
    window = Toplevel()
    label = Label(window, text="Are you sure you want to quit?")
    button_yes = Button(window, text="Yes", command=root.destroy)
    button_no = Button(window, text="No", command=window.destroy)
    label.grid(row=0, column=0, columnspan=2)
    button_yes.grid(row=1, column=0)
    button_no.grid(row=1, column=1)

def folder(): #allows the user to select a file
    global path
    global file_chosen
    folder = filedialog.askdirectory(initialdir="/")
    if folder != "":
        a = folder.split("/")
        chosen_folder = a[len(a) - 1]
        chosen.set(chosen_folder)
        path = folder
        file_chosen = True

def instructions(): #creates window with list of instructions
    window = Toplevel()
    label1 = Label(window, text="Instructions")
    label2 = Label(window, text="Start by choosing a folder which contents you would like to sort")
    label3 = Label(window, text="Next, select which parameters you would like to use")
    label4 = Label(window, text="Finally, fill up the necessary information then press confirm to start sorting")
    close = Button(window, text="Close", command=window.destroy)
    label1.pack()
    label2.pack()
    label3.pack()
    label4.pack()
    close.pack()

chosen = StringVar()
chosen.set("Choose file")

label_file_type = Label(root, text="File type", bg="black", fg="white")
label_file_size = Label(root, text="File size", bg="black", fg="white")
label_file_creation = Label(root, text="Creation date", bg="black", fg="white")
label_file_modification = Label(root, text="Modification date", bg="black", fg="white")
label_file_accessed = Label(root, text="Accessed date", bg="black", fg="white")
label_folder_chosen = Label(root, text="Chosen file", bg="black", fg="white")

label_dash1 = Label(root, text="-", bg="black", fg="white")
label_dash2 = Label(root, text="-", bg="black", fg="white")
label_dash3 = Label(root, text="-", bg="black", fg="white")
label_dash4 = Label(root, text="-", bg="black", fg="white")
label_dash5 = Label(root, text="-", bg="black", fg="white")
label_dash6 = Label(root, text="-", bg="black", fg="white")

button_quit = Button(root, text="Quit", command=check, highlightbackground="black")
button_confirm = Button(root, text="Confirm", command=confirm, highlightbackground="black")
button_folder = Button(root, textvariable=chosen, command=folder, width=15, highlightbackground="black")
button_help = Button(root, text="Help", command=instructions, highlightbackground="black")

e_file_type = Entry(root, width=9, highlightthickness=1)
e_file_type.config(highlightbackground="black", bg="black", fg="white", highlightcolor="white")
e_file_size = Entry(root, width=9, highlightthickness=1)
e_file_size.config(highlightbackground="black", bg="black", fg="white", highlightcolor="white")

e_day1 = Entry(root, width=3, justify="center", highlightthickness=1)
e_day1.insert(0, "dd")
e_day1.config(bg="black", fg="white", highlightbackground="black", highlightcolor="white")
e_month1 = Entry(root, width=3, justify="center", highlightthickness=1)
e_month1.insert(0, "mm")
e_month1.config(bg="black", fg="white", highlightbackground="black", highlightcolor="white")
e_year1 = Entry(root, width=4, justify="center", highlightthickness=1)
e_year1.insert(0, "yyyy")
e_year1.config(bg="black", fg="white", highlightbackground="black", highlightcolor="white")

e_day2 = Entry(root, width=3, justify="center", highlightthickness=1)
e_day2.insert(0, "dd")
e_day2.config(bg="black", fg="white", highlightbackground="black", highlightcolor="white")
e_month2 = Entry(root, width=3, justify="center", highlightthickness=1)
e_month2.insert(0, "mm")
e_month2.config(bg="black", fg="white", highlightbackground="black", highlightcolor="white")
e_year2 = Entry(root, width=4, justify="center", highlightthickness=1)
e_year2.insert(0, "yyyy")
e_year2.config(bg="black", fg="white", highlightbackground="black", highlightcolor="white")

e_day3 = Entry(root, width=3, justify="center", highlightthickness=1)
e_day3.insert(0, "dd")
e_day3.config(bg="black", fg="white", highlightbackground="black", highlightcolor="white")
e_month3 = Entry(root, width=3, justify="center", highlightthickness=1)
e_month3.insert(0, "mm")
e_month3.config(bg="black", fg="white", highlightbackground="black", highlightcolor="white")
e_year3 = Entry(root, width=4, justify="center", highlightthickness=1)
e_year3.insert(0, "yyyy")
e_year3.config(bg="black", fg="white", highlightbackground="black", highlightcolor="white")

sizes = ["KB", "MB", "GB", "TB"]

clicked1 = StringVar()
clicked1.set(sizes[1])
clicked2 = StringVar()
clicked2.set("Greater than")
clicked3 = StringVar()
clicked3.set("Before")
clicked4 = StringVar()
clicked4.set("Before")
clicked5 = StringVar()
clicked5.set("is")
clicked6 = StringVar()
clicked6.set("Before")

size_menu = OptionMenu(root, clicked1, *sizes)
size_menu.config(width=4, bg="black")
menu = OptionMenu(root, clicked2, "Greater than", "Less than", "Equal to")
menu.config(width=9, bg="black")
timing_menu1 = OptionMenu(root, clicked3, "Before", "After", "On")
timing_menu1.config(width=9, bg="black")
timing_menu2 = OptionMenu(root, clicked4, "Before", "After", "On")
timing_menu2.config(width=9, bg="black")
type_menu = OptionMenu(root, clicked5, "is", "is not")
type_menu.config(width=9, bg="black")
timing_menu3 = OptionMenu(root, clicked6, "Before", "After", "On")
timing_menu3.config(width=9, bg="black")

var1 = IntVar() #creating integer variables which is used for the checkboxes
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
var5 = IntVar()

c1 = Checkbutton(root, variable=var1, bg="black") #creating checkbox variables
c2 = Checkbutton(root, variable=var2, bg="black")
c3 = Checkbutton(root, variable=var3, bg="black")
c4 = Checkbutton(root, variable=var4, bg="black")
c5 = Checkbutton(root, variable=var5, bg="black")

label_folder_chosen.grid(row=0, column=0) #adding items for the first row of the screen
button_folder.grid(row=0, column=1) 

c1.grid(row=1, column=0) #adding items for the second row of the screen
label_file_type.grid(row=1, column=1, sticky="w") 
type_menu.grid(row=1, column=2, sticky="w") 
e_file_type.grid(row=1, column=3, columnspan=3) 

c2.grid(row=2, column=0) #adding items for the third row of the screen
label_file_size.grid(row=2, column=1, sticky="w") 
menu.grid(row=2, column=2, sticky="w") 
e_file_size.grid(row=2, column=3, columnspan=3) 
size_menu.grid(row=2, column=6, columnspan=2, sticky="w") 

c3.grid(row=3, column=0) #adding items for the fourth row of the screen
label_file_creation.grid(row=3, column=1, sticky="w") 
timing_menu1.grid(row=3, column=2, sticky="w")
e_day1.grid(row=3, column=3, sticky="e")
label_dash1.grid(row=3, column=4)
e_month1.grid(row=3, column=5, sticky="w")
label_dash2.grid(row=3, column=6)
e_year1.grid(row=3, column=7, sticky="w")

c4.grid(row=4, column=0) #adding items for the fifth row of the screen
label_file_modification.grid(row=4, column=1, sticky="w")
timing_menu2.grid(row=4, column=2, sticky="w")
e_day2.grid(row=4, column=3, sticky="e")
label_dash3.grid(row=4, column=4)
e_month2.grid(row=4, column=5, sticky="w")
label_dash4.grid(row=4, column=6)
e_year2.grid(row=4, column=7, sticky="w")

c5.grid(row=5, column=0) #adding items for the sixth row of the screen
label_file_accessed.grid(row=5, column=1, sticky="w")
timing_menu3.grid(row=5, column=2, sticky="w")
e_day3.grid(row=5, column=3, sticky="e")
label_dash5.grid(row=5, column=4)
e_month3.grid(row=5, column=5, sticky="w")
label_dash6.grid(row=5, column=6)
e_year3.grid(row=5, column=7, sticky="w")

button_confirm.grid(row=6, column=0) #adding items for the seventh row of the screen
button_quit.grid(row=6, column=1)
button_help.grid(row=6, column=2)

root.mainloop()
