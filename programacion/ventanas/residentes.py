from ventanas.estilo import formulario
import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar, fecha

CAMPOS = [("ci", "CI"), ("nombre", "Nombre(s)"), ("apellidos", "Apellido(s)"),
          ("nac", "Fecha de nacimiento (dd/mm/aaaa)"),
          ("ingreso", "Fecha de ingreso (dd/mm/aaaa)"),
          ("contacto", "Contacto familiar (nombre y teléfono)")]


class Residentes(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.e = formulario(self, 'Registro de residentes', CAMPOS[:4] + [("sexo", "Sexo")] + CAMPOS[4:], self.registrar, 'Residentes', {"sexo":["Femenino","Masculino"]}, ("contacto",))
        self.sexo = self.e.pop("sexo")

    def refrescar(self):
        pass

    def registrar(self):
        try:
            v = {k: e.get().strip() for k, e in self.e.items()}
            con = conectar()
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Residente (ci, nombre, apellidos, fecha_nac, sexo, fecha_ingreso, contacto_familiar) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (v["ci"], v["nombre"], v["apellidos"], fecha(v["nac"]),
                 self.sexo.get(), fecha(v["ingreso"]), v["contacto"]))
            con.commit()
            con.close()
            messagebox.showinfo("Residentes", "Residente registrado")
            for e in self.e.values():
                e.delete(0, "end")
            self.sexo.set("")
        except Exception as error:
            messagebox.showerror("Error", str(error))