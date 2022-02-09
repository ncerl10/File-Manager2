from tkinter import *
from datetime import datetime
from tkinter import filedialog
import os
from pathlib import Path
try:
    from send2trash import send2trash
except Exception as e:
    print(e)

#importing necessary libraries and modules
def loadOptions():
    data = []
    dataReturn = []
    with open('options.txt') as f:
        data = f.readlines()
    for a in data: #filters through all the strings, finds a number (which is assumed to be the value associated with the data line) and appends it
        dataReturn.append(a[:-1])
    return dataReturn #returns only the value of each line of option in a list, in the following format: theme, deleteType 

def saveOptions(d): #the parameter d is a list in the same format as dataReturn
    with open('options.txt', "w") as f:
        for x in d:
          f.write(x+'\n')
background_colour = 'grey'
text_colour = 'white'

try:
    background_colour = loadOptions()[0]
    text_colour = loadOptions()[1]
except:
    pass

print(background_colour,text_colour)

root = Tk() #creating the screen
root.title("File manager") #editing the tile of the screen
root.geometry("600x200") #changing the dimension of the screen
root.config(bg=background_colour)
root.update_idletasks()

path = ""
file_chosen = False
label_error = Label(root)
dataLabel = ['themeID','deleteType'] 



def validate_date(y,m,d): #year, month, day
    common_year = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    leap_year = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if d.isdigit() and m.isdigit() and y.isdigit():
        dINT, mINT, yINT = int(d), int(m), int(y)
        if yINT % 4 == 0:
            if 0 < mINT < 13:
                if 0 < dINT <= leap_year[mINT - 1]:
                    return False
        else:
            if 0 < mINT < 13:
                if 0 < dINT <= common_year[mINT - 1]:
                    return False
    return True

def check_date(v, y, m, d, ny, nm, nd): #checks if the date fits the criteria
    print(y, ny)
    print(m, nm)
    print(d, nd)
    if v == "Before":
        if y < ny:
            return True
        if m < nm:
            return True
        if d < nd:
            return True
    if v == "After":
        if y > ny:
            return True
        if m > nm:
            return True
        if d > nd:
            return True
    if v == "On":
        if y != ny or m != nm or d != nd:
            return True
    return False
 
def confirm(): #activates when the confirm button starts
    def start():
        window.destroy()
        delcount = 0
        p = Path(path)
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
                elif clicked2.get() == "Equal to" and item.stat().st_size != size:
                    continue
            if var3.get() == 1:
                create_date = datetime.fromtimestamp(item.stat().st_ctime)
                create_date = str(create_date)
                create_year = int(create_date[:4])
                create_month = int(create_date[5:7])
                create_day = int(create_date[8:10])
                if check_date(clicked3.get(), int(e_year1.get()), int(e_month1.get()), int(e_day1.get()), create_year, create_month, create_day):
                    continue
            if var4.get() == 1:
                modify_date = datetime.fromtimestamp(item.stat().st_mtime)
                modify_date = str(modify_date)
                modify_year = int(modify_date[:4])
                modify_month = int(modify_date[5:7])
                modify_day = int(modify_date[8:10])
                if check_date(clicked4.get(), int(e_year2.get()), int(e_month2.get()), int(e_day2.get()), modify_year, modify_month, modify_day):
                    continue
            if var5.get() == 1:
                access_date = datetime.fromtimestamp(item.stat().st_atime)
                access_date = str(access_date)
                access_year = int(access_date[:4])
                access_month = int(access_date[5:7])
                access_day = int(access_date[8:10])
                if check_date(clicked5.get(), int(e_year3.get()), int(e_month3.get()), int(e_day3.get()), access_year, access_month, modify_day):
                    continue
            delcount += 1
            try:
                send2trash(item) #sends item to trash
            except Exception as error:
                
                print("error occured, deleting files instead of sending to trash: ")
                os.remove(item)
        try:
            background_colour = loadOptions()[0]
            text_colour = loadOptions()[1]
        except:
            pass    
        done = Toplevel() #creates a window to tell the user that files have been deleted
        done.config(bg=background_colour)
        label_done = Label(done, text= str(delcount)+ " files have been moved to the trash", bg=background_colour, fg=text_colour)
        button_done = Button(done, text="Ok", highlightbackground=background_colour, command=done.destroy)
        label_done.pack()
        button_done.pack()

    global label_error
    global file_chosen
    label_error.destroy()
    #input validation
    if file_chosen == False: #checks if the user has selected a file
        label_error = Label(root, text="Please choose a file", fg="red", bg="systemTransparent")
        label_error.grid(row=7, column=0, columnspan=2, sticky="w")
        return
    if var1.get() == 0 and var2.get() == 0 and var3.get() == 0 and var4.get() == 0 and var5.get() == 0: #checks if the user has selected at least one checkbox
        label_error = Label(root, text="Please choose at least one requirement", fg="red", bg="systemTransparent")
        label_error.grid(row=7, column=0, columnspan=3, sticky="w")
        return
    if var1.get() == 1 and e_file_type.get() == "": #checks if the user has inputed their file type
        label_error = Label(root, text="Please input a file type", fg="red", bg="systemTransparent")
        label_error.grid(row=7, column=0, columnspan=2, sticky="w")
        return
    if var1.get() == 1 and e_file_type.get()[0] != ".": #checks if the file type is inputed in the correct format
        label_error = Label(root, text="File type has to  with a .", fg="red", bg="systemTransparent")
        label_error.grid(row=7, column=0, columnspan=2, sticky="w")
        return
    if var2.get() == 1 and e_file_size.get() == "": #checks if the user has inputed their file size
        label_error = Label(root, text="Please input a file size", fg="red", bg="systemTransparent")
        label_error.grid(row=7, column=0, columnspan=2, sticky="w")
        return
    if var2.get() == 1 and e_file_size.get().isalpha(): #checks if the file size inputed is a number
        label_error = Label(root, text="Invalid input for file size", fg="red", bg="systemTransparent")
        label_error.grid(row=7, column=0, columnspan=2, sticky="w")
        return
    if var2.get() == 1: #check if the file size inputed is a positive number
        if float(e_file_size.get()) < 0: 
            label_error = Label(root, text="Invalid input for file size", fg="red", bg="systemTransparent")
            label_error.grid(row=7, column=0, columnspan=2, sticky="w")
            return
    if var3.get() == 1: #check if the creation date is inputed in the correct format
        if validate_date(e_year1.get(),e_month1.get(),e_day1.get()):
            label_error = Label(root, text="Invalid input for creation date", fg="red", bg="systemTransparent")
            label_error.grid(row=7, column=0, columnspan=2, sticky="w")
            return
    if var4.get() == 1: #check if the modification date is inputed in the correct format
        if validate_date(e_year2.get(),e_month2.get(),e_day2.get()):
            label_error = Label(root, text="Invalid input for modification date", fg="red", bg="systemTransparent")
            label_error.grid(row=7, column=0, columnspan=2, sticky="w")
            return
    if var5.get() == 1: #check if the accessed date is inputed in the correct format
        if validate_date(e_year3.get(),e_month3.get(),e_day3.get()):
            label_error = Label(root, text="Invalid input for accessed date", fg="red", bg="systemTransparent")
            label_error.grid(row=7, column=0, columnspan=2, sticky="w")
            return

    try:
        background_colour = loadOptions()[0]
        text_colour = loadOptions()[1]
    except:
        pass
    window = Toplevel() #creates a window to confirm if the user wants to start deleting files
    window.config(bg=background_colour)
    label = Label(window, text="Are you sure you want to start deleting files?", bg=background_colour, fg=text_colour)
    button_yes = Button(window, text="Yes", highlightbackground=background_colour, command=start)
    button_no = Button(window, text="No", highlightbackground=background_colour, command=window.destroy)
    label.grid(row=0, column=0, columnspan=2)
    button_yes.grid(row=1, column=0)
    button_no.grid(row=1, column=1)

def check(): #creates window to confirm if the user wants to quit the app
    try:
        background_colour = loadOptions()[0]
        text_colour = loadOptions()[1]
    except:
        pass
    window = Toplevel()
    window.config(bg=background_colour)
    label = Label(window, text="Are you sure you want to quit?", bg=background_colour, fg=text_colour)
    button_yes = Button(window, text="Yes", command=root.destroy, highlightbackground=background_colour)
    button_no = Button(window, text="No", command=window.destroy, highlightbackground=background_colour)
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
    try:
        background_colour = loadOptions()[0]
        text_colour = loadOptions()[1]
    except:
        pass
    window = Toplevel()
    window.config(bg=background_colour)
    label1 = Label(window, text="Instructions", bg=background_colour, fg=text_colour)
    label2 = Label(window, text="Start by choosing a folder which contents you would like to sort", bg=background_colour, fg=text_colour)
    label3 = Label(window, text="Next, select which parameters you would like to use", bg=background_colour, fg=text_colour)
    label4 = Label(window, text="Finally, fill up the necessary information then press confirm to start sorting", bg=background_colour, fg=text_colour)
    label5 = Label(window, text="The files will then be moved into your bin", bg=background_colour, fg=text_colour)
    close = Button(window, text="Close", command=window.destroy, highlightbackground=background_colour)
    label1.pack()
    label2.pack()
    label3.pack()
    label4.pack()
    label5.pack()
    close.pack()

def settings(): #activate when the user press the settings button
    def theme(a, b, quit): #changes the theme of the app
        global currSelect
        currSelect = [a,b]
        
        root.config(bg=a)
        
        label_folder_chosen.config(bg=a, fg=b)
        button_folder.config(highlightbackground=a)

        c1.config(bg=a)
        label_file_type.config(bg=a, fg=b)
        type_menu.config(bg=a)
        e_file_type.config(highlightbackground=a, bg=a, fg=b)

        c2.config(bg=a)
        label_file_size.config(bg=a, fg=b)
        menu.config(bg=a)
        e_file_size.config(highlightbackground=a, bg=a, fg=b)
        size_menu.config(bg=a)

        c3.config(bg=a)
        label_file_creation.config(bg=a, fg=b)
        timing_menu1.config(bg=a)
        e_day1.config(highlightbackground=a, bg=a, fg=b)
        label_dash1.config(bg=a, fg=b)
        e_month1.config(highlightbackground=a, bg=a, fg=b)
        label_dash2.config(bg=a, fg=b)
        e_year1.config(highlightbackground=a, bg=a, fg=b)

        c4.config(bg=a)
        label_file_modification.config(bg=a, fg=b)
        timing_menu2.config(bg=a)
        e_day2.config(highlightbackground=a, bg=a, fg=b)
        label_dash3.config(bg=a, fg=b)
        e_month2.config(highlightbackground=a, bg=a, fg=b)
        label_dash4.config(bg=a, fg=b)
        e_year2.config(highlightbackground=a, bg=a, fg=b)

        c5.config(bg=a)
        label_file_accessed.config(bg=a, fg=b)
        timing_menu3.config(bg=a)
        e_day3.config(highlightbackground=a, bg=a, fg=b)
        label_dash5.config(bg=a, fg=b)
        e_month3.config(highlightbackground=a, bg=a, fg=b)
        label_dash6.config(bg=a, fg=b)
        e_year3.config(highlightbackground=a, bg=a, fg=b)

        button_confirm.config(highlightbackground=a)
        button_quit.config(highlightbackground=a)
        button_help.config(highlightbackground=a)
        button_settings.config(highlightbackground=a)

        window.config(bg=a)
        label_theme.config(bg=a, fg=b)
        button_theme1.config(highlightbackground=a)
        button_theme2.config(highlightbackground=a)
        button_theme3.config(highlightbackground=a)
        button_save.config(highlightbackground=a)
        button_cancel.config(highlightbackground=a)

        if quit:
            window.destroy()

    def save():
        try:
            saveOptions(currSelect)
        except:
            pass
        window.destroy()
    try:
        background_colour = loadOptions()[0]
        text_colour = loadOptions()[1]
    except:
        pass
    window = Toplevel() #creates a menu that allows the user to change the theme of the app
    window.config(bg=background_colour)
    button_theme1 = Button(window, text="White", command= lambda: theme("white", "black", False), highlightbackground=background_colour)
    button_theme1.config(width=12)
    button_theme2 = Button(window, text="Black", command= lambda: theme("black", "white", False), highlightbackground=background_colour)
    button_theme2.config(width=12)
    button_theme3 = Button(window, text="Grey", command= lambda: theme("grey", "white", False), highlightbackground=background_colour)
    button_theme3.config(width=12)
    button_save = Button(window, text="Save", command=save, highlightbackground=background_colour)
    button_save.config(width=12)
    button_cancel = Button(window, text="Cancel", command= lambda: theme(background_colour, text_colour, True), highlightbackground=background_colour)
    button_cancel.config(width=12)
    label_theme = Label(window, text="Choose a theme", bg=background_colour, fg=text_colour)
    label_theme.grid(row=0, column=0)
    button_theme1.grid(row=1, column= 0)
    button_theme2.grid(row=1, column= 1)
    button_theme3.grid(row=1, column= 2)
    button_save.grid(row=2, column=0)
    button_cancel.grid(row=2, column=1)

chosen = StringVar()
chosen.set("Choose file")

#creating necessary labels
label_file_type = Label(root, text="File type", bg=background_colour, fg=text_colour)
label_file_size = Label(root, text="File size", bg=background_colour, fg=text_colour)
label_file_creation = Label(root, text="Creation date", bg=background_colour, fg=text_colour)
label_file_modification = Label(root, text="Modification date", bg=background_colour, fg=text_colour)
label_file_accessed = Label(root, text="Accessed date", bg=background_colour, fg=text_colour)
label_folder_chosen = Label(root, text="Chosen file", bg=background_colour, fg=text_colour)

label_dash1 = Label(root, text="-", bg=background_colour, fg=text_colour)
label_dash2 = Label(root, text="-", bg=background_colour, fg=text_colour)
label_dash3 = Label(root, text="-", bg=background_colour, fg=text_colour)
label_dash4 = Label(root, text="-", bg=background_colour, fg=text_colour)
label_dash5 = Label(root, text="-", bg=background_colour, fg=text_colour)
label_dash6 = Label(root, text="-", bg=background_colour, fg=text_colour)

#creating necessary buttons
button_quit = Button(root, text="Quit", command=check, width=7 , highlightbackground=background_colour)
button_confirm = Button(root, text="Confirm", command=confirm, width=9, highlightbackground=background_colour)
button_folder = Button(root, textvariable=chosen, command=folder, width=15, highlightbackground=background_colour)
button_help = Button(root, text="Help", command=instructions, width=7, highlightbackground=background_colour)
button_settings = Button(root, text="Settings", command=settings, width=12, highlightbackground=background_colour)

#creating necessary entries
e_file_type = Entry(root, width=9, highlightthickness=1)
e_file_type.config(highlightbackground=background_colour, bg=background_colour, fg=text_colour)
e_file_size = Entry(root, width=9, highlightthickness=1)
e_file_size.config(highlightbackground=background_colour, bg=background_colour, fg=text_colour)

e_day1 = Entry(root, width=3, justify="center", highlightthickness=1)
e_day1.insert(0, "dd")
e_day1.config(bg=background_colour, fg=text_colour, highlightbackground=background_colour)
e_month1 = Entry(root, width=3, justify="center", highlightthickness=1)
e_month1.insert(0, "mm")
e_month1.config(bg=background_colour, fg=text_colour, highlightbackground=background_colour)
e_year1 = Entry(root, width=4, justify="center", highlightthickness=1)
e_year1.insert(0, "yyyy")
e_year1.config(bg=background_colour, fg=text_colour, highlightbackground=background_colour)

e_day2 = Entry(root, width=3, justify="center", highlightthickness=1)
e_day2.insert(0, "dd")
e_day2.config(bg=background_colour, fg=text_colour, highlightbackground=background_colour)
e_month2 = Entry(root, width=3, justify="center", highlightthickness=1)
e_month2.insert(0, "mm")
e_month2.config(bg=background_colour, fg=text_colour, highlightbackground=background_colour)
e_year2 = Entry(root, width=4, justify="center", highlightthickness=1)
e_year2.insert(0, "yyyy")
e_year2.config(bg=background_colour, fg=text_colour, highlightbackground=background_colour)

e_day3 = Entry(root, width=3, justify="center", highlightthickness=1)
e_day3.insert(0, "dd")
e_day3.config(bg=background_colour, fg=text_colour, highlightbackground=background_colour)
e_month3 = Entry(root, width=3, justify="center", highlightthickness=1)
e_month3.insert(0, "mm")
e_month3.config(bg=background_colour, fg=text_colour, highlightbackground=background_colour)
e_year3 = Entry(root, width=4, justify="center", highlightthickness=1)
e_year3.insert(0, "yyyy")
e_year3.config(bg=background_colour, fg=text_colour, highlightbackground=background_colour)

#creating necessary variables for the option menus
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

#creating necessary option menus
size_menu = OptionMenu(root, clicked1, *sizes)
size_menu.config(width=4, bg=background_colour)
menu = OptionMenu(root, clicked2, "Greater than", "Less than", "Equal to")
menu.config(width=9, bg=background_colour)
timing_menu1 = OptionMenu(root, clicked3, "Before", "After", "On")
timing_menu1.config(width=9, bg=background_colour)
timing_menu2 = OptionMenu(root, clicked4, "Before", "After", "On")
timing_menu2.config(width=9, bg=background_colour)
type_menu = OptionMenu(root, clicked5, "is", "is not")
type_menu.config(width=9, bg=background_colour)
timing_menu3 = OptionMenu(root, clicked6, "Before", "After", "On")
timing_menu3.config(width=9, bg=background_colour)

var1 = IntVar() #creating integer variables which is used for the checkboxes
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
var5 = IntVar()

#creating necessary checkboxes
c1 = Checkbutton(root, variable=var1, bg=background_colour) #creating checkbox variables
c2 = Checkbutton(root, variable=var2, bg=background_colour)
c3 = Checkbutton(root, variable=var3, bg=background_colour)
c4 = Checkbutton(root, variable=var4, bg=background_colour)
c5 = Checkbutton(root, variable=var5, bg=background_colour)

label_folder_chosen.grid(row=0, column=0) #adding items for the first row of the screen
button_folder.grid(row=0, column=1, columnspan=2) 

c1.grid(row=1, column=0) #adding items for the second row of the screen
label_file_type.grid(row=1, column=1, sticky="w", columnspan=2) 
type_menu.grid(row=1, column=3, sticky="w") 
e_file_type.grid(row=1, column=4, columnspan=3) 

c2.grid(row=2, column=0) #adding items for the third row of the screen
label_file_size.grid(row=2, column=1, sticky="w", columnspan=2) 
menu.grid(row=2, column=3, sticky="w") 
e_file_size.grid(row=2, column=4, columnspan=3) 
size_menu.grid(row=2, column=7, columnspan=2, sticky="w") 

c3.grid(row=3, column=0) #adding items for the fourth row of the screen
label_file_creation.grid(row=3, column=1, sticky="w", columnspan=2) 
timing_menu1.grid(row=3, column=3, sticky="w")
e_day1.grid(row=3, column=4, sticky="e")
label_dash1.grid(row=3, column=5)
e_month1.grid(row=3, column=6, sticky="w")
label_dash2.grid(row=3, column=7)
e_year1.grid(row=3, column=8, sticky="w")

c4.grid(row=4, column=0) #adding items for the fifth row of the screen
label_file_modification.grid(row=4, column=1, sticky="w", columnspan=2)
timing_menu2.grid(row=4, column=3, sticky="w")
e_day2.grid(row=4, column=4, sticky="e")
label_dash3.grid(row=4, column=5)
e_month2.grid(row=4, column=6, sticky="w")
label_dash4.grid(row=4, column=7)
e_year2.grid(row=4, column=8, sticky="w")

c5.grid(row=5, column=0) #adding items for the sixth row of the screen
label_file_accessed.grid(row=5, column=1, sticky="w", columnspan=2)
timing_menu3.grid(row=5, column=3, sticky="w")
e_day3.grid(row=5, column=4, sticky="e")
label_dash5.grid(row=5, column=5)
e_month3.grid(row=5, column=6, sticky="w")
label_dash6.grid(row=5, column=7)
e_year3.grid(row=5, column=8, sticky="w")

button_confirm.grid(row=6, column=0) #adding items for the seventh row of the screen
button_quit.grid(row=6, column=1)
button_help.grid(row=6, column=2)
button_settings.grid(row=6, column=3, sticky="w")

root.mainloop()
