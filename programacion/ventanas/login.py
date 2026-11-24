import tkinter as tk
from tkinter import messagebox
from db import consultar, hash_clave


class Login(tk.Frame):
    def __init__(self, padre, al_entrar):
        super().__init__(padre, padx=40, pady=40)
        self.al_entrar = al_entrar
        tk.Label(self, text="La Estancia", font=("Arial", 20, "bold")).pack()
        tk.Label(self, text="Casa de asistencia al adulto mayor").pack(pady=(0, 15))
        tk.Label(self, text="Usuario").pack(anchor="w")
        self.usuario = tk.Entry(self, width=30)
        self.usuario.pack()
        tk.Label(self, text="Contraseña").pack(anchor="w", pady=(10, 0))
        self.clave = tk.Entry(self, width=30, show="*")
        self.clave.pack()
        tk.Button(self, text="Ingresar", command=self.ingresar).pack(pady=15)

    def ingresar(self):
        try:
            r = consultar("SELECT id_usuario FROM Usuario WHERE usuario=%s AND contrasena=%s",
                          (self.usuario.get().strip(), hash_clave(self.clave.get())))
        except Exception as error:
            messagebox.showerror("Error", str(error))
            return
        if r:
            self.al_entrar()
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")