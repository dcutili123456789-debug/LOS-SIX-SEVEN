import tkinter as tk
from ventanas.login import Login
from ventanas.residentes import Residentes
from ventanas.historial import Historial
from ventanas.suministros import Suministros
from ventanas.movimiento import Movimiento
from ventanas.consultas import Consultas
from ventanas.estadisticas import Estadisticas

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("La Estancia")
        self.geometry("900x650")
        self.mostrar_login()

    def mostrar_login(self):
        for w in self.winfo_children():
            w.destroy()
        Login(self, self.mostrar_menu).pack(expand=True)

    def mostrar_menu(self):
        for w in self.winfo_children():
            w.destroy()
        menu = tk.Frame(self)
        menu.pack(side="left", fill="y", padx=10, pady=10)
        zona = tk.Frame(self)
        zona.pack(side="left", fill="both", expand=True)
        self.pantallas = {}
        lista = [("Residentes", Residentes), ("Historial", Historial),
                ("Suministros", Suministros), ("Movimiento", Movimiento),
                ("Consultas", Consultas), ("Estadísticas", Estadisticas)]
        for nombre, clase in lista:
            p = clase(zona)
            p.place(x=0, y=0, relwidth=1, relheight=1)
            self.pantallas[nombre] = p
            tk.Button(menu, text=nombre, width=15,
                      command=lambda n=nombre: self.ir(n)).pack(pady=3)
        tk.Button(menu, text="Cerrar sesión", width=15,
                  command=self.mostrar_login).pack(side="bottom")
        self.ir("Residentes")

    def ir(self, nombre):
        self.pantallas[nombre].refrescar()
        self.pantallas[nombre].tkraise()


App().mainloop()