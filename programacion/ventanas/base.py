"""Piezas comunes: pantalla base, campos del formulario, tabla emergente."""
import functools
import tkinter as tk
from tkinter import ttk, messagebox

import mysql.connector

from db import mostrar as formatear


def seguro(fn):
    """Muestra los errores en un cuadro en vez de cerrar el programa."""
    @functools.wraps(fn)
    def envoltura(*a, **k):
        try:
            return fn(*a, **k)
        except ValueError as e:
            messagebox.showerror("Dato inválido", str(e))
        except mysql.connector.Error as e:
            messagebox.showerror("Error de base de datos", e.msg)
    return envoltura


class Pantalla(tk.Frame):
    def __init__(self, padre, titulo):
        super().__init__(padre, padx=25, pady=20)
        tk.Label(self, text=titulo, font=("Arial", 18, "bold")).pack(anchor="w")
        tk.Frame(self, height=2, bd=1, relief="solid").pack(fill="x", pady=(2, 12))

    def refrescar(self):
        pass


def crear_campos(frame, campos, completos=()):
    """campos: (clave, etiqueta, opciones o None, editable opcional).
    Devuelve el diccionario de widgets. Dos columnas."""
    w, fila, col = {}, 0, 0
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    for clave, etiqueta, opciones, *ed in campos:
        completo = clave in completos
        if completo and col == 1:
            fila, col = fila + 2, 0
        span = 2 if completo else 1
        tk.Label(frame, text=etiqueta, anchor="w").grid(
            row=fila, column=col, columnspan=span, sticky="w", padx=10, pady=(8, 0))
        if opciones is None:
            e = tk.Entry(frame)
        else:
            estado = "normal" if (ed and ed[0]) else "readonly"
            e = ttk.Combobox(frame, values=opciones, state=estado)
        e.grid(row=fila + 1, column=col, columnspan=span, sticky="we", padx=10)
        w[clave] = e
        if completo or col == 1:
            fila, col = fila + 2, 0
        else:
            col = 1
    return w


def valores(w):
    return {k: v.get().strip() for k, v in w.items()}


def limpiar(w):
    for v in w.values():
        if isinstance(v, ttk.Combobox):
            v.set("")
        else:
            v.delete(0, "end")


def botones(padre, registrar, consultar):
    f = tk.Frame(padre)
    f.pack(anchor="w", pady=12)
    tk.Button(f, text="Registrar", width=14, command=registrar).pack(side="left", padx=5)
    tk.Button(f, text="Consultar", width=14, command=consultar).pack(side="left", padx=5)


def ventana_tabla(titulo, columnas, filas):
    top = tk.Toplevel()
    top.title(titulo)
    top.geometry("800x350")
    tabla = ttk.Treeview(top, columns=columnas, show="headings")
    for c in columnas:
        tabla.heading(c, text=c)
        tabla.column(c, width=110)
    for f in filas:
        tabla.insert("", "end", values=formatear(f))
    tabla.pack(fill="both", expand=True)
    if not filas:
        messagebox.showinfo("Consultar", "No se encontraron registros.", parent=top)
