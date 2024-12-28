#------------------------------------<Initialization Start>-------------------------------------------------------
from tkinter import * #The UI module that this program relies on
from tkinter import messagebox #This is a function that allows making windows message boxes, has to be called separetly
from tkinter.ttk import * #Theamed tkinter which makes the UI look ever so slightly modern
from tkinter.filedialog import askopenfilename
import os
from pathlib import Path
import threading
# from PIL import Image, ImageTk
import webbrowser
from tkinter import messagebox

os.chdir(Path(__file__).parent) #Changes cmd directory to the one that has the py file
root_location = Path(__file__).parent #The location of the main file

# Checks if the required python files exist
if os.path.exists("backend.py"):
    import backend as backend
else:
    messagebox.showerror("Error", "Critical files are missing, please redownload the application to function properly.")
    quit()

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
    DivisionFrame = Frame(wind)
    DivisionFrame.pack(fill='both', expand=True)
    # Configure the grid
    DivisionFrame.grid_rowconfigure(0, weight=0)  # 20% of the space goes here
    DivisionFrame.grid_rowconfigure(1, weight=10)  # 80% of the space goes here
    DivisionFrame.grid_columnconfigure(0, weight=1)
    style = Style()
    style.configure("navbar.TFrame", background="#391D0D")
    style.configure("Custom2.TFrame", background="#6F3F29")
    style.configure("Title.TLabel", background="#6F3F29", foreground="white", font=(fnt, 15, "bold"), padding=(5, 0))
    style.configure("Titlet.TLabel", background="#391D0D", foreground="white", font=(fnt, 15, "bold"), padding=(5, 0))
    style.configure("navbutton.TLabel", background="#A5622F", foreground="white", font=(fnt, 12))  # Change the font of the text
    style.map("navbutton.TLabel",foreground=[('pressed', '#391D0D'), ('active', 'white')],background=[('pressed', '!disabled', '#FFE7D4'), ('active', '#E99A5D')])
    navbar = Frame(DivisionFrame, style="navbar.TFrame")
    navbar.grid(row=0, column=0, sticky="nsew")
    main_frame = Frame(DivisionFrame, style="Custom2.TFrame")
    main_frame.grid(row=1, column=0, sticky="nsew")
    Label(navbar, text="File compression project", style="Titlet.TLabel").grid(row=0, column=0)
    Button(navbar, text="Compress", command=compress_menu, style="navbutton.TLabel").grid(row=0, column=1, padx=10, pady=10)
    Button(navbar, text="Decompress", command=decompress_menu, style="navbutton.TLabel").grid(row=0, column=2, padx=10, pady=10)
    Button(navbar, text="About", command=settings_menu, style="navbutton.TLabel").grid(row=0, column=3, padx=10, pady=10)
    compress_menu() #Starts the server menu

#------------------------------------<Initialization End>-------------------------------------------------------
#------------------------------------<Menus Start>-------------------------------------------------------
def compress_menu():
    clear() #Clears the previous menu
    compress_back = Frame(main_frame, style="Custom2.TFrame")
    compress_back.pack(expand=True)

    Label(compress_back, text="Choose text file", style="Titlet.TLabel").grid(row=0, column=0)
    Label(compress_back, text="Any text based file ex(.txt .html .css) works!", style="Titlet.TLabel").grid(row=1, column=0)
    
    upload_frame = Frame(compress_back, style="Custom2.TFrame")
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

    Label(compress_back, text="Select Compression/Encoding type", style="Title.TLabel").grid(row=3, column=0)
    compression_method = StringVar(value="huff")
    style.configure("TRadiobutton", background="#6F3F29", foreground="white", font=(fnt, 12))
    Radiobutton(compress_back, text="Huffman", variable=compression_method, value="huff", style="TRadiobutton").grid(row=4, column=0, padx=10, pady=5)
    Radiobutton(compress_back, text="Run-Length", variable=compression_method, value="run-length", style="TRadiobutton").grid(row=5, column=0, padx=10, pady=5)
    
    def compress_button():
        if file_path:
            if compression_method.get() == "huff":
                result = backend.huff_encoder(file_path)
                if result:
                    messagebox.showinfo("Error", "File compression Failed!\n{}".format(result))
                else:
                    output_file = os.path.join('Huffman compressed ' + os.path.basename(file_path))
                    messagebox.showinfo("Success", 'File compressed successfully!\nSaved as "{}"'.format(output_file))
            elif compression_method.get() == "run-length":
                result = backend.run_length_encode(file_path)
                if result:
                    messagebox.showinfo("Error", "File compression Failed!\n{}".format(result))
                else:
                    output_file = os.path.join('run-length compressed ' + os.path.basename(file_path))
                    messagebox.showinfo("Success", 'File compressed successfully!\nSaved as "{}"'.format(output_file))

    Button(compress_back, text="Compress", command=compress_button, style="server_off_button.TLabel").grid(row=6, column=0)

def decompress_menu():
    clear() #Clears the previous menu
    decode_back = Frame(main_frame, style="Custom2.TFrame")
    decode_back.pack(expand=True)

    Label(decode_back, text="Choose text file", style="Titlet.TLabel").grid(row=0, column=0)
    Label(decode_back, text="Any text based file ex(.txt .html .css) works!", style="Titlet.TLabel").grid(row=1, column=0)
    
    upload_frame = Frame(decode_back, style="Custom2.TFrame")
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

    Label(decode_back, text="Select Decompression/Decoding type", style="Title.TLabel").grid(row=3, column=0)
    compression_method = StringVar(value="huff")
    style.configure("TRadiobutton", background="#6F3F29", foreground="white", font=(fnt, 12))
    Radiobutton(decode_back, text="Huffman", variable=compression_method, value="huff", style="TRadiobutton").grid(row=4, column=0, padx=10, pady=5)
    Radiobutton(decode_back, text="Run-Length", variable=compression_method, value="run-length", style="TRadiobutton").grid(row=5, column=0, padx=10, pady=5)
    
    def decompress_button():
        if file_path:
            if compression_method.get() == "huff":
                result = backend.decode_file(file_path)
                if result:
                    messagebox.showinfo("Error", "File decompression Failed!\n{}".format(result))
                else:
                    output_file = os.path.join('Huffman decompressed ' + os.path.basename(file_path))
                    messagebox.showinfo("Success", 'File decompressed successfully!\nSaved as "{}"'.format(output_file))
                    
            elif compression_method.get() == "run-length":
                result = backend.run_length_decode(file_path)
                if result:
                    messagebox.showinfo("Error", "File decompression Failed!\n{}".format(result))
                else:
                    output_file = os.path.join('run-length decompressed ' + os.path.basename(file_path))
                    messagebox.showinfo("Success", 'File decompressed successfully!\nSaved as "{}"'.format(output_file))
            

    Button(decode_back, text="Decompress", command=decompress_button, style="server_off_button.TLabel").grid(row=6, column=0)


def settings_menu():
    clear() #Clears the previous menu
    setting_back = Frame(main_frame, style="Custom2.TFrame")
    setting_back.pack(expand=True)

    #Description frame
    style.configure("desc_title.TLabel", background="#6F3F29", foreground="white", font=(fnt, 25, "bold"))
    style.configure("desc_version.TLabel", background="#6F3F29", foreground="white", font=(fnt, 10))
    style.configure("desc_repo.TLabel", background="#6F3F29", foreground="white", font=(fnt, 15))
    style.map("desc_repo.TLabel", foreground=[('pressed', '#391D0D'), ('active', 'white')], background=[('pressed', '!disabled', '#FFE7D4'), ('active', '#E99A5D')])
    
    description_frame = Frame(setting_back, style="Custom2.TFrame")
    description_frame.grid(row=0, column=0, sticky='nsew')
    
    Label(description_frame, text="SUT file compression project", style="desc_title.TLabel").pack()
    Label(description_frame, text="Version 1.0", style="desc_version.TLabel").pack()
    Label(description_frame, text="Made by Ali Yassin, Seif Waheed, Omar Abduh", style="desc_version.TLabel").pack()

    #Redirect to repo
    Button(description_frame, text="See GitHub repo", style="desc_repo.TLabel", command=lambda: webbrowser.open("https://github.com/Ali13Yassin/SUT-File_compression")).pack()

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