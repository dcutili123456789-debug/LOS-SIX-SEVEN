import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar, consultar, fecha

CAMPOS = [("ci", "Residente (CI)"), ("fecha", "Fecha de registro (dd/mm/aaaa)"),
          ("patologia", "Patología"), ("evolucion", "Evolución"),
          ("medicamento", "Medicamento (opcional)"), ("dosis", "Dosis"),
          ("frecuencia", "Frecuencia"), ("responsable", "Responsable")]


class Historial(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padx=20, pady=20)
        tk.Label(self, text="Historial clínico", font=("Arial", 16, "bold")).pack(anchor="w")
        self.e = {}
        for clave, texto in CAMPOS:
            tk.Label(self, text=texto).pack(anchor="w", pady=(6, 0))
            if clave == "medicamento":
                self.e[clave] = ttk.Combobox(self, state="readonly", width=42)
            else:
                self.e[clave] = tk.Entry(self, width=45)
            self.e[clave].pack(anchor="w")
        tk.Button(self, text="Registrar", width=15, command=self.registrar).pack(anchor="w", pady=12)

    def refrescar(self):
        filas = consultar("SELECT i.nombre FROM Medicamento m JOIN Insumo i ON i.id_insumo = m.id_insumo")
        self.e["medicamento"]["values"] = [""] + [f[0] for f in filas]

    def registrar(self):
        try:
            v = {k: e.get().strip() for k, e in self.e.items()}
            con = conectar()
            cur = con.cursor()
            cur.execute("SELECT id_residente FROM Residente WHERE ci=%s", (v["ci"],))
            r = cur.fetchone()
            if not r:
                raise Exception("No existe un residente con esa CI")
            cur.execute("INSERT INTO Historial (id_residente, patologia, evolucion, fecha, responsable) "
                        "VALUES (%s,%s,%s,%s,%s)",
                        (r[0], v["patologia"], v["evolucion"], fecha(v["fecha"]), v["responsable"]))
            id_historial = cur.lastrowid
            if v["medicamento"]:
                cur.execute("SELECT m.id_medicamento FROM Medicamento m JOIN Insumo i "
                            "ON i.id_insumo = m.id_insumo WHERE i.nombre=%s", (v["medicamento"],))
                m = cur.fetchone()
                cur.execute("INSERT INTO Prescripcion (id_historial, id_residente, id_medicamento, dosis, frecuencia) "
                            "VALUES (%s,%s,%s,%s,%s)",
                            (id_historial, r[0], m[0], v["dosis"], v["frecuencia"]))
            con.commit()
            con.close()
            messagebox.showinfo("Historial", "Registro guardado")
            for e in self.e.values():
                if isinstance(e, ttk.Combobox):
                    e.set("")
                else:
                    e.delete(0, "end")
        except Exception as error:
            messagebox.showerror("Error", str(error))