import customtkinter as ctk
from PIL import Image
import os
from cryptography.fernet import Fernet
from CTkMessagebox import CTkMessagebox
from config import firebase_config
from frames import dashbord, signin, signup

# setup default theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Set key for decrypt and encrypt password
key = Fernet.generate_key()
if os.path.exists(".\\key\\refKey.txt"):
    pass
else:
    f = open(".\\key\\refKey.txt", "wb")
    f.write(key)
    f.close()

# Create root page
class Application(ctk.CTk):
    # __init__ function for class Application
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        ctk.CTk.__init__(self, *args, **kwargs)
        self.signin_frame = signin.Signin_Page
        self.signup_frame = signup.Signup_Page
        self.dashbord_frame = dashbord.Dashboard_Page
        self.firebase_conf = firebase_config.FirebaseConfig()
        self.user_id, self.patient_id, self.user = None, None, None
        self.user_dict, self.patient_dict, self.physical__dict = firebase_config.User, firebase_config.Patient, firebase_config.Physical

        ## --------- ENV VARIABLES -------------##
        os.environ['PATIENT_INFO'] = str(None)
        os.environ['CAP_START'] = str(False)
        os.environ['USER_INFO'] = str(None)
        ## --------- END ENV VARIABLES ---------##

        self.current_version = '1.0'

        self.title(f"Practice Physical Therapy v{self.current_version}")

        # creating a container
        container=ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        self.grid_columnconfigure(1, weight=1, minsize=830)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # initializing frames to an empty array
        self.frames={}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (self.signup_frame, self.signin_frame, self.dashbord_frame):

            frame=F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F]=frame

            frame.grid(row=0, column=0, sticky=ctk.NSEW)

        self.show_frame(self.signin_frame)

        # def callback(self, url):
        #     webbrowser.open_new(url)

        # def check_update():
        #     time.sleep(4)
        #     z = FirebaseConfig()
        #     u = z.storage.child('version').get_url(None)
        #     b = requests.get(u).json()

        #     if b['version'] == self.current_version:
        #         pass
        #     else:
        #         ans = messagebox.askquestion("Alert!", "A new update is available, would you like to download it now?")
        #         if ans == 'yes':
        #             callback(self, 'https://github.com/fortysev-en/FirebaseTkinterApp')
        #         else:
        #             pass

        # threading.Thread(target=check_update, daemon=True).start()

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame=self.frames[cont]
        frame.tkraise()
        frame.update()
        frame.event_generate("<<ShowFrame>>")

# Driver Code
app=Application()
app.resizable(False, False)
app.mainloop()