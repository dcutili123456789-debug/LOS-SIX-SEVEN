import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar, fecha

CAMPOS = [("ci", "CI"), ("nombre", "Nombre(s)"), ("apellidos", "Apellido(s)"),
          ("nac", "Fecha de nacimiento (dd/mm/aaaa)"),
          ("ingreso", "Fecha de ingreso (dd/mm/aaaa)"),
          ("contacto", "Contacto familiar (nombre y teléfono)")]


class Residentes(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padx=20, pady=20)
        tk.Label(self, text="Registro de residentes", font=("Arial", 16, "bold")).pack(anchor="w")
        self.e = {}
        for clave, texto in CAMPOS:
            tk.Label(self, text=texto).pack(anchor="w", pady=(8, 0))
            self.e[clave] = tk.Entry(self, width=45)
            self.e[clave].pack(anchor="w")
        tk.Label(self, text="Sexo").pack(anchor="w", pady=(8, 0))
        self.sexo = ttk.Combobox(self, values=["Femenino", "Masculino"], state="readonly", width=42)
        self.sexo.pack(anchor="w")
        tk.Button(self, text="Registrar", width=15, command=self.registrar).pack(anchor="w", pady=15)

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