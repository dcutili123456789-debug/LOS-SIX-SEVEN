import tkinter as tk
from ventanas.estilo import *
from ventanas.login import Login
from ventanas.residentes import Residentes
from ventanas.historial import Historial
from ventanas.suministros import Suministros
from ventanas.movimiento import Movimiento
from ventanas.consultas import Consultas
from ventanas.estadisticas import Estadisticas
class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title('La Estancia | Sistema de gestión'); self.geometry('1100x720'); self.minsize(900,650); configurar(self); self.mostrar_login()
    def mostrar_login(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(bg=AZUL); Login(self,self.mostrar_menu).pack(expand=True)
    def mostrar_menu(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(bg=FONDO)
        menu=tk.Frame(self,bg=AZUL,width=230); menu.pack(side='left',fill='y'); menu.pack_propagate(False)
        etiqueta(menu,'La Estancia',bg=AZUL,fg=AMARILLO,font=(FUENTE,23,'bold')).pack(anchor='w',padx=20,pady=(30,8))
        etiqueta(menu,'Sistema de gestión',bg=AZUL,fg=BLANCO).pack(anchor='w',padx=20,pady=(0,30))
        zona=tk.Frame(self,bg=FONDO); zona.pack(side='left',fill='both',expand=True)
        self.pantallas={}; self.botones={}
        for nombre,clase in [('Residentes',Residentes),('Historial',Historial),('Suministros',Suministros),('Movimiento',Movimiento),('Consultas',Consultas),('Estadísticas',Estadisticas)]:
            p=clase(zona); p.place(x=0,y=0,relwidth=1,relheight=1); self.pantallas[nombre]=p
            b=tk.Button(menu,text=nombre,anchor='w',padx=14,pady=15,bg=AZUL,fg=BLANCO,activebackground=AMARILLO,activeforeground=AZUL,bd=0,relief='flat',cursor='hand2',font=(FUENTE,12),command=lambda n=nombre:self.ir(n)); b.pack(fill='x',padx=12,pady=3); self.botones[nombre]=b
        boton(menu,'Cerrar sesión',self.mostrar_login,sec=True).pack(side='bottom',fill='x',padx=12,pady=18)
        self.ir('Residentes')
    def ir(self,nombre):
        for n,b in self.botones.items(): b.configure(bg=AMARILLO if n==nombre else AZUL,fg=AZUL if n==nombre else BLANCO,font=(FUENTE,12,'bold' if n==nombre else 'normal'))
        self.pantallas[nombre].tkraise(); self.pantallas[nombre].refrescar()
    def abrir_consulta(self,destino):
        self.ir('Consultas'); p=self.pantallas['Consultas']; p.donde.set(destino); p.texto.delete(0,'end'); p.buscar()
if __name__=='__main__': App().mainloop()
