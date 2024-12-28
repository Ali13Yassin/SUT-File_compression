#------------------------------------<Initialization Start>-------------------------------------------------------
from tkinter import * #The UI module that this program relies on
from tkinter import messagebox #This is a function that allows making windows message boxes, has to be called separetly
from tkinter.ttk import * #Theamed tkinter which makes the UI look ever so slightly modern
from tkinter.filedialog import askopenfilename
import os
from pathlib import Path
import threading
import backend as backend
# from PIL import Image, ImageTk
import webbrowser
from tkinter import messagebox

os.chdir(Path(__file__).parent) #Changes cmd directory to the one that has the py file
root_location = Path(__file__).parent #The location of the main file

#Checks if the required python files exist
# if os.path.exists("Corefunctions.py") and os.path.exists("Exportfunctions.py"):
#     from Corefunctions import * #The library I made that handles backend operations
#     from Exportfunctions import * #The library I made that exports information
# else:
#     messagebox.showerror("Error", "Critical files are missing, please redownload the application to function properly.")
#     quit()

#Starts the program
def start():
    # filecheck()#Checks if other database files exist and creates them
    window() #Defines properties of the main window
    mainmenu() #The first menu to the application
    wind.mainloop() #Makes the window apear

#Defines properties of the main window
def window():
    global wind,div,fnt #Defines the main window, and div and font as global variables
    wind = Tk()
    # wind.iconbitmap("imgs/dog2.ico")  # Set the icon
    centx = int((wind.winfo_screenwidth() - 800) / 2) #Gets coordinates of where to center the window on x-axis
    centy = int((wind.winfo_screenheight() - 500) / 2) #Gets coordinates of where to center the window on y-axis
    wind.geometry("800x500+{}+{}".format(centx, centy)) #Centers the window
    wind.title("File compression project")
    fnt = "Manrope" #To be able to change font through one change
    div = Frame(wind) #Funny name from html that's not gonna cause issues at all lolol
    div.pack() #The frame keeps the layout decent

def mainmenu():
    global main_frame, style #To clear last menu when coming back
    port_num = StringVar()
    DivisionFrame = Frame(wind)
    DivisionFrame.pack(fill='both', expand=True)
    # Configure the grid
    DivisionFrame.grid_rowconfigure(0, weight=0)  # 20% of the space goes here
    DivisionFrame.grid_rowconfigure(1, weight=10)  # 80% of the space goes here
    DivisionFrame.grid_columnconfigure(0, weight=1)
    style = Style()
    style.configure("navbar.TFrame", background="#391D0D")
    style.configure("Custom2.TFrame", background="#6F3F29")
    style.configure("Title.TLabel", background="#391D0D", foreground="white", font=(fnt, 15, "bold"), padding=(5, 0))
    style.configure("navbutton.TLabel", background="#A5622F", foreground="white", font=(fnt, 12))  # Change the font of the text
    style.map("navbutton.TLabel",foreground=[('pressed', '#391D0D'), ('active', 'white')],background=[('pressed', '!disabled', '#FFE7D4'), ('active', '#E99A5D')])
    navbar = Frame(DivisionFrame, style="navbar.TFrame")
    navbar.grid(row=0, column=0, sticky="nsew")
    main_frame = Frame(DivisionFrame, style="Custom2.TFrame")
    main_frame.grid(row=1, column=0, sticky="nsew")
    Label(navbar, text="File compression project", style="Title.TLabel").grid(row=0, column=0)
    Button(navbar, text="Compress", command=compress_menu, style="navbutton.TLabel").grid(row=0, column=1, padx=10, pady=10)
    Button(navbar, text="Decompress", command=compress_menu, style="navbutton.TLabel").grid(row=0, column=2, padx=10, pady=10)
    Button(navbar, text="About", command=settings_menu, style="navbutton.TLabel").grid(row=0, column=3, padx=10, pady=10)
    compress_menu() #Starts the server menu

#------------------------------------<Initialization End>-------------------------------------------------------
#------------------------------------<Menus Start>-------------------------------------------------------
def compress_menu():
    clear() #Clears the previous menu
    server_back = Frame(main_frame, style="Custom2.TFrame")
    server_back.pack(expand=True)

    Label(server_back, text="Choose text file", style="Title.TLabel").grid(row=0, column=0)
    Label(server_back, text="Any text based file ex(.txt .html .css) works!", style="Title.TLabel").grid(row=1, column=0)
    
    upload_frame = Frame(server_back, style="Custom2.TFrame")
    upload_frame.grid(row=2, column=0)
    style.configure("server_off_button.TLabel", background="#A5622F", foreground="white", font=(fnt, 20, "bold"), padding=(10, 10))  # Change the font of the text
    style.map("server_off_button.TLabel",foreground=[('pressed', '#391D0D'), ('active', 'white')],background=[('pressed', '!disabled', '#FFE7D4'), ('active', '#E99A5D')])
    
    def uploader():
                global file_path
                file_path = askopenfilename()
                if file_path:
                    File_name_label.config(text=os.path.basename(file_path))

    Button(upload_frame, text="Upload", command=uploader, style="server_off_button.TLabel").grid(row=0, column=0)
    File_name_label = Label(upload_frame, text="No file uploaded", style="Title.TLabel")
    File_name_label.grid(row=0, column=1)

    Label(server_back, text="Select compression/encoding type", style="Title.TLabel").grid(row=0, column=0)
    compression_method = StringVar(value="huff")
    style.configure("TRadiobutton", background="#6F3F29", foreground="white", font=(fnt, 12))
    Radiobutton(server_back, text="Huffman", variable=compression_method, value="huff", style="TRadiobutton").grid(row=4, column=0, padx=10, pady=5)
    Radiobutton(server_back, text="Run-Length", variable=compression_method, value="run-length", style="TRadiobutton").grid(row=5, column=0, padx=10, pady=5)
    
    def compress_button():
        if file_path:
            if compression_method.get() == "huff":
                backend.huff_encoder(file_path)
            elif compression_method.get() == "run-length":
                backend.run_length_encode(file_path)

    Button(server_back, text="Compress", command=compress_button, style="server_off_button.TLabel").grid(row=6, column=0)



def view_files_menu(action):
    new_window = Toplevel(wind)
    new_window.title("Server files")
    back_frame = Frame(new_window, style="navbar.TFrame")
    back_frame.pack(fill='both', expand=True)
    # Create a Treeview widget
    tree = Treeview(back_frame)

    # Define columns
    tree["columns"] = ("Name", "Size", "Type")

    # Format columns
    tree.column("#0", width=0, stretch=NO)
    tree.column("Name", anchor=W, width=200)
    tree.column("Size", anchor=W, width=100)
    tree.column("Type", anchor=W, width=100)

    # Create headings
    tree.heading("#0", text="", anchor=W)
    tree.heading("Name", text="Name", anchor=W)
    tree.heading("Size", text="Size", anchor=W)
    tree.heading("Type", text="Type", anchor=W)

    # Add data to the treeview
    lines = clienter.list_files()
    for i in range(len(lines)):
        name = lines[i].split()[-1]
        size = lines[i].split()[-5]
        if lines[i].split()[0] == "drwxrwxrwx":
            Filetype = "Directory"
        else:
            Filetype = "File"
        tree.insert("", "end", text=i, values=(name, size, Filetype))

    # Display the treeview
    tree.pack(fill=BOTH, expand=True)
    if action == 1:
        def download():
            selected_items = tree.selection()
            for item in selected_items:
                clienter.download_file(tree.item(item)["values"][0])
        Button(back_frame, text="Download", command=download, style="navbutton.TLabel").pack(pady=10)

    elif action == 2:
        tree = Treeview(new_window, columns=("File Name", "Size", "Type"), selectmode='browse')
        def upload():
            from tkinter.filedialog import askopenfilename
            file_path = askopenfilename()
            if file_path:
                selected_items = tree.selection()
                if selected_items != ():
                    clienter.change_directory(tree.item(selected_items[0])["values"][0])
                clienter.upload_file(file_path)
                new_window.destroy()
        def new_fold():
            new_fold_name = StringVar()
            Entry_frame = Frame(back_frame)
            Entry_frame.pack(pady=5)
            selected_items = tree.selection()
            def confirm():
                if selected_items != ():
                    clienter.change_directory(tree.item(selected_items[0])["values"][0])
                clienter.create_directory(new_fold_name.get())
                new_window.destroy()
            Label(Entry_frame, text="New folder name:").grid(row=0, column=0)
            Entry(Entry_frame, textvariable=new_fold_name).grid(row=0, column=1)
            Button(Entry_frame, text="Create", command=confirm).grid(row=0, column=2)
            selected_items = tree.selection()
        Button(back_frame, text="Upload", command=upload, style="navbutton.TLabel").pack(pady=5)
        Button(back_frame, text="Create new folder", command=new_fold, style="navbutton.TLabel").pack(pady=5)
    elif action == 0:
        def delete():
            selected_items = tree.selection()
            if messagebox.askyesno("Warning", "Are you sure you want to delete the selected files?"):
                for item in selected_items:
                    clienter.delete_file(tree.item(item)["values"][0])
                new_window.destroy()
        Button(back_frame, text="Delete selected items", command=delete, style="navbutton.TLabel").pack(pady=5)

def settings_menu():
    clear() #Clears the previous menu
    setting_back = Frame(main_frame, style="Custom2.TFrame")
    setting_back.pack(fill='both', expand=True)
    setting_back.grid_columnconfigure(0, weight=1)
    setting_back.grid_columnconfigure(1, weight=1)
    setting_back.grid_rowconfigure(0, weight=1)
    options_frame = VerticalScrolledFrame(setting_back, style="Custom2.TFrame")
    options_frame.grid(row=0, column=0, sticky='nsew')

    #Description frame
    style.configure("desc_title.TLabel", background="#6F3F29", foreground="white", font=(fnt, 25, "bold"))
    style.configure("desc_version.TLabel", background="#6F3F29", foreground="white", font=(fnt, 10))
    style.configure("desc_repo.TLabel", background="#6F3F29", foreground="white", font=(fnt, 15))
    description_frame = Frame(setting_back, style="Custom2.TFrame")
    description_frame.grid(row=0, column=1, sticky='nsew')
    # img = ImageTk.PhotoImage(Image.open("imgs/dog2.jpg"))
    # image_label = Label(description_frame, image=img)
    # image_label.image = img
    # image_label.pack()
    Label(description_frame, text="FTP project", style="desc_title.TLabel").pack()
    Label(description_frame, text="Version 1.0", style="desc_version.TLabel").pack()

    #Redirect to repo
    Repo_frame = Frame(description_frame, style="Custom2.TFrame")
    img2 = ImageTk.PhotoImage(Image.open("imgs/GitHub2.png"))
    image_git = Label(Repo_frame, image=img2, style="desc_repo.TLabel")
    image_git.image = img2
    image_git.grid(row=0, column=0)
    Button(Repo_frame, text="See GitHub repo", style="desc_repo.TLabel",command=lambda: webbrowser.open("https://github.com/Ali13Yassin/The-Ethel-Project")).grid(row=0, column=1)
    Repo_frame.pack(padx=10, pady=10)

    #Settings options

    def settings_visual_load():
        #TODO: load the settings from the settings file then apply them to the checkboxes
        pass
    #This makes the settings save when any checkbox is pressed
    def on_checkbutton_press():
        #TODO: call the function that saves the settings
        pass
    
    
    #All the settings are stored in these variables
    checkbutton_logs = IntVar()

    checkbutton_autosave = IntVar()
    
    style.configure('Settings_checkbox.TCheckbutton', background='#391D0D', indicatorbackground='#E99A5D', indicatorcolor='#391D0D', foreground='#A5622F', focuscolor='#E99A5D')
    ftp_settings_frame = Frame(options_frame.interior, style="navbar.TFrame")
    ftp_settings_frame.pack(padx=10, pady=10)
    Label(ftp_settings_frame, text="FTP settings", style="Title.TLabel").grid(row=0, column=0)
    Label(ftp_settings_frame, text="Server logs", style="settings.TLabel").grid(row=1, column=0)
    Checkbutton(ftp_settings_frame, style="Settings_checkbox.TCheckbutton", command=lambda: on_checkbutton_press(), variable=checkbutton_logs).grid(row=1, column=1)
    

    easy_settings_frame = Frame(options_frame.interior, style="navbar.TFrame")
    easy_settings_frame.pack(padx=10, pady=10)
    Label(easy_settings_frame, text="Easy transfer settings", style="Title.TLabel").grid(row=0, column=0)
    Label(easy_settings_frame, text="Auto Accept", style="settings.TLabel").grid(row=1, column=0)
    Checkbutton(easy_settings_frame, style="Settings_checkbox.TCheckbutton", command=lambda: on_checkbutton_press(), variable=checkbutton_autosave).grid(row=1, column=1)

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set, bg="#6F3F29")
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = Frame(canvas, style="Custom2.TFrame")
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


#------------------------------------<Menus End>-------------------------------------------------------
#------------------------------------<General Start>-------------------------------------------------------
#Used as a placeholder for menus I didn't add
def placeholder():
    print("Button pressed")

#Deletes the widgets from previous menu and cleares memory from them
def clear():
    for widget in main_frame.winfo_children():
        widget.destroy() #Used this instead of forget to clear memory

#------------------------------------<General End>-------------------------------------------------------
start() #Starts the application