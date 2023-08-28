"""Sign in screen of the application."""

import os, sys
from PIL import Image
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

current_path = f'{os.path.dirname(__file__)}'

# Create sign in page
class Signin_Page(ctk.CTkFrame):
    """Sign in screen of the application."""

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.parent=parent
        self.controller=controller

        # create of frame left layout
        self.left_side = ctk.CTkFrame(self, width=30, height=20, corner_radius=20)
        self.left_side.grid(row=0, column=0)

        # Conver the image in CTkImage
        self.auth_img=ctk.CTkImage(Image.open(os.path.join(current_path.replace("frames", "wwwroot"), "login.jpg")), size=(500, 670))

        # Create a Label Widget to display the text or Image
        self.bg_img=ctk.CTkLabel(self.left_side, text="", image=self.auth_img)
        self.bg_img.grid(row=0, column=0)

        # label of frame right layout
        self.right_side = ctk.CTkFrame(self, width=500, height=500, fg_color="gray85", corner_radius=20)
        self.right_side.grid(row=0, column=1, padx=50, pady=20)

        self.tile=ctk.CTkLabel(self.right_side, text ="ยินดีต้อนรับ", font=ctk.CTkFont(family="Mitr", size=20, weight="normal"), width=500)
        self.tile.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=ctk.NSEW)

        self.email_lb=ctk.CTkLabel(self.right_side, text ="อีเมล:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.email_lb.grid(row=1, column=0, padx=30, pady=0, sticky=ctk.W)
        self.email_entry=ctk.CTkEntry(self.right_side, placeholder_text="sample@gmail.com", width=460)
        self.email_entry.grid(row=2, column=0, columnspan=2, padx=30, pady=(0, 5), sticky=ctk.W)

        self.password_lb=ctk.CTkLabel(self.right_side, text ="รหัสผ่าน:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.password_lb.grid(row=3, column=0, padx=30, pady=0, sticky=ctk.W)
        self.password_entry=ctk.CTkEntry(self.right_side, placeholder_text="abc1234", show="*", width=460)
        self.password_entry.grid(row=4, column=0, columnspan=2, padx=30, pady=(0, 5), sticky=ctk.W)

        self.devider=ctk.CTkFrame(self.right_side, width=400, height=2, fg_color="gray80")
        self.devider.grid(row=5, column=0, columnspan=2, padx=50, pady=(30, 20), sticky=ctk.NSEW)

        self.signup_btn=ctk.CTkButton(self.right_side, width=200, text="ยังไม่มีบัญชี?",
                                   fg_color="gray80", border_width=2, border_color="gray80", text_color=("gray20", "#DCE4EE"),
                                   command=lambda: controller.show_frame(controller.signup_frame))
        self.signup_btn.grid(row=6, column=0, padx=10, pady=(0, 20))
        self.signin_btn=ctk.CTkButton(self.right_side, width=200, text="เข้าสู่ระบบ",font=ctk.CTkFont(family="Mitr", size=14, weight="normal"),
                              command=lambda: self.signin_event())
        self.signin_btn.grid(row=6, column=1, padx=10, pady=(0, 20))
        # self.signin_btn.bind('<Return>', self.signin_event())
  
    def signin_event(self):
        self.user_len = len(list(self.controller.firebase_conf.get_user(self.email_entry.get())))

        if (self.email_entry.get() == '') or (self.password_entry.get() == ''):
            msg = CTkMessagebox(title="เกิดข้อผิดพลาด!", message="อีเมลหรือรหัสผ่านไม่สามารถว่างเปล่าได้ กรุณาลองใหม่อีกครั้ง!", 
                              icon="warning", option_1="ลองอีกครั้ง")
            
        if (self.user_len == 0 and self.email_entry.get() != '' and self.password_entry.get() != ''):
            msg = CTkMessagebox(title="เกิดข้อผิดพลาด!", message="อีเมลนี้ยังไม่ได้สมัครสมาชิก กรุณาลองอีเมลใหม่อีกครั้ง หรือสมัครสมาชิกใหม่!", 
                              icon="warning", option_1="ลองอีกครั้ง", option_2="สมัครสามชิก")
            
            if msg.get() == "สมัครสามชิก":
                # Set empty value all field
                self.email_entry.delete('0', 'end')
                self.password_entry.delete('0', 'end')
                # Switch frame
                self.controller.show_frame(self.controller.signup_frame)
        else:
            for user in self.controller.firebase_conf.get_user(self.email_entry.get()):
                try:
                    response = self.controller.firebase_conf.login_user(user, self.password_entry.get())
                    # if true.
                    if response:
                        self.controller.user_id = user.to_dict().get('user_id')
                        self.controller.user = user.to_dict()
                        # Redirect to dashboard page
                        self.signin_msg=CTkMessagebox(title="สำเร็จ", message="เข้าสู่ระบบสำเร็จ", 
                                                      icon="check")
                        if self.signin_msg.get()=="OK":
                            # Set empty value all field
                            self.email_entry.delete('0', 'end')
                            self.password_entry.delete('0', 'end')
                            self.controller.show_frame(self.controller.dashbord_frame)
                    else:
                        CTkMessagebox(title="เกิดข้อผิดพลาด!", message="รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง!",
                                      icon="warning", option_1="ลองอีกครั้ง")
                except Exception as error:
                    print(f"{type(error).__name__}: {error}")
                    CTkMessagebox(title="เกิดข้อผิดพลาด", message="เกิดข้อผิดพลาด!!!", option_1="ลองอีกครั้ง")      
