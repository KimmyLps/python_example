"""Cloud Firestore Configuration."""
import os
from firebase_admin import credentials, firestore
import firebase_admin
import datetime, time, uuid
from cryptography.fernet import Fernet
from google.cloud.firestore_v1.base_query import FieldFilter

# Set default variable
current_path = f'{os.path.dirname(__file__)}'


# Set the database
cred = credentials.Certificate(f'{current_path.replace("config", "")}key\\fir-f2960-firebase-adminsdk-gmyqh-5febe75f1e.json')
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()

# Create configure firebase
class FirebaseConfig:
    def __init__(self):
        # MAKE SURE YOU ADD YOUR OWN API KEYS FROM YOUR FIREBASE PROJECT
        self.user_ref = db.collection("users")
        self.patient_ref = db.collection("patients")
        self.physical_ref = db.collection("physicals")

    # User and Authentication
    def register(self, full_name, phone, email, password, position, department, hospital):
        try:
            with open(f'{current_path.replace("config", "")}key\\refKey.txt') as f:
                refKey = ''.join(f.readlines())
                refKeybyt = bytes(refKey, 'utf-8')
            f.close()

            fernet = Fernet(refKeybyt)
            self.enc_password = fernet.encrypt(password.encode())

            self.user_id = str(uuid.uuid4())
            self.user_ref.document(self.user_id).set(
                User(self.user_id, full_name, phone, email, self.enc_password, position, department, hospital).to_dict()
            )
            return True
        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return False
    def login_user(self, user, password):
        try:
            with open(f'{current_path.replace("config", "")}key\\refKey.txt') as f:
                refKey = ''.join(f.readlines())
                refKeybyt = bytes(refKey, 'utf-8')
            f.close()

            fernet = Fernet(refKeybyt)
            self.password_hash = user.to_dict().get('password_hash')
            self.dec_password = fernet.decrypt(self.password_hash).decode()
            return (password == self.dec_password)
        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return False
    def reset_password(self, username):
        try:
            self.auth.send_password_reset_email(username)
            return
        except:
            return False    
    def get_user(self, email):
        try:
            users = self.user_ref.where(filter=FieldFilter("email", "==", email)).stream()
            return users
        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return None

    # Patient
    def add_patient(self, prefix, full_name, sex, date_of_bird, age, nationality, marital_status, career, address, weight, height, patient_level, symptom):
        # print(self.patient_ref)
        try:
            self.patient_id = str(uuid.uuid4())
            self.patient_ref.document(self.patient_id).set(
                Patient(self.patient_id, prefix, full_name, sex, date_of_bird, age, nationality, marital_status, career, address, weight, height, patient_level, symptom).to_dict()
            )
            return True
        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return False  
    def get_patient_by_id(self, id):
        try:
            patient = self.patient_ref.document(f'{id}')
            return patient
        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return None     
    def get_patients(self):
        try:
            patients = self.patient_ref.stream()
            return patients
        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return None
        
    # Physical
    def get_physicals(self):
        try:
            physicals = self.physical_ref.stream()
            return physicals
        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return None
    def get_physical_by_id(self, id):
        try:
            physical = self.physical_ref.document(f'{id}')
            return physical
        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return None
    def add_physical(self, patient_id, user_id, ordinal_number):
        try:
            self.physical_id = str(uuid.uuid4())
            self.physical_ref.document(self.physical_id).set(
                Physical(self.physical_id, patient_id, user_id, ordinal_number).to_dict()
            )
            return True
        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return False
        
    # def resend_verification_email(self):
    #     try:
    #         with open('session', 'r') as user_cred:
    #             cred = json.load(user_cred)
    #             self.auth.send_email_verification(cred['idToken'])
    #     except:
    #         return False

class User:
    def __init__(self, user_id, full_name, phone, email, password_hash, position, department, hospital):

        ts = time.time()
        date_time = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
        
        self.user_id=user_id
        self.full_name=full_name
        self.phone=phone
        self.email=email
        self.password_hash=password_hash
        self.position=position
        self.department=department
        self.hospital=hospital
        self.created_date=date_time
        self.login_date=date_time

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        user=User(
            source["user_id"], 
            source["full_name"], 
            source["phone"], 
            source["email"],
            source["password_hash"],
            source["position"],
            source["department"],
            source["hospital"],
            # source["created_date"],
            # source["login_date"]
            )
        
        return user
        # [END_EXCLUDE]
    
    def to_dict(self):
        # [START_EXCLUDE]
        dest={
            "user_id": self.user_id,
            "full_name": self.full_name,
            "phone": self.phone,
            "email": self.email,
            "password_hash": self.password_hash,
            "position": self.position,
            "department": self.department,
            "hospital": self.hospital,
            "created_date": self.created_date,
            "login_date": self.login_date
        }

        return dest
        # [END_EXCLUDE]

class Patient:
    def __init__(self, patient_id, prefix, full_name, sex, date_of_bird, age, nationality, marital_status, career, address, weight, height, patient_level, symptom):
        self.patient_id=patient_id
        self.prefix=prefix
        self.full_name=full_name
        self.sex=sex
        self.date_of_bird=str(date_of_bird)
        self.age=age
        self.nationality=nationality
        self.marital_status=marital_status
        self.career=career
        self.address=address
        self.weight=weight
        self.height=height
        self.patient_level=patient_level
        self.symptom=symptom

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        dest = Patient(
            source["patient_id"], 
            source["prefix"], 
            source["full_name"], 
            source["sex"], 
            source["date_of_bird"], 
            source["age"], 
            source["nationality"], 
            source["marital_status"], 
            source["career"], 
            source["address"], 
            source["weight"], 
            source["height"], 
            source["patient_level"], 
            source["symptom"], 
        )
        return dest
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest={
            "patient_id": self.patient_id,
            "prefix": self.prefix,
            "full_name": self.full_name,
            "sex": self.sex,
            "date_of_bird": self.date_of_bird,
            "age": self.age,
            "nationality": self.nationality,
            "marital_status": self.marital_status,
            "career": self.career,
            "address": self.address,
            "weight": self.weight,
            "height": self.height,
            "patient_level": self.patient_level,
            "symptom": self.symptom,
        }
        return dest
        # [END_EXCLUDE]

    # def  __repr__(self):
    #     return f"Patient(\
    #             patient_id={self.patient_id},\
    #             prefix={self.prefix},\
    #             full_name={self.full_name},\
    #             sex={self.sex},\
    #             date_of_bird={self.date_of_bird},\
    #             age={self.age},\
    #             nationality={self.nationality},\
    #             marital_status={self.marital_status},\
    #             career={self.career},\
    #             address={self.address},\
    #             weight={self.weight},\
    #             height={self.height},\
    #             patient_level={self.patient_level},\
    #             symptom={self.symptom}\
    #         )"
        
class Physical:
    def __init__(self, physical_id, patient_id, user_id, ordinal_number):

        ts = time.time()
        date_time = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')

        self.physical_id = physical_id
        self.patient_id = patient_id
        self.user_id = user_id
        self.ordinal_number = ordinal_number
        self.date = date_time

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        dest = Physical(
            source["physical_id"], 
            source["patient_id"], 
            source["user_id"], 
            source["ordinal_number"], 
            source["date"], 
        )
        return dest
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest={
            "physical_id": self.physical_id,
            "patient_id": self.patient_id,
            "user_id": self.user_id,
            "ordinal_number": self.ordinal_number,
            "date": self.date,
        }
        return dest
        # [END_EXCLUDE]
