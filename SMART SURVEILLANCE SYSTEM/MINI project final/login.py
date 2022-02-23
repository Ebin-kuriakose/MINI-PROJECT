import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os,sys
from tkinter.font import BOLD




class LoginPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self, bg="#dfe300", height=431, width=626)  # this is the background
        main_frame.pack(fill="both", expand="true")

        

        self.geometry("626x431")  # Sets window size to 626w x 431h pixels
        self.resizable(0, 0)  # This prevents any resizing of the screen
        title_styles = {"font": ("Verdana", 14 ,BOLD),
                       "background": "#dfe300",
                       "foreground": "BLACK"}


        text_styles = {"font": ("Verdana", 14 ,BOLD),
                       "background": "#dfe300",
                       "foreground": "BLACK"}

        frame_login = tk.Frame(main_frame, bg="", relief="groove", bd=2)  # this is the frame that holds all the login details and buttons
        frame_login.place(rely=0.120, relx=0.17, height=150, width=400)
       
       

        label_title = tk.Label(frame_login, title_styles, text="LOGIN PAGE")
        label_title.grid(row=0, column=1, columnspan=1)

        label_user = tk.Label(frame_login, text_styles, text="USERNAME:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(frame_login, text_styles, text="PASSWORD:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(frame_login, width=45, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(frame_login, width=45, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(frame_login, text="Login", command=lambda: getlogin())
        button.place(rely=0.70, relx=0.50)

        signup_btn = ttk.Button(frame_login, text="Register", command=lambda: get_signup())
        signup_btn.place(rely=0.70, relx=0.75)

        def get_signup():
            SignupPage()

        def getlogin():
            username = entry_user.get()
            password = entry_pw.get()
            # if your want to run the script as it is set validation = True
            validation = validate(username, password)
            if validation:
                tk.messagebox.showinfo("Login Successful",
                                       "Welcome {}".format(username))

                os.system('python app.py')                       
                root.deiconify()
                #top.destroy()
            else:
                tk.messagebox.showerror("Information", "The Username or Password you have entered are incorrect ")

        def validate(username, password):
            # Checks the text file for a username/password combination.
            try:
                with open("credentials.txt", "r") as credentials:
                    for line in credentials:
                        line = line.split(",")
                        if line[1] == username and line[3] == password:
                            return True
                    return False
            except FileNotFoundError:
                print("You need to Register first or amend Line 71 to     if True:")
                return False


class SignupPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # main_frame = tk.Frame(self, bg="#3F6BAA", height=150, width=250)
        # main_frame.place(rely=0.30, relx=0.17, height=150, width=400)
        # pack_propagate prevents the window resizing to match the widgets

        main_frame = tk.Frame(self, bg="#dfe300", height=431, width=626)  # this is the background
        main_frame.pack(fill="both", expand="true")
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")

        main_frame2 = tk.Frame(main_frame, bg="", relief="groove", bd=2)  # this is the frame that holds all the login details and buttons
        main_frame2.place(rely=0.20, relx=0.17, height=150, width=400)

        self.geometry("550x350")
        self.resizable(0, 0)

        self.title("Registration")

        text_styles = {"font": ("Verdana", 14 ,BOLD),
                       "background": "#dfe300",
                       "foreground": "BLACK"}

        label_user = tk.Label(main_frame2, text_styles, text="NEW USERNAME:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(main_frame2, text_styles, text="NEW PASSWORD:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(main_frame2, width=20, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(main_frame2, width=20, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(main_frame2, text="Create Account", command=lambda: signup())
        button.grid(row=4, column=1)

        def signup():
            # Creates a text file with the Username and password
            user = entry_user.get()
            pw = entry_pw.get()
            validation = validate_user(user)
            if not validation:
                tk.messagebox.showerror("Information", "That Username already exists")
            else:
                if len(pw) > 3:
                    credentials = open("credentials.txt", "a")
                    credentials.write(f"Username,{user},Password,{pw},\n")
                    credentials.close()
                    tk.messagebox.showinfo("Information", "Your account details have been stored.")
                    SignupPage.destroy(self)

                else:
                    tk.messagebox.showerror("Information", "Your password needs to be longer than 3 values.")

        def validate_user(username):
            # Checks the text file for a username/password combination.
            try:
                with open("credentials.txt", "r") as credentials:
                    for line in credentials:
                        line = line.split(",")
                        if line[1] == username:
                            return False
                return True
            except FileNotFoundError:
                return True
class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, bg="#84CEEB", height=600, width=1024)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        # self.resizable(0, 0) prevents the app from being resized
        # self.geometry("1024x600") fixes the applications size
        self.frames = {}

# top = LoginPage()
# top.title("Tkinter App Template - Login Page")
# root = MyApp()
# root.withdraw()
# #root.title("Tkinter App Template")

# root.mainloop()  
root = LoginPage()
root.title("SMART SURVEILLANCE SYSTEM")
root.mainloop()    