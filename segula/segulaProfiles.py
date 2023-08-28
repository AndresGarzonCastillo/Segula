from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient
from segulaClinical import segulaClinical

class SegulaProfiles:
    db_name = 'SegulaPatients'

    def get_database(self):
        client = MongoClient('mongodb://localhost:27017/')
        return client[self.db_name]

    def __init__(self, profile, patient_data):
        self.profile = profile
        self.patient_data = patient_data
        self.create_main_window()
        self.create_clinical_history_window()

    def create_main_window(self):
        self.profile.geometry('800x600')
        self.profile.iconbitmap('segula.ico')
        self.profile.config(bg="#D1E338")
        self.profile.resizable(False, False)
        ancho_ventana = self.profile.winfo_reqwidth()
        alto_ventana = self.profile.winfo_reqheight()
        posicion_x = int((self.profile.winfo_screenwidth() / 3) - (ancho_ventana / 1))
        posicion_y = int((self.profile.winfo_screenheight() / 3) - (alto_ventana / 1))

        self.profile.geometry("+{}+{}".format(posicion_x, posicion_y))

        self.profile.title('Segula Nutrition')

        segula = Label(self.profile, text="Segula Nutrition", bg="#D1E338", font=("Cooper Black", 24))
        segula.grid(column=0, columnspan=4, row=0, padx=110, pady=10)

        segulaPrincipal = Label(self.profile, text="Patient Profile", bg="#D1E338", font=("Cooper Black", 15))
        segulaPrincipal.grid(column=0, columnspan=2, row=1, padx=110, pady=15)

        row = 2
        self.data_labels = {}
        label_names = {
            'documentType': 'Document Type',
            'documentNumber': 'Document Number',
            'nationality': 'Nationality',
            'patientName': 'Patient Name',
            'patientLastname': 'Patient Lastname',
            'birthDate': 'Birth Date',
            'patientAge': 'Patient Age',
            'genderPatient': 'Gender Patient',
            'sexPatient': 'Sex Patient',
            'addressPatient': 'Address Patient',
            'statePatient': 'State Patient',
            'cityPatient': 'City Patient',
            'cellphonePatient': 'Cellphone Patient',
            'contactPhone': 'Emergency Case',
        }

        for key, value in self.patient_data.items():
            if key != '_id':
                # Obtain the name of the label from the dictionary, if exists, otherwise use the original key value
                label_text = label_names.get(key, key)

                label = Label(self.profile, text=label_text, bg="#D1E338")
                label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
                data_label = Label(self.profile, text=value, bg="#D1E338")
                data_label.grid(row=row, column=1, padx=10, pady=5)
                self.data_labels[key] = data_label
                row += 1

        edit_button = Button(self.profile, text="Edit", command=self.edit_patient_data, bg="black", fg="white")
        edit_button.grid(row=row, column=0, pady=10)

        delete_button = Button(self.profile, text="Delete", command=self.delete_patient_data, bg="black", fg="white")
        delete_button.grid(row=row, column=1, pady=10)

    def create_clinical_history_window(self):
        segulaPrincipal = Label(self.profile, text="Clinical History", bg="#D1E338", font=("Cooper Black", 15))
        segulaPrincipal.grid(column=2, columnspan=2, row=1, padx=110)

        add_button = Button(self.profile, text="Assign Medical Appointment", bg="black", fg="white", command=self.assign_medical_cite)
        add_button.grid(column=3, row=12)

        self.tree_frame = ttk.Frame(self.profile)
        self.tree_frame.grid(column=2, row=1, columnspan=6, rowspan=15, padx=10, pady=10)

        self.patientClinicalHistory = ttk.Treeview(self.tree_frame, columns=('documentNumber', 'date', 'lifeCoach'))
        self.patientClinicalHistory.pack(side='left')

        scrollbar = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.patientClinicalHistory.yview)
        scrollbar.pack(side='right', fill='y')

        self.patientClinicalHistory.configure(yscroll=scrollbar.set)

        self.patientClinicalHistory.heading('documentNumber', text='ID')
        self.patientClinicalHistory.heading('date', text='Date Last Appointment')
        self.patientClinicalHistory.heading('lifeCoach', text='Life Coach')

        self.patientClinicalHistory.column('#0', width=0)
        self.patientClinicalHistory.column('documentNumber', width=100)
        self.patientClinicalHistory.column('date', width=100)
        self.patientClinicalHistory.column('lifeCoach', width=150)

        self.patientClinicalHistory.bind('<<TreeviewSelect>>', self.show_selected_history)

    def edit_patient_data(self):
        edit_window = Toplevel(self.profile)
        edit_window.title('Edit Patient')
        self.edit_window = edit_window

        patients = {
            'documentType': 'Document Type:',
            'documentNumber': 'Document Number:',
            'nationality': 'Nationality:',
            'patientName': 'Patient Name:',
            'patientLastname': 'Patient Lastname:',
            'birthDate': 'Birth Date:',
            'patientAge': 'Patient Age:',
            'genderPatient': 'Gender:',
            'sexPatient': 'Sex:',
            'addressPatient': 'Address:',
            'statePatient': 'State:',
            'cityPatient': 'City:',
            'cellphonePatient': 'Cellphone:',
            'contactPhone': 'Emergency Case:'
        }

        row = 0
        entry_fields = {}
        for field_name, label_text in patients.items():
            entry_label = Label(edit_window, text=label_text)
            entry_label.grid(row=row, column=0, padx=10, pady=5)
            entry_field = Entry(edit_window)
            entry_field.grid(row=row, column=1, padx=10, pady=5)

            if field_name in self.patient_data:
                entry_field.insert(0, self.patient_data[field_name])

            entry_fields[field_name] = entry_field
            row += 1

        save_button = Button(edit_window, text='Save', command=lambda: self.save_edited_data(entry_fields))
        save_button.grid(row=row, columnspan=2, pady=10)

        # Bring the edit window to the front
        self.profile.lift()

    def save_edited_data(self, entry_fields):
        db = self.get_database()
        collection = db['Patients']

        patient_id = self.patient_data['_id']
        updated_data = {}

        for field_name, entry_field in entry_fields.items():
            updated_data[field_name] = entry_field.get()

        collection.update_one({'_id': patient_id}, {'$set': updated_data})

        # Update the data in the user interface
        for key, value in updated_data.items():
            if key in self.data_labels:
                self.data_labels[key].config(text=value)

        messagebox.showinfo("Success", "Patient data updated!")
        self.edit_window.destroy()
        self.profile.lift()

    def delete_patient_data(self):
        result = messagebox.askyesno("Confirmation", "Are you sure you want to delete the patient data?")
        if result:
            db = self.get_database()
            collection = db['Patients']

            patient_id = self.patient_data['_id']
            collection.delete_one({'_id': patient_id})

            messagebox.showinfo("Success", "Patient data deleted!")
            self.profile.destroy()
        else:
            self.profile.lift()

    def search_clinical_history(self):
        # Get the search term from the Entry widget
        search_term = self.search_entry.get()

        # Perform the database query
        db = self.get_database()
        collection = db['clinicalHistory']
        query = {
            '$or': [
                {'documentNumber': {'$regex': search_term, '$options': 'i'}},
                {'date': {'$regex': search_term, '$options': 'i'}},
                {'lifeCoach': {'$regex': search_term, '$options': 'i'}}
            ]
        }
        cursor = collection.find(query)
        # Clear any existing data in the Treeview
        self.patientClinicalHistory.delete(*self.patientClinicalHistory.get_children())
        # Populate the Treeview with the search results
        for history in cursor:
            date = history.get('date', '')  # Use an empty string as default if 'date' key is not present
            self.patientClinicalHistory.insert('', 'end', text=date, values=(
                history.get('documentNumber', ''),
                date,
                history.get('lifeCoach', '')
            ))

    def load_clinical_history(self, patient_data):
        db = self.get_database()
        collection = db['clinicalHistory']
        query = {'documentNumber': patient_data['documentNumber']}

        # Sort the clinical histories by date in descending order
        cursor = collection.find(query).sort('date', -1)

        # Clear any existing data in the Treeview
        self.patientClinicalHistory.delete(*self.patientClinicalHistory.get_children())

        # Populate the Treeview with the clinical histories
        for history in cursor:
            date = history.get('date', '')  # Use an empty string as default if 'date' key is not present
            self.patientClinicalHistory.insert('', 'end', text=date, values=(
                history.get('documentNumber', ''),
                date,
                history.get('lifeCoach', ''),
                history.get('weight', ''),
                history.get('height', ''),
                history.get('remarks', ''),
                history.get('dosage', ''),
                history.get('treatment', '')
            ))
            
    def show_selected_history(self, event):
        selected_items = self.patientClinicalHistory.selection()
        if selected_items:
            selected_item = selected_items[0]
            date = self.patientClinicalHistory.item(selected_item, 'text')

            # Get clinical history data from the database
            db = self.get_database()
            collection = db['clinicalHistory']
            query = {'date': date}
            clinical_history_data = collection.find_one(query)
            
            patient_query = {'documentNumber': clinical_history_data.get('documentNumber')}
            patient_data = db['Patients'].find_one(patient_query)
            patient_full_name = f"{patient_data.get('patientName')}\n{patient_data.get('patientLastname')}"
            self.profile.lift()
            
            history = Tk()
            application4 = segulaClinical(history, clinical_history_data, patient_full_name)
            history.mainloop()
            
    def assign_medical_cite(self):
        assign_window = Toplevel(self.profile)
        assign_window.title("Assign Medical Appointment")
        assign_window.config(bg="#D1E338")

        # Create labels and entry fields to ask for the date, document number, and life coach
        date_label = Label(assign_window, text="Date of the Appointment:", bg="#D1E338")
        date_label.grid(row=0, column=0, padx=10, pady=5)
        date_entry = Entry(assign_window)
        date_entry.grid(row=0, column=1, padx=10, pady=5)

        doc_num_label = Label(assign_window, text="Document Number:", bg="#D1E338")
        doc_num_label.grid(row=1, column=0, padx=10, pady=5)
        doc_num_entry = Entry(assign_window)
        doc_num_entry.grid(row=1, column=1, padx=10, pady=5)

        life_coach_label = Label(assign_window, text="Life Coach:", bg="#D1E338")
        life_coach_label.grid(row=2, column=0, padx=10, pady=5)
        life_coach_entry = Entry(assign_window)
        life_coach_entry.grid(row=2, column=1, padx=10, pady=5)

        # Add a button to save the appointment data
        save_button = Button(assign_window, text="Save", 
                             command=lambda: self.save_medical_cite(date_entry.get(), doc_num_entry.get(), life_coach_entry.get(), 
                                    assign_window))
        save_button.grid(row=3, columnspan=2, pady=10)

        # Bring the new window to the front
        assign_window.lift()

    def save_medical_cite(self, date, doc_num, life_coach, assign_window):
        # Connect to the MongoDB client and get the collection
        client = MongoClient('mongodb://localhost:27017/')
        db = client['SegulaPatients']
        collection = db['clinicalHistory']

        # Create a dictionary with the appointment data
        appointment_data = {
            'documentNumber': doc_num,
            'date': date,
            'lifeCoach': life_coach,
            'weight': '',
            'height': '',
            'remarks': '',
            'dosage': '',
            'treatment': '',
        }

        # Insert the appointment data into the collection
        collection.insert_one(appointment_data)

        # After saving, update the clinical history in the interface
        self.load_clinical_history(self.patient_data)
        assign_window.destroy()

if __name__ == '__main__':
    profiles = Tk()
    application3 = SegulaProfiles(profiles, {})  # Pass an empty dictionary for patient_data
    profiles.mainloop()

