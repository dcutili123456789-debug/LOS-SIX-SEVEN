from ventanas.estilo import *
import tkinter as tk
from tkinter import messagebox
from db import consultar, hash_clave


class Login(tk.Frame):
    def __init__(self, padre, al_entrar):
        super().__init__(padre,bg=AZUL)
        self.al_entrar=al_entrar
        etiqueta(self,'La Estancia',bg=AZUL,fg=AMARILLO,font=(FUENTE,32,'bold')).pack(pady=(0,12))
        etiqueta(self,'Casa de asistencia al adulto mayor',bg=AZUL,fg=BLANCO,font=(FUENTE,14)).pack(pady=(0,22))
        card=tk.Frame(self,bg=BLANCO,padx=26,pady=22,highlightthickness=1,highlightbackground=BORDE); card.pack()
        etiqueta(card,'Iniciar sesión',fg=TEXTO,font=(FUENTE,21,'bold')).pack(anchor='w',pady=(0,12))
        etiqueta(card,'Usuario').pack(anchor='w')
        self.usuario=entrada(card,width=30); self.usuario.pack(fill='x',ipady=10,pady=(5,14))
        etiqueta(card,'Contraseña').pack(anchor='w')
        self.clave=entrada(card,width=30,show='*'); self.clave.pack(fill='x',ipady=10,pady=(5,22))
        boton(card,'Ingresar',self.ingresar,amarillo=True).pack(fill='x')
        self.clave.bind('<Return>',lambda e:self.ingresar()); self.usuario.focus_set()

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