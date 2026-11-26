import tkinter as tk
from tkinter import ttk
AZUL='#0B3D91'; AMARILLO='#FFA600'; FONDO='#F0F4F9'; BLANCO='#FFFFFF'; TEXTO='#142139'; GRIS='#596579'; BORDE='#A0AEC2'
FUENTE='Segoe UI'
def configurar(root):
    root.option_add('*Font', (FUENTE, 11))
    s=ttk.Style(root); s.theme_use('clam')
    s.configure('TCombobox', padding=8, fieldbackground=BLANCO, background=BLANCO, foreground=TEXTO, bordercolor=BORDE, arrowsize=15)
    s.map('TCombobox', fieldbackground=[('readonly',BLANCO)], foreground=[('readonly',TEXTO)], selectbackground=[('readonly',BLANCO)], selectforeground=[('readonly',TEXTO)])
    s.configure('Treeview', background=BLANCO, fieldbackground=BLANCO, foreground=TEXTO, rowheight=34, font=(FUENTE,10))
    s.configure('Treeview.Heading', background=AZUL, foreground=BLANCO, font=(FUENTE,10,'bold'), padding=9)
    s.map('Treeview.Heading', background=[('active','#174FA6')]); s.map('Treeview',background=[('selected','#DCE9FA')],foreground=[('selected',TEXTO)])
def etiqueta(p,text,**kw):
    return tk.Label(p,text=text,bg=kw.pop('bg',BLANCO),fg=kw.pop('fg',GRIS),font=kw.pop('font',(FUENTE,11)),**kw)
def entrada(p,**kw):
    return tk.Entry(p,bg=BLANCO,fg=TEXTO,insertbackground=TEXTO,relief='flat',highlightthickness=1,highlightbackground=BORDE,highlightcolor=AZUL,font=(FUENTE,12),**kw)
def boton(p,text,command,sec=False,amarillo=False):
    bg=AMARILLO if amarillo else BLANCO if sec else AZUL; fg=AZUL if sec or amarillo else BLANCO
    b=tk.Button(p,text=text,command=command,bg=bg,fg=fg,activebackground='#FFD071' if amarillo else '#DCE9FA' if sec else '#174FA6',activeforeground=fg,relief='flat',bd=0,highlightthickness=1 if sec else 0,highlightbackground=AZUL,font=(FUENTE,11,'bold'),cursor='hand2',padx=25,pady=12)
    return b
def pagina(p,titulo):
    p.configure(bg=FONDO,padx=30,pady=25)
    etiqueta(p,titulo,bg=FONDO,fg=TEXTO,font=(FUENTE,25,'bold')).pack(anchor='w')
    tk.Frame(p,bg=AMARILLO,width=64,height=5).pack(anchor='w',pady=(12,20))
    card=tk.Frame(p,bg=BLANCO,highlightthickness=1,highlightbackground='#D3DAE4',padx=20,pady=18)
    card.pack(fill='both',expand=True); return card
def campos(p,items,opciones=None,completos=()):
    opciones=opciones or {}; widgets={}; r=c=0
    for i in range(2): p.columnconfigure(i,weight=1,uniform='campos')
    for clave,texto in items:
        full=clave in completos
        if full and c: r+=2; c=0
        span=2 if full else 1
        etiqueta(p,texto).grid(row=r,column=c,columnspan=span,sticky='w',padx=9,pady=(10,5))
        e=ttk.Combobox(p,values=opciones[clave],state='readonly',width=1) if clave in opciones else entrada(p,width=1)
        e.grid(row=r+1,column=c,columnspan=span,sticky='ew',padx=9,ipady=8 if clave not in opciones else 0)
        widgets[clave]=e
        if full or c: r+=2;c=0
        else: c=1
    return widgets
def acciones(p,registrar,consultar):
    f=tk.Frame(p,bg=BLANCO); f.pack(fill='x',pady=(22,0)); boton(f,'Registrar',registrar).pack(side='left',padx=(9,12)); boton(f,'Consultar',consultar,sec=True).pack(side='left')
def formulario(p,titulo,items,registrar,destino,opciones=None,completos=()):
    card=pagina(p,titulo); f=tk.Frame(card,bg=BLANCO); f.pack(fill='x'); w=campos(f,items,opciones,completos)
    acciones(card,registrar,lambda:p.winfo_toplevel().abrir_consulta(destino)); return w
