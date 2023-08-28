from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient
from PIL import Image, ImageTk
from segulaPrincipal import SegulaPrincipal

class SegulaLogin:
    db_name = 'SegulaPatients'

    def __init__(self, login):
        self.login = login
        self.login.title('Segula Nutrition')
        self.login.iconbitmap('segula.ico')
        self.login.resizable(False, False)
        ancho_ventana = self.login.winfo_reqwidth()
        alto_ventana = self.login.winfo_reqheight()
        posicion_x = int((self.login.winfo_screenwidth() / 2) - (ancho_ventana / 2))
        posicion_y = int((self.login.winfo_screenheight() / 2) - (alto_ventana / 2))

        self.login.geometry("+{}+{}".format(posicion_x, posicion_y))
        self.login.configure(bg="black")
        
        # Carga la imagen de fondo
        image = Image.open("segula.png")
        image = image.resize((500, 300))
        
        # Convertir la imagen a un objeto PhotoImage
        photo = ImageTk.PhotoImage(image)
        
        # widget Label para mostrar la imagen de fondo
        background_label = Label(self.login, image=photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        background_label.image = photo
        
        segula = Label(self.login, text="Segula Nutrition", font=("Cooper Black", 24))
        segula.grid(column=0, row=0, padx=110)

        segulaLogin = Label(self.login, text="Login", font=("Cooper Black", 20))
        segulaLogin.grid(column=0, row=1, padx=110)

        segulaUsername = Label(self.login, text="Username")
        segulaUsername.grid(column=0, row=2, padx=10, pady=5)

        self.username = Entry(self.login, width=35)
        self.username.grid(column=0, row=3, padx=3, pady=5)

        segulaPassword = Label(self.login, text="Password")
        segulaPassword.grid(column=0, row=4, padx=10, pady=5)

        self.password = Entry(self.login, width=35, show='*')
        self.password.grid(column=0, row=5, padx=3, pady=5)

        segulaLoginSystem = ttk.Button(self.login, text="LOGIN", command=self.validate_login)
        segulaLoginSystem.grid(column=0, row=6, pady=20)

    def validate_login(self):
        username = self.username.get()
        password = self.password.get()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password.")
            return

        client = MongoClient('mongodb://localhost:27017/')
        db = client[self.db_name]
        collection = db['Doctors']

        user = collection.find_one({'username': username, 'password': password})
        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.login.destroy()
            principal = Tk()
            application2 = SegulaPrincipal(principal)
            principal.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password.")
            self.username.delete(0, 'end')
            self.password.delete(0, 'end')
            
if __name__ == '__main__':
    login = Tk()
    application1 = SegulaLogin(login)
    login.mainloop()

