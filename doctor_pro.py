from patient_pro import Patient
from tabulate import tabulate
import json
import os
from datetime import datetime
import time


def get_valid_date(prompt="📅 Enter appointment date (DD-MM-YYYY): ", dates=None):
    if dates is None:
        dates = []
    while True:
        date_str = input(prompt)
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            if date_obj.date() < datetime.now().date():
                print("⚠️ Date must be today or in the future. Try again.")
                continue
            if any(existing_date.date() == date_obj.date() for existing_date in dates):
                print("⚠️ Sorry, another patient already booked that date!")
                continue
            dates.append(date_obj)
            return date_obj
        except ValueError:
            print("⚠️ Invalid date format. Use DD-MM-YYYY. Try again.")


class DoctorAI:
    def __init__(self):
        self.patients = []
        self.appointments = []
        self.dates = []

    """ def load_all_patients(self, file_name="health_data.json"):
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    print("⚠️ health_data.json is empty or corrupted.")
                    return

            for data in all_data:
                p = Patient(data["name"], data["age"], data["id"])
                p.health_data = data.get("health_analysis", [])
                p.view_doctAI = data.get("view_doctAI", 0)
                self.patients.append(p)
            print(f"✅ Loaded {len(self.patients)} patients from file.")
        else:
            print("⚠️ No saved patients yet.") """

    
    def generate_id(self, name, age):
        """Generates a unique ID based on name and age."""
        return f"{name[:3].upper()}{age}{int(time.time()) % 10000}"

    def add_patient(self, name, age):
        patient = Patient(name=name, age=age, id=self.generate_id(name, age))
        patient.store_data()
        self.patients.append(patient)
        print(f"From now your ID is {id}")
        print("✅ Patient added to DoctorAI successfully!")

    def remove_patient(self, id):
        for patient in self.patients:
            if patient.id == id:
                self.patients.remove(patient)
                print(f"🗑️ Patient with ID {id} removed successfully.")
                self.save_all()
                return
        print(f"⚠️ Patient with ID {id} not found.")

    def view_patients(self, patient_type):
        print("🔥 Top patients needing attention:")
        headers = ["NAME", "AGE", "ID", "HEALTH DATA"]
        rows = []
        for patient in self.patients:
            if (patient_type == "1" and patient.view_doctAI == 20) or \
               (patient_type == "2" and patient.view_doctAI == 10) or \
               (patient_type == "3" and patient.view_doctAI == 3) or \
               (patient_type == "4"):
                rows.append([patient.name, patient.age, patient.id, patient.health_data])
        if rows:
            print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        else:
            print("✅ All patients are stable.")

    def search_patient(self, id):
        for patient in self.patients:
            if patient.id == id:
                print(f"""
   ID : {patient.id}
   NAME : {patient.name}
   AGE : {patient.age} 
   HEALTH DATA : {patient.health_data}""")
                return
        print(f"⚠️ Patient with ID {id} not found.")

    def give_advice(self, id):
        for patient in self.patients:
            if patient.id == id:
                patient.get_advice()
                return
        print(f"⚠️ Patient with ID {id} not found.")

    def load_data_file(self, id):
        for patient in self.patients:
            if patient.id == id:
                patient.load_data()
                return
        print(f"⚠️ Patient with ID {id} not found.")

    def add_appointments(self, name, age, num, problem):
        date = get_valid_date(dates=self.dates)
        appointment = [name, age, num, date, problem]
        self.appointments.append(appointment)
        print(f"✅ Appointment for {name} is booked to the doctor's schedule at {date}.")

    def see_appointments(self):
        if self.appointments:
            for i, app in enumerate(sorted(self.appointments, key=lambda a: a[3])):
                date_str = app[3].strftime("%d-%m-%Y")
                print(f"{i + 1}. NAME: {app[0]} | AGE: {app[1]} | PH.NO: {app[2]} | DATE: {date_str} | PROBLEM: {app[4]}")
        else:
            print("No appointments scheduled.")

    def get_health_trend(self, id):
        for patient in self.patients:
            if patient.id == id:
                if len(patient.health_data) < 2:
                    print(f"⚠️ Patient {patient.name} does not have enough data to determine trends.")
                    return
                fastings = [entry['fasting'] for entry in patient.health_data[-5:]]
                post_meals = [entry['post_meal'] for entry in patient.health_data[-5:]]

                def trend(data):
                    if data[-1] < data[0]:
                        return "📉 improving"
                    elif data[-1] > data[0]:
                        return "📈 worsening"
                    else:
                        return "➖ stable"

                print(f"Health trend for {patient.name} =>")
                print(f"Fasting: {trend(fastings)} | Post-Meal: {trend(post_meals)}")
                return
        print(f"⚠️ Patient with ID {id} not found.")

    def get_my_id(self, name):
        for patient in self.patients:
            if patient.name.lower() == name.lower():
                print(f"🆔 Your ID is: {patient.id}")
                return
        print("⚠️ No patient found with that name.")

    def see_ids(self):
        print("🔍 All Registered Patient IDs:")
        for patient in self.patients:
            print(f"- {patient.name}: {patient.id}")

    def save_all(self, file_name="health_data.json"):
        all_data = []
        for patient in self.patients:
            all_data.append({
                "name": patient.name,
                "age": patient.age,
                "id": patient.id,
                "health_analysis": patient.health_data,
                "view_doctAI": patient.view_doctAI
            })
        with open(file_name, "w") as f:
            json.dump(all_data, f, indent=4)
        print("💾 All data saved successfully!")

    def get_diabetes_health_tips(self):
        return [
            "🥗 Eat balanced meals low in sugar and refined carbs.",
            "🏃‍♂️ Exercise regularly to maintain a healthy weight.",
            "🩺 Monitor blood sugar levels consistently.",
            "💧 Stay hydrated and avoid sugary drinks.",
            "😴 Get enough sleep and manage stress levels."
        ]
