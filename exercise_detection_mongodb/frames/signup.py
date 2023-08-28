"""Sign up screen of the application."""

import os
from PIL import Image
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


current_path = f'{os.path.dirname(__file__)}'

# Create sign up page
class Signup_Page(ctk.CTkFrame):
    """Sign up screen of the application."""

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller=controller
        self.parent = parent
        
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

        self.tile=ctk.CTkLabel(self.right_side, text ="สมัครสมาชิก", font=ctk.CTkFont(family="Mitr", size=20, weight="normal"), width=500)
        self.tile.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=ctk.NSEW)

        # left
        self.name_lb=ctk.CTkLabel(self.right_side, text ="ชื่อนามสกุล:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.name_lb.grid(row=1, column=0, padx=30, pady=0, sticky=ctk.W)
        self.name_entry=ctk.CTkEntry(self.right_side, placeholder_text="สีสัน สดใส", width=200)
        self.name_entry.grid(row=2, column=0, padx=30, pady=(0, 5), sticky=ctk.W)

        self.phone_lb=ctk.CTkLabel(self.right_side, text ="เบอร์โทร:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.phone_lb.grid(row=3, column=0, padx=30, pady=0, sticky=ctk.W)
        self.phone_entry=ctk.CTkEntry(self.right_side, placeholder_text="0123456789", width=200)
        self.phone_entry.grid(row=4, column=0, padx=30, pady=(0, 5), sticky=ctk.W)

        self.email_lb=ctk.CTkLabel(self.right_side, text ="อีเมล:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.email_lb.grid(row=5, column=0, padx=30, pady=0, sticky=ctk.W)
        self.email_entry=ctk.CTkEntry(self.right_side, placeholder_text="sample@gmail.com", width=200)
        self.email_entry.grid(row=6, column=0, padx=30, pady=(0, 5), sticky=ctk.W)

        self.password_lb=ctk.CTkLabel(self.right_side, text ="รหัสผ่าน:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.password_lb.grid(row=7, column=0, padx=30, pady=0, sticky=ctk.W)
        self.password_entry=ctk.CTkEntry(self.right_side, placeholder_text="abc1234", show="*", width=200)
        self.password_entry.grid(row=8, column=0, padx=30, pady=(0, 5), sticky=ctk.W)
        
        self.devider=ctk.CTkFrame(self.right_side, width=400, height=2, fg_color="gray80")
        self.devider.grid(row=9, column=0, columnspan=2, padx=50, pady=(30, 20), sticky=ctk.NSEW)
        
        # right
        self.position_lb=ctk.CTkLabel(self.right_side, text ="ตำแหน่ง:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.position_lb.grid(row=1, column=1, padx=30, pady=0, sticky=ctk.W)
        self.position_entry=ctk.CTkEntry(self.right_side, placeholder_text="พนักงานทั่วไป", width=200)
        self.position_entry.grid(row=2, column=1, padx=30, pady=(0, 5), sticky=ctk.W)

        self.department_lb=ctk.CTkLabel(self.right_side, text ="แผนก:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.department_lb.grid(row=3, column=1, padx=30, pady=0, sticky=ctk.W)
        self.department_entry=ctk.CTkEntry(self.right_side, placeholder_text="ผู้ป่วยใน", width=200)
        self.department_entry.grid(row=4, column=1, padx=30, pady=(0, 5), sticky=ctk.W)

        self.hospital_lb=ctk.CTkLabel(self.right_side, text ="โรงพยาบาล:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.hospital_lb.grid(row=5, column=1, padx=30, pady=0, sticky=ctk.W)
        self.hospital_entry=ctk.CTkEntry(self.right_side, placeholder_text="โรงพยาบาลกัลยาณิวัฒนาการุณย์", width=200)
        self.hospital_entry.grid(row=6, column=1, padx=30, pady=(0, 5), sticky=ctk.W)

        self.confirm_pass_lb=ctk.CTkLabel(self.right_side, text ="ยืนยันรหัสผ่าน:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.confirm_pass_lb.grid(row=7, column=1, padx=30, pady=0, sticky=ctk.W)
        self.confirm_pass_entry=ctk.CTkEntry(self.right_side, placeholder_text="abc1234", show="*", width=200)
        self.confirm_pass_entry.grid(row=8, column=1, padx=30, pady=(0, 5), sticky=ctk.W)

        self.have_acc_btn=ctk.CTkButton(self.right_side, width=200, text="มีบัญชีแล้ว?",
                                        fg_color="gray80", border_width=2, border_color="gray80", text_color=("gray20", "#DCE4EE"),
                                        command=lambda: controller.show_frame(controller.signin_frame))
        self.have_acc_btn.grid(row=12, column=0, padx=10, pady=(0, 10))
        self.signin_btn=ctk.CTkButton(self.right_side, width=200, text="สมัคร", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"),
                                      command=lambda: self.signup_event())
        self.signin_btn.grid(row=12, column=1, padx=10, pady=(0, 10))
    
    # Create register event click
    def signup_event(self):

        self.user_len = len(list(self.controller.firebase_conf.get_user(self.email_entry.get())))

        if self.user_len > 0:
            msg = CTkMessagebox(title="เกิดข้อผิดพลาด!", message="อีเมลนี้ได้มีการสมัครสมาชิกแล้ว!",
                  icon="warning", option_1="ลองอีกครั้ง", option_2="เข้าสู่ระบบ")
            if msg.get() == "เข้าสู่ระบบ":
                self.controller.show_frame(self.controller.signin_frame)
        elif self.name_entry.get() == "":
            CTkMessagebox(title="เกิดข้อผิดพลาด!", message="ชื่อนามสกุลไม่สามารถว่างเปล่าได้!",
                            icon="warning", option_1="ลองอีกครั้ง")
        elif self.email_entry.get() == "":
            CTkMessagebox(title="เกิดข้อผิดพลาด!", message="อีเมลไม่สามารถว่างเปล่าได้!",
                            icon="warning", option_1="ลองอีกครั้ง")
        elif self.password_entry.get() == "":
            CTkMessagebox(title="เกิดข้อผิดพลาด!", message="รหัสผ่านไม่สามารถว่างเปล่าได้!",
                            icon="warning", option_1="ลองอีกครั้ง")
        elif self.password_entry.get() != self.confirm_pass_entry.get():
            CTkMessagebox(title="เกิดข้อผิดพลาด!", message="รหัสผ่านไม่ตรงกัน!",
                          icon="warning", option_1="ลองอีกครั้ง")
        else:
            try:
                # Sign in
                reponse = self.controller.firebase_conf.register(
                    self.name_entry.get(), self.phone_entry.get(), self.email_entry.get(), self.password_entry.get(),
                    self.position_entry.get(), self.department_entry.get(), self.hospital_entry.get()
                )

                if reponse:
                    # Redirect to login page
                    msg=CTkMessagebox(title="สำเร็จ", message="สมัครสมาชิกสำเร็จ",
                        icon="check")
                    
                    if msg.get()=="OK":
                        # Set empty value all field
                        self.name_entry.delete('0', 'end')
                        self.phone_entry.delete('0', 'end')
                        self.email_entry.delete('0', 'end')
                        self.password_entry.delete('0', 'end')
                        self.confirm_pass_entry.delete('0', 'end')
                        self.position_entry.delete('0', 'end')
                        self.department_entry.delete('0', 'end')
                        self.hospital_entry.delete('0', 'end')
                        # Switch frame
                        self.controller.show_frame(self.controller.signin_frame)
                
            except Exception as error:
                print(f"{type(error).__name__}: {error}")
                CTkMessagebox(title="เกิดข้อผิดพลาด!", message="เกิดข้อผิดพลาด!!!", option_1="ลองอีกครั้ง")
