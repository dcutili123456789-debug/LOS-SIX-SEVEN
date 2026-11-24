import tkinter as tk
from tkinter import messagebox
from db import conectar, fecha

CAMPOS = [("nombre", "Insumo / medicamento"), ("descripcion", "Descripción"),
          ("categoria", "Categoría"), ("proveedor", "Proveedor"),
          ("lote", "N.º de lote"), ("cantidad", "Cantidad"),
          ("vence", "Fecha de vencimiento (dd/mm/aaaa)"),
          ("stock_min", "Stock mínimo (alerta)")]


def buscar_o_crear(cur, tabla, col_id, nombre):
    cur.execute(f"SELECT {col_id} FROM {tabla} WHERE nombre=%s", (nombre,))
    r = cur.fetchone()
    if r:
        return r[0]
    cur.execute(f"INSERT INTO {tabla} (nombre) VALUES (%s)", (nombre,))
    return cur.lastrowid


class Suministros(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, padx=20, pady=20)
        tk.Label(self, text="Suministros", font=("Arial", 16, "bold")).pack(anchor="w")
        self.e = {}
        for clave, texto in CAMPOS:
            tk.Label(self, text=texto).pack(anchor="w", pady=(6, 0))
            self.e[clave] = tk.Entry(self, width=45)
            self.e[clave].pack(anchor="w")
        tk.Button(self, text="Registrar", width=15, command=self.registrar).pack(anchor="w", pady=12)

    def refrescar(self):
        pass

    def registrar(self):
        try:
            v = {k: e.get().strip() for k, e in self.e.items()}
            con = conectar()
            cur = con.cursor()
            id_cat = buscar_o_crear(cur, "Categoria", "id_categoria", v["categoria"])
            id_prov = buscar_o_crear(cur, "Proveedor", "id_proveedor", v["proveedor"])
            cur.execute("SELECT id_insumo FROM Insumo WHERE nombre=%s AND id_categoria=%s",
                        (v["nombre"], id_cat))
            r = cur.fetchone()
            if r:
                id_insumo = r[0]
            else:
                cur.execute("INSERT INTO Insumo (nombre, descripcion, id_categoria, stock_min) "
                            "VALUES (%s,%s,%s,%s)",
                            (v["nombre"], v["descripcion"], id_cat, int(v["stock_min"])))
                id_insumo = cur.lastrowid
            if v["categoria"].lower() in ("medicamento", "medicamentos"):
                cur.execute("SELECT id_medicamento FROM Medicamento WHERE id_insumo=%s", (id_insumo,))
                if not cur.fetchone():
                    cur.execute("INSERT INTO Medicamento (id_insumo) VALUES (%s)", (id_insumo,))
            vence = fecha(v["vence"]) if v["vence"] else None
            cur.execute("INSERT INTO Lote (id_insumo, id_proveedor, numero_lote, cantidad, vence) "
                        "VALUES (%s,%s,%s,%s,%s)",
                        (id_insumo, id_prov, v["lote"], int(v["cantidad"]), vence))
            con.commit()
            con.close()
            messagebox.showinfo("Suministros", "Insumo y lote registrados")
            for e in self.e.values():
                e.delete(0, "end")
        except Exception as error:
            messagebox.showerror("Error", str(error))