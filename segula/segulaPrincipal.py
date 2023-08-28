from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient
from PIL import Image, ImageTk
from segulaProfiles import SegulaProfiles

class SegulaPrincipal:
    db_name = 'SegulaPatients'

    def __init__(self, principal):
        self.principal = principal
        self.principal.title('Segula Nutrition')
        self.principal.geometry('800x400')
        self.principal.iconbitmap('segula.ico')
        self.principal.resizable(False, False)
        ancho_ventana = self.principal.winfo_reqwidth()
        alto_ventana = self.principal.winfo_reqheight()
        posicion_x = int((self.principal.winfo_screenwidth()/3) - (ancho_ventana / 2))
        posicion_y = int((self.principal.winfo_screenheight()/3) - (alto_ventana / 2))
        
        self.principal.geometry("+{}+{}".format(posicion_x, posicion_y))

        image = Image.open("segulaFruit.png")
        image = image.resize((800, 400))
        
        # Convertir la imagen a un objeto PhotoImage
        photo = ImageTk.PhotoImage(image)
        
        # widget Label para mostrar la imagen de fondo
        background_label = Label(self.principal, image=photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        background_label.image = photo
        
        segula = Label(self.principal, text="Segula Nutrition", font=("Cooper Black", 24), bg="black", fg="white")
        segula.grid(column=1, columnspan=3, row=0, padx=110, pady=20)

        segulaPrincipal = Label(self.principal, text=f"Welcome Life Coach German Martinez", font=("Cooper Black", 15), bg="black", fg="white")
        segulaPrincipal.grid(column=1, columnspan=3, row=1, padx=110)

        segulaInsertPatient = Button(self.principal, text="INSERT PATIENT", command=self.open_patient_form, bg="black", fg="white")
        segulaInsertPatient.grid(column=0, row=2, padx=15 ,pady=5)
        search_label = Label(self.principal, text="Search Patient:", bg="black", fg="white")
        search_label.grid(column=1, row=2)
        self.search_entry = Entry(self.principal)
        self.search_entry.grid(column=3, row=2)
        search_button = Button(self.principal, text="Search", command=self.search_patient, bg="black", fg="white")
        search_button.grid(column=4, row=2)

        self.tree_frame = ttk.Frame(self.principal)
        self.tree_frame.grid(column=1, row=5, columnspan=3, padx=10, pady=10)

        self.patient_list = ttk.Treeview(self.tree_frame, columns=('documentNumber', 'patientName', 'patientLastname', 'cellphonePatient'))
        self.patient_list.pack(side='left')

        scrollbar = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.patient_list.yview)
        scrollbar.pack(side='right', fill='y')

        self.patient_list.configure(yscroll=scrollbar.set)

        self.patient_list.heading('documentNumber', text='Document Number')
        self.patient_list.heading('patientName', text='Patient Name')
        self.patient_list.heading('patientLastname', text='Patient Lastname')
        self.patient_list.heading('cellphonePatient', text='Cellphone')

        self.patient_list.column('#0', width=0)
        self.patient_list.column('documentNumber', width=100)
        self.patient_list.column('patientName', width=150)
        self.patient_list.column('patientLastname', width=150)
        self.patient_list.column('cellphonePatient', width=100)

        self.patient_list.bind('<<TreeviewSelect>>', self.show_patient_details)

    def get_database(self):
        client = MongoClient('mongodb://localhost:27017/')
        return client[self.db_name]

    def open_patient_form(self):
        self.form_window = Toplevel(self.principal)
        self.form_window.title('Insert Patient')

        fields = [
            ('Document Type:', 'docTypeEntry'),
            ('Document Number:', 'docNumberEntry'),
            ('Nationality:', 'nationalityEntry'),
            ('Patient Name:', 'patientNameEntry'),
            ('Patient Last Name:', 'lastNameEntry'),
            ('Birth Date:', 'birthDateEntry'),
            ('Patient Age:', 'patientAgeEntry'),
            ('Gender Patient:', 'genderPatientEntry'),
            ('Sex Patient:', 'sexPatientEntry'),
            ('Address Patient:', 'addressPatientEntry'),
            ('State or Province:', 'statePatientEntry'),
            ('City of Residence:', 'cityEntry'),
            ('Cellphone:', 'cellphoneEntry'),
            ('Phone number in an emergency case:', 'contactPhoneEntry')
        ]

        row = 0
        for label, field_name in fields:
            entry_label = Label(self.form_window, text=label)
            entry_label.grid(row=row, column=0, padx=10, pady=5)
            entry_field = Entry(self.form_window)
            entry_field.grid(row=row, column=1, padx=10, pady=5)
            setattr(self, field_name, entry_field)
            row += 1

        save_button = Button(self.form_window, text='Save', command=self.save_patient_data)
        save_button.grid(row=row, columnspan=2, pady=10)

    def save_patient_data(self):
        db = self.get_database()
        collection = db['Patients']
        patients = {
            'documentType': self.docTypeEntry.get(),
            'documentNumber': self.docNumberEntry.get(),
            'nationality': self.nationalityEntry.get(),
            'patientName': self.patientNameEntry.get(),
            'patientLastname': self.lastNameEntry.get(),
            'birthDate': self.birthDateEntry.get(),
            'patientAge': self.patientAgeEntry.get(),
            'genderPatient': self.genderPatientEntry.get(),
            'sexPatient': self.sexPatientEntry.get(),
            'addressPatient': self.addressPatientEntry.get(),
            'statePatient': self.statePatientEntry.get(),
            'cityPatient': self.cityEntry.get(),
            'cellphonePatient': self.cellphoneEntry.get(),
            'contactPhone': self.contactPhoneEntry.get(),
        }
        collection.insert_one(patients)
        messagebox.showinfo("Success", "Patient data saved!")
        response = messagebox.askyesno("Confirmation", "Do you want to add a new patient?")
        if response:
            self.clear_entries()
            self.form_window.lift(self.principal)  # Coloca la ventana del formulario por encima de la principal
        else:
            self.form_window.destroy()

    def clear_entries(self):
        fields = [
            'docTypeEntry',
            'docNumberEntry',
            'nationalityEntry',
            'patientNameEntry',
            'lastNameEntry',
            'birthDateEntry',
            'patientAgeEntry',
            'genderPatientEntry',
            'sexPatientEntry',
            'addressPatientEntry',
            'statePatientEntry',
            'cityEntry',
            'cellphoneEntry',
            'contactPhoneEntry'
        ]
        for field_name in fields:
            entry_field = getattr(self, field_name, None)
            if entry_field:
                entry_field.delete(0, 'end')

    def search_patient(self):
        search_text = self.search_entry.get()
        db = self.get_database()
        collection = db['Patients']
        query = {
            '$or': [
                {'patientName': {'$regex': search_text, '$options': 'i'}},
                {'patientLastname': {'$regex': search_text, '$options': 'i'}},
                {'documentNumber': {'$regex': search_text, '$options': 'i'}}
            ]
        }

        self.patient_list.delete(*self.patient_list.get_children())
        results = collection.find(query)
        for result in results:
            self.patient_list.insert('', 'end', values=(
                result['documentNumber'],
                result['patientName'],
                result['patientLastname'],
                result['cellphonePatient']
            ))

    def show_patient_details(self, event):
        selected_items = self.patient_list.selection()
        if selected_items:
            selected_item = selected_items[0]
            values = self.patient_list.item(selected_item, 'values')
            document_number = values[0]

            db = self.get_database()
            collection = db['Patients']
            query = {'documentNumber': document_number}
            patient_data = collection.find_one(query)

            profiles = Tk()
            application3 = SegulaProfiles(profiles, patient_data)
            # Load the clinical history for the selected patient
            application3.load_clinical_history(patient_data)
            profiles.mainloop()
            
if __name__ == '__main__':
    principal = Tk()
    application2 = SegulaPrincipal(principal)
    principal.mainloop()

