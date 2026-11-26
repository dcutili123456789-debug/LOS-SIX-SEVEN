import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db import consultar

CONSULTAS = {
    "Residentes por sexo": "SELECT sexo, COUNT(*) FROM Residente GROUP BY sexo",
    "Patologías más frecuentes": "SELECT patologia, COUNT(*) FROM Historial "
                                 "GROUP BY patologia ORDER BY COUNT(*) DESC LIMIT 5",
    "Stock por insumo": "SELECT i.nombre, SUM(l.cantidad) FROM Lote l "
                        "JOIN Insumo i ON i.id_insumo = l.id_insumo "
                        "GROUP BY i.nombre ORDER BY SUM(l.cantidad) DESC LIMIT 5",
    "Entradas vs salidas": "SELECT tipo, COUNT(*) FROM Movimiento GROUP BY tipo",
}


# ================= FÓRMULAS MATEMÁTICAS =================

def porcentaje(valor, total):
    # porcentaje = valor / total * 100
    return valor / total * 100


def promedio(datos):
    # media = suma de los datos / cantidad de datos
    return sum(datos) / len(datos)


def mediana(datos):
    # valor central de los datos ordenados
    ordenados = sorted(datos)
    n = len(ordenados)
    medio = n // 2
    if n % 2 == 1:
        return ordenados[medio]
    return (ordenados[medio - 1] + ordenados[medio]) / 2


def desviacion(datos):
    # s = raíz( suma((x - media)^2) / (n - 1) )
    if len(datos) < 2:
        return 0
    media = promedio(datos)
    suma = sum((x - media) ** 2 for x in datos)
    return (suma / (len(datos) - 1)) ** 0.5


def calcular_edad(nacimiento):
    # edad = año actual - año de nacimiento (menos 1 si aún no cumplió años)
    hoy = date.today()
    cumplio = (hoy.month, hoy.day) >= (nacimiento.month, nacimiento.day)
    return hoy.year - nacimiento.year - (0 if cumplio else 1)


class Estadisticas(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padx=20, pady=15)
        tk.Label(self, text="Estadísticas", font=("Arial", 16, "bold")).pack(anchor="w")

        tk.Label(self, text="Ver gráfica de").pack(anchor="w", pady=(8, 0))
        self.opcion = ttk.Combobox(self, values=list(CONSULTAS), state="readonly", width=40)
        self.opcion.set("Residentes por sexo")
        self.opcion.pack(anchor="w")
        self.opcion.bind("<<ComboboxSelected>>", lambda e: self.refrescar())

        self.figura = Figure(figsize=(8, 3.4), dpi=90)
        self.lienzo = FigureCanvasTkAgg(self.figura, master=self)
        self.lienzo.get_tk_widget().pack(anchor="w", pady=8)

        self.resumen = tk.Label(self, text="", justify="left")
        self.resumen.pack(anchor="w")
        self.edades = tk.Label(self, text="", justify="left")
        self.edades.pack(anchor="w", pady=(6, 0))

    def refrescar(self):
        try:
            filas = consultar(CONSULTAS[self.opcion.get()])
            nacimientos = consultar("SELECT fecha_nac FROM Residente")
        except Exception as error:
            messagebox.showerror("Error", str(error))
            return

        self.figura.clear()
        if not filas:
            self.figura.text(0.5, 0.5, "Sin datos todavía", ha="center")
            self.lienzo.draw()
            self.resumen.config(text="")
        else:
            nombres = [str(f[0]) for f in filas]
            valores = [int(f[1]) for f in filas]
            total = sum(valores) or 1
            porcentajes = [porcentaje(v, total) for v in valores]

            barras, pastel = self.figura.subplots(1, 2)
            grafica = barras.bar(nombres, valores, color=[f"C{i}" for i in range(len(valores))])
            barras.bar_label(grafica)
            barras.set_title("Cantidad")
            barras.tick_params(axis="x", labelrotation=30)

            etiquetas = [f"{n}\n{p:.1f}%" for n, p in zip(nombres, porcentajes)]
            pastel.pie(valores, labels=etiquetas)
            pastel.set_title("Porcentaje")
            self.figura.tight_layout()
            self.lienzo.draw()

            detalle = "   ".join(f"{n}: {v}/{total} = {p:.1f}%"
                                 for n, v, p in zip(nombres, valores, porcentajes))
            self.resumen.config(text=f"{detalle}\n"
                                     f"Total: {total}   Promedio: {promedio(valores):.1f}   "
                                     f"Mediana: {mediana(valores)}   "
                                     f"Desv. estándar: {desviacion(valores):.1f}")

        edades = [calcular_edad(f[0]) for f in nacimientos]
        if edades:
            self.edades.config(text=f"Edad de los residentes → Promedio: {promedio(edades):.1f}   "
                                    f"Mediana: {mediana(edades)}   "
                                    f"Desv. estándar: {desviacion(edades):.1f}   "
                                    f"Mín: {min(edades)}   Máx: {max(edades)}")
        else:
            self.edades.config(text="Sin residentes registrados")