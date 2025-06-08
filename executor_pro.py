from doctor_pro import DoctorAI
doctor = DoctorAI()

def get_appointment():
    print("\n🩺 BOOK AN APPOINTMENT")
    name = input("👤 Name: ")
    age = input("🎂 Age: ")
    number = input("📞 Phone Number: ")
    problem = input("🩻 Describe your health concern: ")
    doctor.add_appointments(name, age, number, problem)

def add_new_patient():
    print("\n🏥 JOIN THE HEALTH SYSTEM")
    name = input("👤 Your Full Name: ")
    age = input("🎂 Your Age: ")
    doctor.add_patient(name, age)

def main():
    print("═══════════════════════════════════════════════════")
    print("🔷 HEALTH-CARE MANAGEMENT SYSTEM with DoctorAI")
    print("═══════════════════════════════════════════════════\n")

    while True:
        try:
            print("🏥 Who are you?")
            print("  [1] 👨‍⚕️ I'm a Patient")
            print("  [2] 🧑‍⚕️ I'm a Doctor")
            role = int(input("Choose your role (1 or 2): "))
            if role in [1, 2]:
                break
            else:
                print("⚠️ Please enter 1 or 2.\n")
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.\n")
    
    # ───────────────────── PATIENT DASHBOARD ─────────────────────
    if role == 1:
        print("\n💙 Welcome to DoctorAI, Your Personal Health Partner!")
        while True:
            print("\n💡 Available Actions:")
            print("  [1] 🏥 Join the hospital system")
            print("  [2] 📅 Book an appointment")
            print("  [3] 🧠 Get health tips & guides")
            print("  [4] 🔎 Analyze my health & get schedule")
            print("  [5] 🆔 Get my Patient ID")
            print("  [6] ❌ Exit")

            choice = input("\n👉 Choose an option: ")
            if choice == "1":
                add_new_patient()
            elif choice == "2":
                get_appointment()
            elif choice == "3":
                print("\n🚀 Pro Tips to Tackle Diabetes Like a Pro:")
                for tip in doctor.get_diabetes_health_tips():
                    print(f"✅ {tip}")
            elif choice == "4":
                pid = input("🆔 Enter your Patient ID: ")
                doctor.give_advice(id=pid)
            elif choice == "5":
                name = input("👤 Enter your name to find your ID: ")
                doctor.get_my_id(name)
            elif choice == "6":
                print("\n🙏 Thank you for using DoctorAI! Stay healthy and sharp. 💪")
                break
            else:
                print("⚠️ Invalid choice. Try again!")

    # ───────────────────── DOCTOR DASHBOARD ─────────────────────
    elif role == 2:
        print("\n🧑‍⚕️ Welcome Doctor, launching DoctorAI dashboard...")
        while True:
            print("\n🩺 Doctor Command Center:")
            print("  [1] ➕ Add Patient")
            print("  [2] 🗑️ Remove Patient")
            print("  [3] 📅 View Appointments")
            print("  [4] 🧭 View Patients by Priority")
            print("  [5] 🔍 Search for a Patient")
            print("  [6] 📈 Health Trend Analysis")
            print("  [7] 💾 Save All Records")
            print("  [8] ❌ Exit")

            choice = input("\n👉 Choose an option: ")

            if choice == "1":
                name = input("👤 Patient Name: ")
                age = input("🎂 Patient Age: ")
                doctor.add_patient(name, age)

            elif choice == "2":
                print("\n🆔 Existing Patient IDs:")
                doctor.see_ids()
                id = input("Enter the Patient ID to remove: ")
                doctor.remove_patient(id=id)

            elif choice == "3":
                doctor.see_appointments()

            elif choice == "4":
                print("\n🔍 Filter by Priority:")
                print("  [1] Critical")
                print("  [2] Monitoring Needed")
                print("  [3] Normal")
                print("  [4] View All")
                patient_type = input("Choose a priority type (1-4): ")
                doctor.view_patients(patient_type=patient_type)

            elif choice == "5":
                print("\n🆔 Existing Patient IDs:")
                doctor.see_ids()
                pid = input("Enter the Patient ID to search: ")
                doctor.search_patient(id=pid)

            elif choice == "6":
                print("\n🆔 Existing Patient IDs:")
                doctor.see_ids()
                pid = input("Enter the Patient ID: ")
                doctor.get_health_trend(id=pid)

            elif choice == "7":
                doctor.save_all()
                print("💾 All patient records saved successfully!")

            elif choice == "8":
                print("\n👋 Session ended. Have a healing day, Doctor!")
                break

            else:
                print("⚠️ Invalid choice. Try again!")

# Boot it up!
if __name__ == "__main__":
    main()
