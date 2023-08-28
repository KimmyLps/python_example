"""Dashbord screen of the application."""
import customtkinter as ctk
from CTkTable import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkcalendar import DateEntry
from CTkMessagebox import CTkMessagebox
import cv2, os
from PIL import Image, ImageTk
from mediapipe import solutions
# Set the database
# current_path = f'{os.path.dirname(__file__)}'
# root_path = current_path.replace("/pages", "")
# cred = credentials.Certificate(f'{root_path}/key/fir-f2960-firebase-adminsdk-gmyqh-5febe75f1e.json')
# firebase = fa.initialize_app(cred)
# db = firestore.client()

class Dashboard_Page(ctk.CTkFrame):
    """Dashbord screen of the application."""

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.parent=parent
        self.controller=controller
        self.add_patient = None
        self.layout_scroll_frame = None
        self.start_physical = None
        self.name_info_label = None

        # self.update = self.update()
        # self.update_idletasks = self.update_idletasks()

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1, minsize=830)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)



        self.side_menu_layout()
        self.dashbord_layout()

    def side_menu_layout(self):
        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text=f"ยินดีต้อนรับ", font=ctk.CTkFont(size=24, weight="bold"), width=200)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.name_info_label = ctk.CTkLabel(self.sidebar_frame, text=f"sample long name and lastname", font=ctk.CTkFont(size=15, weight="bold"))
        self.name_info_label.grid(row=1, column=0, padx=20, pady=(0, 10))
        # print(self.controller.user)
        # if self.controller.user:
        #     print(self.controller.user)
        #     self.logo_label.configure(text=f"ยินดีต้อนรับ,\n{self.controller.user.get('full_name')}")
        self.dashboard_btn = ctk.CTkButton(self.sidebar_frame, text="แดชบอร์ด", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"), 
                                           command=self.redirect_dashbord)
        self.dashboard_btn.grid(row=2, column=0, padx=20, pady=10)
        self.new_patient_btn = ctk.CTkButton(self.sidebar_frame, text="เพิ่มข้อมูลคนไข้", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"), 
                                             command=self.redirect_add_patient)
        self.new_patient_btn.grid(row=3, column=0, padx=20, pady=10)
        self.edit_patient_btn = ctk.CTkButton(self.sidebar_frame, text="แก้ไขข้อมูลคนไข้", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"), 
                                              command=self.redirect_edit_patient)
        self.edit_patient_btn.grid(row=4, column=0, padx=20, pady=10)
        self.delete_patient_btn = ctk.CTkButton(self.sidebar_frame, text="ลบข้อมูลคนไข้", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"), 
                                                command=self.redirect_delete_patient)
        self.delete_patient_btn.grid(row=5, column=0, padx=20, pady=10)
        self.start_physical_btn = ctk.CTkButton(self.sidebar_frame, text="เริ่มกายภาพ", height=50, fg_color="#21618C", font=ctk.CTkFont(family="Mitr", size=16, weight="normal"), 
                                                command=self.redirect_start_physical)
        self.start_physical_btn.grid(row=6, column=0, padx=20, pady=10)
        self.log_out_btn = ctk.CTkButton(self.sidebar_frame, text="ออกจากระบบ", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"),
                                                anchor="bottom", 
                                                command=self.log_out)
        self.log_out_btn.grid(row=8, column=0, padx=20, pady=20)

        # self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        # self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        # self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
        #                                                                command=self.redirect_edit_patient)
        # self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
    # create layout scroll
    def dashbord_layout(self):
        self.layout_scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=10, height=650, fg_color="transparent")
        self.layout_scroll_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.layout_scroll_frame.grid_columnconfigure(0, weight=1)

        # create detail patient history
        self.patient_detail_frame = patient_detail_frame(self.layout_scroll_frame, self.controller, "ประวัติคนไข้")
        self.patient_detail_frame.grid(row=0, column=1, padx=(0, 10), pady=(20, 0), sticky=ctk.NSEW)
        self.patient_detail_frame.grid_columnconfigure(0, weight=1)

        # create table detail patient history
        self.table_detail_frame = ctk.CTkScrollableFrame(self.layout_scroll_frame, label_text="ประวัติกายภาพ", 
                                                    width=380, height=250, corner_radius=10,
                                                    label_font=ctk.CTkFont(family="Mitr", size=20, weight="normal"))
        self.table_detail_frame.grid(row=0, column=2, padx=(0, 10), pady=(20, 0), sticky="nsew")
        self.table_detail_frame.grid_columnconfigure(0, weight=1)

        headers = ["ชื่อ", "วันที่/เวลา", "จำนวนครั้ง"]
        data = []
        for physical in self.controller.firebase_conf.get_physicals():
            if physical:
                patient = self.controller.firebase_conf.get_patient_by_id(physical.to_dict().get('patient_id'))
                if patient:
                    data.append([
                        patient.get().to_dict().get('full_name'),
                        physical.to_dict().get('date'),
                        physical.to_dict().get('ordinal_number')
                    ])

        data.insert(0, headers)

        self.table = CTkTable(self.table_detail_frame, row=len(data), column=3, values=data, header_color="gray60")
        self.table.grid()

        # create report chart
        self.report_chart_frame = report_chart_frame(self.layout_scroll_frame, "Report Chart")
        self.report_chart_frame.grid(row=1, column=1, columnspan=2, padx=(0, 10), pady=(20, 0), sticky=ctk.NSEW)
        self.report_chart_frame.grid_columnconfigure(0, weight=1)

        # set default values
        # self.appearance_mode_optionemenu.set("Dark")

        # Display dashbord layout

    def open_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def redirect_dashbord(self):
        if self.add_patient:
            self.add_patient.grid_forget()
            self.add_patient = None
        if self.start_physical:
            self.start_physical.cap.release()
            cv2.destroyAllWindows()
            self.start_physical.grid_forget()
            self.start_physical = None
        if self.layout_scroll_frame:
            pass
        else:
            self.dashbord_layout()

    def redirect_add_patient(self):
        if self.layout_scroll_frame:
            self.layout_scroll_frame.grid_forget()
            self.layout_scroll_frame = None
        if self.start_physical:
            self.start_physical.cap.release()
            cv2.destroyAllWindows()
            self.start_physical.grid_forget()
            self.start_physical = None
        if self.add_patient:
            pass
        else:
            self.add_patient = add_patient(self, self.controller, "เพิ่มข้อมูลคนไข้")
            self.add_patient.grid(row=0, column=1, columnspan=2, padx=(10, 10), pady=(20, 20), sticky=ctk.NSEW)

    def redirect_edit_patient(self):
        print("edit_patient click")

    def redirect_delete_patient(self):
        print("delete_patient click")

    def redirect_start_physical(self):
        if os.environ.get('PATIENT_INFO') == str(None):
            CTkMessagebox(title="เกิดข้อผิดพลาด!", message="กรุณาเลือกคนไข้ก่อนกดเริ่มกายภาพ ",
                          icon="warning")
        else:
            if os.environ.get('CAP_START') == str(True):
                CTkMessagebox(title="เกิดข้อผิดพลาด!", message="กรุณาหยุดกายภาพก่อนเริ่มใหม่อีกครั้ง!",
                              icon="warning")
            else:
                if self.add_patient:
                    self.add_patient.grid_forget()
                    self.add_patient = None
                if self.layout_scroll_frame:
                    self.layout_scroll_frame.grid_forget()
                    self.layout_scroll_frame = None
                self.start_physical = physical_frame(self, self.controller, "กายภาพ")
                self.start_physical.grid(row=0, column=1, columnspan=2, padx=(10, 10), pady=(20, 20), sticky=ctk.NSEW)

    def log_out(self):
        msg = CTkMessagebox(title="ยืนยัน!", message="ยืนยันออกจากระบบ!",
                            icon="warning", option_1="ยืนยัน", option_2="ยกเลิก")
        if msg.get() == "ยืนยัน":
            os.environ['PATIENT_INFO'] = str(None)
            os.environ['CAP_START'] = str(False)
            os.environ['USER_INFO'] = str(None)
            self.controller.show_frame(self.controller.signin_frame)

class patient_detail_frame(ctk.CTkFrame):
    def __init__(self, master, controller, title=ctk.StringVar):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.controller = controller
        self.opt_values = []
        self.opt_names = []
        self.patient_info = None
        os.environ['PATIENT_INFO'] = str(None)

        self.title_lb = ctk.CTkLabel(self, text=self.title, fg_color="gray78", corner_radius=10, 
                                            font=ctk.CTkFont(family="Mitr", size=20, weight="normal"))
        self.title_lb.grid(row=0, column=0, padx=10, pady=(10, 0), columnspan=2, sticky="ew")

        opt_values = []
        opt_names = []
        self.patients = self.controller.firebase_conf.get_patients()
        for patient in self.patients:
            opt_values.append(patient.to_dict())
            opt_names.append(patient.to_dict().get('full_name'))
            self.opt_values = opt_values
            self.opt_names = opt_names

        def select_name_collback(self, choice):
            # print("choice ", choice)
            # print("opt_values ", list(self.opt_values))
            filtered = filter(lambda val: val.get('full_name') == choice, self.opt_values)
            for i in range(1):
                filtered = list(filtered)
                self.controller.patient_id = filtered[i].get('patient_id')
                patient_info ={
                    "full_name": filtered[i]['full_name'],
                    "sex": filtered[i]['sex'],
                    "age": filtered[i]['age'],
                    "address": filtered[i]['address']
                    }
                self.patient_info = patient_info
                os.environ['PATIENT_INFO'] = str(patient_info)

            if self.patient_info:
                self.name_value.configure(text=f"{self.patient_info.get('full_name')}")
                self.sex_value.configure(text=f"{self.patient_info.get('sex')}")
                self.age_value.configure(text=f"{self.patient_info.get('age')}")
                self.address_value.configure(text=f"{self.patient_info.get('address')}")

        self.select_name = ctk.CTkOptionMenu(self, values=opt_names, command=lambda e: select_name_collback(self, e))
        self.select_name.grid(row=1, column=0, padx=(10, 0), pady=(20, 10))
        self.select_name.set("เลือกคนไข้")

        self.name_label = ctk.CTkLabel(self, text="ชื่อ", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"), width=50, anchor=ctk.W)
        self.name_label.grid(row=2, column=0, padx=15, pady=(10, 5), sticky=ctk.W)
        self.name_value = ctk.CTkLabel(self, text=".......", font=ctk.CTkFont(family="Mitr", size=12, weight="normal"), width=200, anchor=ctk.W)
        self.name_value.grid(row=2, column=1, padx=5, pady=(10, 5))
        # if self.patient_info:
        #     self.name_value.configure(text=f"{self.patient_info.full_name}")

        self.sex_label = ctk.CTkLabel(self, text="เพศ:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"), width=50, anchor=ctk.W)
        self.sex_label.grid(row=3, column=0, padx=15, pady=(10, 5), sticky=ctk.W)
        self.sex_value = ctk.CTkLabel(self, text=".......", font=ctk.CTkFont(family="Mitr", size=12, weight="normal"), width=200, anchor=ctk.W)
        self.sex_value.grid(row=3, column=1, padx=5, pady=(10, 5))

        self.age_label = ctk.CTkLabel(self, text="อายุ:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"), width=50, anchor=ctk.W)
        self.age_label.grid(row=4, column=0, padx=15, pady=(10, 5), sticky=ctk.W)
        self.age_value = ctk.CTkLabel(self, text=".......", font=ctk.CTkFont(family="Mitr", size=12, weight="normal"), width=200, anchor=ctk.W)
        self.age_value.grid(row=4, column=1, padx=5, pady=(10, 5))

        self.address_label = ctk.CTkLabel(self, text="ที่อยู่:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"), width=50, anchor=ctk.W)
        self.address_label.grid(row=5, column=0, padx=15, pady=(10, 5), sticky=ctk.W)
        self.address_value = ctk.CTkLabel(self, text="...................... \n .......", wraplength=200,
                                                 font=ctk.CTkFont(family="Mitr", size=12, weight="normal"), width=200, anchor=ctk.W)
        self.address_value.grid(row=5, column=1, padx=5, pady=(10, 5))

        self.other_label = ctk.CTkLabel(self, text="อื่นๆ:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"), width=50, anchor=ctk.W)
        self.other_label.grid(row=6, column=0, padx=15, pady=(10, 5), sticky=ctk.W)
        self.other_value = ctk.CTkLabel(self, text="...........", font=ctk.CTkFont(family="Mitr", size=12, weight="normal"), width=200, anchor=ctk.W)
        self.other_value.grid(row=6, column=1, padx=5, pady=(10, 5))

class report_chart_frame(ctk.CTkFrame):
    def __init__(self, master, title=ctk.StringVar):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title_lb = ctk.CTkLabel(self, text=self.title, fg_color="gray78", corner_radius=10, 
                                            font=ctk.CTkFont(family="Mitr", size=20, weight="normal"))
        self.title_lb.grid(row=0, column=0, padx=10, pady=(10, 10), columnspan=2, sticky="ew")

        # fig = Figure(figsize = (1, 1),
        #          dpi = 100, layout="compressed")
        stockListExp = ['AMZN' , 'AAPL', 'JETS', 'CCL', 'NCLH']
        stockSplitExp = np.array([35, 25, 25, 15, 20])

        fig = Figure(figsize = (6.5, 5.5), dpi = 100) # create a figure object
        ax = fig.add_subplot(111) # add an Axes to the figure

        ax.pie(stockSplitExp, radius=1, labels=stockListExp,autopct='%0.2f%%')
        ax.legend(title = "Four Fruits:")

        chart1 = FigureCanvasTkAgg(fig, self)
        chart1.get_tk_widget().grid()

class add_patient(ctk.CTkFrame):
    def __init__(self, master, controller, title=ctk.StringVar):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.master = master
        self.controller = controller

        self.title_lb = ctk.CTkLabel(self, text=self.title, fg_color="gray78", corner_radius=10, 
                                            font=ctk.CTkFont(family="Mitr", size=20, weight="normal"))
        self.title_lb.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        # left
        self.prefix_lb=ctk.CTkLabel(self, text ="คำนำหน้า:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.prefix_lb.grid(row=1, column=0, padx=30, pady=0, sticky=ctk.W)
        self.prefix_entry=ctk.CTkEntry(self, placeholder_text="คำนำหน้า", width=350)
        self.prefix_entry.grid(row=2, column=0, padx=30, pady=(0, 5), sticky=ctk.W)

        self.name_lb=ctk.CTkLabel(self, text ="ชื่อนามสกุล:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.name_lb.grid(row=3, column=0, padx=30, pady=0, sticky=ctk.W)
        self.name_entry=ctk.CTkEntry(self, placeholder_text="ชื่อนามสกุล", width=350)
        self.name_entry.grid(row=4, column=0, padx=30, pady=(0, 5), sticky=ctk.W)

        self.sex_lb=ctk.CTkLabel(self, text="เพศ:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.sex_lb.grid(row=5, column=0, padx=30, pady=0, sticky=ctk.W)
        self.sex_entry=ctk.CTkEntry(self, placeholder_text="เพศ", width=350)
        self.sex_entry.grid(row=6, column=0, padx=30, pady=(0, 5), sticky=ctk.W)

        self.date_of_bird_lb=ctk.CTkLabel(self, text="วันเกิด:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.date_of_bird_lb.grid(row=7, column=0, padx=30, pady=0, sticky=ctk.W)
        def date_entry_selected(event):
            w = event.widget
            date = w.get_date()
            self.date_of_bird_entry.set_date(date)
        self.date_of_bird_entry=DateEntry(self, width=20, selectmode='day', foreground= "white")
        self.date_of_bird_entry.grid(row=8, column=0, padx=30, pady=(0, 5), sticky=ctk.W)
        self.date_of_bird_entry.bind("<<DateEntrySelected>>", date_entry_selected)

        self.age_lb=ctk.CTkLabel(self, text ="อายุ:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.age_lb.grid(row=9, column=0, padx=30, pady=0, sticky=ctk.W)
        self.age_entry=ctk.CTkEntry(self, placeholder_text="อายุ", width=350)
        self.age_entry.grid(row=10, column=0, padx=30, pady=(0, 5), sticky=ctk.W)

        self.nationality_lb=ctk.CTkLabel(self, text ="สัญชาติ:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.nationality_lb.grid(row=11, column=0, padx=30, pady=0, sticky=ctk.W)
        self.nationality_entry=ctk.CTkEntry(self, placeholder_text="สัญชาติ", width=350)
        self.nationality_entry.grid(row=12, column=0, padx=30, pady=(0, 5), sticky=ctk.W)

        self.address_lb=ctk.CTkLabel(self, text ="ที่อยู่:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.address_lb.grid(row=13, column=0, padx=30, pady=0, sticky=ctk.W)
        self.address_entry=ctk.CTkEntry(self, placeholder_text="ที่อยู่", width=770)
        self.address_entry.grid(row=14, column=0, columnspan=2, padx=30, pady=(0, 5), sticky=ctk.W)

        # right
        self.marital_status_lb=ctk.CTkLabel(self, text ="สถานภาพสมรส:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.marital_status_lb.grid(row=1, column=1, padx=30, pady=0, sticky=ctk.W)
        self.marital_status_entry=ctk.CTkEntry(self, placeholder_text="สถานภาพสมรส", width=350)
        self.marital_status_entry.grid(row=2, column=1, padx=30, pady=(0, 5), sticky=ctk.W)
        
        self.career_lb=ctk.CTkLabel(self, text ="อาชีพ:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.career_lb.grid(row=3, column=1, padx=30, pady=0, sticky=ctk.W)
        self.career_entry=ctk.CTkEntry(self, placeholder_text="อาชีพ", width=350)
        self.career_entry.grid(row=4, column=1, padx=30, pady=(0, 5), sticky=ctk.W)

        self.weight_lb=ctk.CTkLabel(self, text ="น้ำหนัก:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.weight_lb.grid(row=5, column=1, padx=30, pady=0, sticky=ctk.W)
        self.weight_entry=ctk.CTkEntry(self, placeholder_text="น้ำหนัก", width=350)
        self.weight_entry.grid(row=6, column=1, padx=30, pady=(0, 5), sticky=ctk.W)

        self.height_lb=ctk.CTkLabel(self, text ="ส่วนสูง:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.height_lb.grid(row=7, column=1, padx=30, pady=0, sticky=ctk.W)
        self.height_entry=ctk.CTkEntry(self, placeholder_text="ส่วนสูง", width=350)
        self.height_entry.grid(row=8, column=1, padx=30, pady=(0, 5), sticky=ctk.W)

        self.patient_level_lb=ctk.CTkLabel(self, text ="ระดับคนไข้:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.patient_level_lb.grid(row=9, column=1, padx=30, pady=0, sticky=ctk.W)
        self.patient_level_entry=ctk.CTkEntry(self, placeholder_text="ระดับคนไข้", width=350)
        self.patient_level_entry.grid(row=10, column=1, padx=30, pady=(0, 5), sticky=ctk.W)

        self.symptom_lb=ctk.CTkLabel(self, text ="อาการป่วย:", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"))
        self.symptom_lb.grid(row=11, column=1, padx=30, pady=0, sticky=ctk.W)
        self.symptom_entry=ctk.CTkEntry(self, placeholder_text="อาการป่วย", width=350)
        self.symptom_entry.grid(row=12, column=1, padx=30, pady=(0, 5), sticky=ctk.W)

        # action buttons
        self.add_patient_btn=ctk.CTkButton(self, width=350, text="เพิ่ม", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"),
                                           command=lambda: self.add_patient_event())
        self.add_patient_btn.grid(row=15, column=1, padx=10, pady=10)

    def add_patient_event(self):
        msg = CTkMessagebox(title="ยืนยัน!", message="ยืนยันการเพิ่มข้อมูลคนไข้!",
                                      icon="warning", option_1="ยืนยัน", option_2="ยกเลิก")
        if msg.get() == "ยืนยัน":
            response = self.controller.firebase_conf.add_patient(
                self.prefix_entry.get(), self.name_entry.get(), self.sex_entry.get(), self.date_of_bird_entry.get_date(), int(self.age_entry.get()), 
                self.nationality_entry.get(), self.marital_status_entry.get(), self.career_entry.get(), self.address_entry.get(), 
                int(self.weight_entry.get()), int(self.height_entry.get()), self.patient_level_entry.get(), self.symptom_entry.get()
            )

            if response:
                add_patient_msg = CTkMessagebox(title="สำเร็จ", message="เพิ่มข้อมูลคนไข้สำเร็จ", 
                                              icon="check", option_1="OK")
                if add_patient_msg.get() == "Ok":
                    # Set empty value all field

                    # Switch to dashbord layout frame
                    self.master.add_patient.grid_forget()
                    self.master.dashbord_layout()

class physical_frame(ctk.CTkFrame):
    def __init__(self, master, controller, title=ctk.StringVar):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.title = title
        self.video_source = 0
        self.mp_drawing, self.mp_pose = solutions.drawing_utils, solutions.pose
        self.counter, self.stage = 0, None
        self.cap_width, self.cap_height = 800, 550
        self.dim = (self.cap_width, self.cap_height)
        self.frame_rate = 60
        self.update_interval = int(1000 / self.frame_rate)  # Convert frame rate to update interval

        self.title_lb = ctk.CTkLabel(self, text=self.title, fg_color="gray78", corner_radius=10, 
                                            font=ctk.CTkFont(family="Mitr", size=20, weight="normal"))
        self.title_lb.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="ew")

        self.vdo_canvas = ctk.CTkCanvas(self, width=self.cap_width, height=self.cap_height)
        self.vdo_canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.cap = cv2.VideoCapture(self.video_source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_height)

        self.stop_cap_btn = ctk.CTkButton(self, width=200, text="หยุดกายภาพ", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"),
                                        command=lambda: self.stop_cap())
        self.stop_cap_btn.grid(row=2, column=1, padx=10, pady=10)

        def start_cap_again(self):
            print("Start cap again")
            if os.environ.get('CAP_START') is str(False):
                self.cap_update()
            else:
                CTkMessagebox(title="เกิดข้อผิดพลาด!", message="กรุณาหยุดกายภาพก่อนเริ่มใหม่อีกครั้ง!",
                              icon="warning")
        self.start_cap_btn = ctk.CTkButton(self, width=200, text="เริ่มกายภาพอีกครั้ง", font=ctk.CTkFont(family="Mitr", size=14, weight="normal"),
                                        command=lambda: start_cap_again(self))
        self.start_cap_btn.grid(row=2, column=0, padx=10, pady=10)

        self.cap_update()
        

        # self.stop_cap_btn.bind('<Return>', self.stop_cap())

    def cap_update(self):
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.1) as pose:
            # while self.cap.isOpened():
            success, frame = self.cap.read()
            if success:
                os.environ['CAP_START'] = str(True)

                resized_frame = cv2.resize(frame, self.dim, interpolation = cv2.INTER_AREA)
                # Recolor image to RGB
                image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

                # Make detection
                results = pose.process(image)

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark
                    # Get coordinates
                    # LEFT
                    left_shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    left_wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    # RIGHT
                    right_shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    right_elbow = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    right_wrist = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                    # Calculate angle
                    left_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
                    right_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)

                    # Visualize angle
                    # LEFT
                    cv2.putText(image, str(left_angle),
                                tuple(np.multiply(left_elbow, [self.cap_width, self.cap_height]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                    # RIGHT
                    cv2.putText(image, str(right_angle),
                                tuple(np.multiply(right_elbow, [self.cap_width, self.cap_height]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

                    # Curl counter logic
                    if left_angle > 160:
                        self.stage = "down"
                    if left_angle < 30 and self.stage == 'down':
                        self.stage = "up"
                        self.counter += 1
                        # print("counter is: ", self.counter)
                except:
                    pass
                
                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0, 0), (225, 73), (93, 173, 226), -1)

                # Rep data
                cv2.putText(image, 'REPS', (15, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(self.counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Stage data
                cv2.putText(image, 'STAGE', (100, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, self.stage, (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Render detections
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                        self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                        self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                        )

                self.photo = ImageTk.PhotoImage(image=Image.fromarray(image))
                self.vdo_canvas.create_image(0, 0, image=self.photo, anchor=ctk.NW)
                self.master.after(self.update_interval, self.cap_update)
            else:
                self.cap.release()

    def calculate_angle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle
    
    def stop_cap(self):
        msg = CTkMessagebox(title="ยืนยัน!", message="ยืนยันการหยุดกายภาพให้คุณ ",
                            icon="warning", option_1="ยืนยัน", option_2="ยกเลิก")
        if msg.get() == "ยืนยัน":
            response = self.controller.firebase_conf.add_physical(
                self.controller.patient_id, self.controller.user_id, self.counter
            )
            if response:
                self.cap.release()
                os.environ['CAP_START'] = str(False)
                CTkMessagebox(title="สำเร็จ", message="บันทึกข้อมูลกายภาพสำเร็จ",
                              icon="check", option_1="OK")
        