from ventanas.estilo import *
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
        super().__init__(padre)
        card=pagina(self,'Consultas'); f=tk.Frame(card,bg=BLANCO); f.pack(fill='x')
        w=campos(f,[('donde','Consultar en'),('texto','Buscar (CI, nombre, lote...)')],{'donde':list(CONSULTAS)})
        self.donde=w['donde']; self.texto=w['texto']; self.donde.set('Residentes')
        boton(card,'Buscar',self.buscar).pack(anchor='w',padx=9,pady=18)
        area=tk.Frame(card,bg=BLANCO); area.pack(fill='both',expand=True)
        self.tabla=ttk.Treeview(area,columns=COLUMNAS,show='headings',height=10)
        for c in COLUMNAS:
            self.tabla.heading(c,text=c); self.tabla.column(c,width=105,minwidth=75)
        y=ttk.Scrollbar(area,orient='vertical',command=self.tabla.yview); x=ttk.Scrollbar(area,orient='horizontal',command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=y.set,xscrollcommand=x.set)
        y.pack(side='right',fill='y'); x.pack(side='bottom',fill='x'); self.tabla.pack(fill='both',expand=True)
        self.texto.bind('<Return>',lambda e:self.buscar())

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