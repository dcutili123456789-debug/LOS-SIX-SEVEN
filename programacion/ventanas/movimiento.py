import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar, consultar, fecha

CAMPOS = [("tipo", "Tipo (entrada o salida)"), ("lote", "Insumo y lote (muestra el stock)"),
          ("cantidad", "Cantidad"), ("ci", "Residente CI (solo salidas)"),
          ("fecha", "Fecha (dd/mm/aaaa)"), ("obs", "Observación / motivo (opcional)")]


class Movimiento(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padx=20, pady=20)
        tk.Label(self, text="Movimiento", font=("Arial", 16, "bold")).pack(anchor="w")
        self.e = {}
        for clave, texto in CAMPOS:
            tk.Label(self, text=texto).pack(anchor="w", pady=(6, 0))
            if clave == "tipo":
                self.e[clave] = ttk.Combobox(self, values=["entrada", "salida"], state="readonly", width=42)
            elif clave == "lote":
                self.e[clave] = ttk.Combobox(self, state="readonly", width=60)
            else:
                self.e[clave] = tk.Entry(self, width=45)
            self.e[clave].pack(anchor="w")
        tk.Button(self, text="Registrar", width=15, command=self.registrar).pack(anchor="w", pady=12)

    def refrescar(self):
        filas = consultar("SELECT l.id_lote, i.nombre, l.numero_lote, l.cantidad FROM Lote l "
                          "JOIN Insumo i ON i.id_insumo = l.id_insumo ORDER BY i.nombre")
        self.e["lote"]["values"] = [f"{a} | {b} | Lote {c} | stock {d}" for a, b, c, d in filas]

    def registrar(self):
        try:
            v = {k: e.get().strip() for k, e in self.e.items()}
            id_lote = int(v["lote"].split("|")[0])
            cantidad = int(v["cantidad"])
            con = conectar()
            cur = con.cursor()
            id_residente = None
            if v["tipo"] == "salida":
                cur.execute("SELECT id_residente FROM Residente WHERE ci=%s", (v["ci"],))
                r = cur.fetchone()
                if not r:
                    raise Exception("No existe un residente con esa CI")
                id_residente = r[0]
                cur.execute("UPDATE Lote SET cantidad = cantidad - %s WHERE id_lote=%s", (cantidad, id_lote))
            else:
                cur.execute("UPDATE Lote SET cantidad = cantidad + %s WHERE id_lote=%s", (cantidad, id_lote))
            cur.execute("INSERT INTO Movimiento (id_lote, id_residente, tipo, cantidad, fecha, observacion) "
                        "VALUES (%s,%s,%s,%s,%s,%s)",
                        (id_lote, id_residente, v["tipo"], cantidad, fecha(v["fecha"]), v["obs"]))
            con.commit()
            con.close()
            messagebox.showinfo("Movimiento", "Movimiento registrado")
            for e in self.e.values():
                if isinstance(e, ttk.Combobox):
                    e.set("")
                else:
                    e.delete(0, "end")
            self.refrescar()
        except Exception as error:
            messagebox.showerror("Error", str(error))