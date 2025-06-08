import time
import json
import os

class Patient:
    def __init__(self, name, age, id):
        self.name = name
        self.age = age
        self.id = id
        self.health_data = []
        self.view_doctAI = 0

    def save_time(self):
        return time.strftime("%I:%M:%S %p | %d-%m-%Y %A", time.localtime())

    def store_data(self):
        while True:
            try:
                fasting = int(input("1. What is today's fasting sugar level? (mg/dL) => "))
                post_meal = int(input("2. What is your sugar level 2 hours after meal? (mg/dL) => "))
                medicine = input("3. Did you take your medicine today? (Yes/No) => ").strip()
                symptoms = input("""\n4. Are you feeling any of these? (Enter numbers separated by comma e.g. 1,2,5):
    1) Excessive thirst
    2) Frequent urination
    3) Tired or weak
    4) Blurred vision
    5) Tingling/numbness in feet
    => """).strip()
                break
            except ValueError as e:
                print(f"Invalid input: {e} | Please enter valid values.\n")

        entry = {
            "timestamp": self.save_time(),
            "fasting": fasting,
            "post_meal": post_meal,
            "medicine": medicine,
            "symptoms": symptoms
        }

        self.health_data.append(entry)
        #self.save_data_in_file()
        print("✅ Data saved successfully.")
        print("🩺 Stay consistent and stay healthy! See you next time.\n")

    def get_advice(self):
        print("\n---------------------------HEALTH ANALYZER----------------------------")

        if not self.health_data:
            print("⚠️ No data to analyze.")
            return

        latest = self.health_data[-1]
        fasting = latest["fasting"]
        post_meal = latest["post_meal"]
        medicine = latest["medicine"]
        symptoms = latest["symptoms"].split(",")

        score = 0
        print(f"\n--- Analysis for {latest['timestamp']} ---")

        # Fasting Sugar
        if fasting > 130 or fasting < 70:
            score += 1
            print("\n🔴 Fasting Sugar Alert – Fix your sleep, eat early, and walk more.")
        elif 70 < fasting < 99:
            print("\n🟢 Fasting Sugar Normal – Keep it up!")
        else:
            score += 0.3
            print("\n🟡 Fasting Sugar Borderline – Adjust sleep & dinner time.")

        # Post-meal Sugar
        if post_meal < 70:
            score += 0.5
            print("\n🟡 Low Post-Meal Sugar – Eat something sweet immediately.")
        elif 70 < post_meal < 140:
            print("\n🟢 Post-Meal Sugar Normal – You're doing great!")
        elif 140 < post_meal < 199:
            score += 0.5
            print("\n🟡 Elevated Post-Meal Sugar – Reduce lunch carbs, walk more.")
        else:
            score += 1
            print("\n🔴 High Post-Meal Sugar – Immediate action needed!")

        # Medicine Check
        if medicine.lower() == "yes":
            print("🟢 Medicine Taken")
        else:
            score += 0.5
            print("🔴 Medicine Not Taken – Don't skip it!")

        # Symptoms Check
        critical_symptoms = {"4", "5"}
        if len(symptoms) >= 2 or any(sym.strip() in critical_symptoms for sym in symptoms):
            score += 1
            print("🔴 Symptoms Alert – Multiple or critical symptoms detected!")

        # Health Status
        print("\n🩺 Health Status: ", end="")

        if score == 0:
            print("🟢 Stable")
            self.view_doctAI += 20
        elif score <= 2:
            print("🟡 Monitor")
            self.view_doctAI += 20
        else:
            print("🔴 Doctor Needed")
            self.view_doctAI += 20
        print("------------------------------------------------------------------\n")

    def get_health_trend(self):
        """
        Analyze health trends based on last 5 entries.
        Returns whether fasting and post-meal sugar levels are improving, worsening, or stable.
        """
        if len(self.health_data) < 2:
            return "⚠️ Not enough data to determine trends."
        
        fastings = [entry['fasting'] for entry in self.health_data[-5:]]
        post_meals = [entry['post_meal'] for entry in self.health_data[-5:]]
        
        def trend(data):
            if data[-1] < data[0]:
                return "📉 improving"
            elif data[-1] > data[0]:
                return "📈 worsening"
            else:
                return "➖ stable"
            
        fasting_trend = trend(fastings)
        post_meal_trend = trend(post_meals)
        
        print(f"\n📊 Trend Report (last 5 entries):")
        print(f"   🕗 Fasting Sugar Trend: {fasting_trend}")
        print(f"   🍛 Post-Meal Sugar Trend: {post_meal_trend}")

    def save_data_in_file(self, file_name="health_data.json"):
        patient_data = {
            "name": self.name,
            "id": self.id,
            "age": self.age,
            "health_analysis": self.health_data,
            "view_doctAI": self.view_doctAI
        }

        all_data = []

        # Load existing data
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                try:
                    all_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    print("⚠️ Warning: File corrupted or empty. Resetting file.")
                    all_data = []

        # Update existing patient entry or add new
        for i, entry in enumerate(all_data):
            if entry.get("id") == self.id:
                all_data[i] = patient_data
                break
        else:
            all_data.append(patient_data)

        # Write to file
        try:
            with open(file_name, "w") as f:
                json.dump(all_data, f, indent=4)
            print("💾 Data saved to file successfully.")
        except Exception as e:
            print(f"❌ Failed to save data: {e}")


    def load_data(self, file_name="health_data.json"):
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    print("⚠️ File is empty or corrupted.")
                    return

            for patient in all_data:
                if patient["id"] == self.id:
                    self.name = patient["name"]
                    self.age = patient["age"]
                    self.health_data = patient["health_analysis"]
                    self.view_doctAI = patient.get("view_doctAI", 0)
                    print(f"✅ Data loaded for patient {self.name} ::\n(ID: {self.id}) ::\nHealth Data : \n{self.health_data} !:")
                    return

            print("⚠️ No matching patient ID found.")
        else:
            print("🚫 No file found to load data from.")

    # Utility Methods for ID management
    @staticmethod
    def generate_id(name, age):
        """Generates a unique ID based on name and age."""
        return f"{name[:3].upper()}{age}{int(time.time()) % 10000}"

    @staticmethod
    def see_ids(file_name="health_data.json"):
        """Lists all patient IDs in the data file."""
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    print("⚠️ File is empty or corrupted.")
                    return []
            ids = [patient["id"] for patient in all_data]
            print(f"📋 Existing Patient IDs: {ids}")
            return ids
        else:
            print("🚫 No data file found.")
            return []

    def get_my_id(self):
        """Returns the patient's ID."""
        return self.id
