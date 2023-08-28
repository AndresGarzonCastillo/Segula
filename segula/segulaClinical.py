from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

class segulaClinical:
    db_name = 'SegulaPatients'

    def get_database(self):
        client = MongoClient('mongodb://localhost:27017/')
        return client[self.db_name]
    
    def __init__(self, history, clinical_history_data, patient_full_name):
        self.history = history
        self.clinical_history_data = clinical_history_data
        self.patient_full_name = patient_full_name
        self.create_clinical_history_window()
        
    def create_clinical_history_window(self):
        self.history.geometry('450x700')
        self.history.iconbitmap('segula.ico')
        self.history.config(bg="#D1E338")
        self.history.resizable(False, False)
        ancho_ventana = self.history.winfo_reqwidth()
        alto_ventana = self.history.winfo_reqheight()
        posicion_x = int((self.history.winfo_screenwidth() / 3) - (ancho_ventana / 1))
        posicion_y = int((self.history.winfo_screenheight() / 3) - (alto_ventana / 1))

        self.history.geometry("+{}+{}".format(posicion_x, posicion_y))

        self.history.title('Segula Nutrition')

        segula = Label(self.history, text=self.patient_full_name, bg="#D1E338", font=("Cooper Black", 24))
        segula.grid(column=0, columnspan=4, row=0, padx=110, pady=10)

        segulaPrincipal = Label(self.history, text="Patient Clinical History", bg="#D1E338", font=("Cooper Black", 15))
        segulaPrincipal.grid(column=0, columnspan=2, row=1, padx=110, pady=15)
        
        row = 3
        label_names = {}
        self.entry_fields = {}  # Store Entry widgets for each field
        self.text_areas = {}  # Store Text widgets for 'remarks', 'dosage', and 'treatment' fields

        label_names = {
                'documentNumber': 'Document Number',
                'date': 'Date Last Appointment',
                'lifeCoach': 'Life Coach',
                'weight': 'Patient Weight',
                'height': 'Patient Height',
                'remarks': 'Patient Remarks',
                'dosage': 'Patient Dosage',
                'treatment': 'Patient Treatment',
            }

        save_button = Button(self.history, text="Save", command=self.save_data, bg="black", fg="white")
        save_button.grid(row=22, column=1, padx=10, pady=5, sticky="w")        
        
        for key, value in self.clinical_history_data.items():
            if key != '_id':
                label_text = label_names.get(key, key)
                label = Label(self.history, text=label_text, bg="#D1E338")
                label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

                if key in ('remarks', 'dosage', 'treatment'):
                    # Create a Text widget for 'remarks', 'dosage', and 'treatment' fields
                    text_area = Text(self.history, height=5, width=30)
                    text_area.insert(tk.END, value)  # Populate the Text with the existing value
                    text_area.grid(row=row, column=1, padx=10, pady=5, sticky="w")
                    self.text_areas[key] = text_area
                else:
                    # Create an editable Entry widget for other fields
                    entry_field = Entry(self.history)
                    entry_field.insert(0, value)  # Populate the Entry with the existing value
                    entry_field.grid(row=row, column=1, padx=10, pady=5, sticky="w")
                    self.entry_fields[key] = entry_field

                row += 1
                
    def save_data(self):
        # Get the database and the collection
        db = self.get_database()
        collection = db['clinicalHistory']
        # Prepare the data to update
        clinical_history_data_id = self.clinical_history_data['_id']
        data_to_update = {}
        
        for field_name, entry_field in self.entry_fields.items():
            data_to_update[field_name] = entry_field.get()
        
        for field_name, text_area in self.text_areas.items():
            data_to_update[field_name] = text_area.get("1.0", tk.END).strip()

        collection.update_one({'_id': clinical_history_data_id}, {'$set': data_to_update})

        messagebox.showinfo('Success', 'Data updated successfully!')
        self.history.lift()

if __name__ == '__main__':
    history = Tk()
    application4 = segulaClinical(history)
    history.mainloop()
    
