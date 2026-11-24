import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db import consultar, mostrar

CONSULTAS = {
    "Residentes": "SELECT CONCAT(nombre,' ',apellidos), ci, IFNULL(contacto_familiar,''), sexo, '', fecha_ingreso "
                  "FROM Residente WHERE ci LIKE %s OR nombre LIKE %s OR apellidos LIKE %s",
    "Historial": "SELECT CONCAT(r.nombre,' ',r.apellidos), r.ci, h.patologia, h.responsable, '', h.fecha "
                 "FROM Historial h JOIN Residente r ON r.id_residente = h.id_residente "
                 "WHERE r.ci LIKE %s OR r.nombre LIKE %s OR h.patologia LIKE %s",
    "Insumos": "SELECT i.nombre, l.numero_lote, c.nombre, '', l.cantidad, l.vence "
               "FROM Lote l JOIN Insumo i ON i.id_insumo = l.id_insumo "
               "JOIN Categoria c ON c.id_categoria = i.id_categoria "
               "WHERE i.nombre LIKE %s OR l.numero_lote LIKE %s OR c.nombre LIKE %s",
    "Movimientos": "SELECT i.nombre, l.numero_lote, IFNULL(m.observacion,''), m.tipo, m.cantidad, m.fecha "
                   "FROM Movimiento m JOIN Lote l ON l.id_lote = m.id_lote "
                   "JOIN Insumo i ON i.id_insumo = l.id_insumo "
                   "WHERE i.nombre LIKE %s OR l.numero_lote LIKE %s OR m.tipo LIKE %s",
}
COLUMNAS = ["Nombre / Insumo", "CI / Lote", "Detalle", "Tipo", "Cantidad", "Fecha"]


class Consultas(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padx=20, pady=20)
        tk.Label(self, text="Consultas", font=("Arial", 16, "bold")).pack(anchor="w")
        tk.Label(self, text="Consultar en").pack(anchor="w", pady=(8, 0))
        self.donde = ttk.Combobox(self, values=list(CONSULTAS), state="readonly", width=42)
        self.donde.set("Residentes")
        self.donde.pack(anchor="w")
        tk.Label(self, text="Buscar (CI, nombre, lote...)").pack(anchor="w", pady=(8, 0))
        self.texto = tk.Entry(self, width=45)
        self.texto.pack(anchor="w")
        tk.Button(self, text="Buscar", width=15, command=self.buscar).pack(anchor="w", pady=10)
        self.tabla = ttk.Treeview(self, columns=COLUMNAS, show="headings", height=12)
        for c in COLUMNAS:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=105)
        self.tabla.pack(fill="both", expand=True)

    def refrescar(self):
        pass

    def buscar(self):
        try:
            sql = CONSULTAS[self.donde.get()]
            patron = f"%{self.texto.get().strip()}%"
            self.tabla.delete(*self.tabla.get_children())
            for fila in consultar(sql, (patron, patron, patron)):
                self.tabla.insert("", "end", values=mostrar(fila))
        except Exception as error:
            messagebox.showerror("Error", str(error))