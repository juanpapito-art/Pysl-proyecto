import customtkinter as ctk
import os
from datetime import datetime
from tkinter import messagebox
import pandas as pd

# Configuración del entorno
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("ACTA DE INSPECCIÓN DE SEGURIDAD - BOMBEROS LA ESTRELLA")
app.geometry("1200x950")

# Contenedor con Scroll para la hoja completa
main_frame = ctk.CTkScrollableFrame(app, width=1150, height=900)
main_frame.pack(side="top", pady=10, padx=10, fill="both", expand=True)

# --- ENCABEZADO OFICIAL ---
ctk.CTkLabel(main_frame, text="CUERPO DE BOMBEROS VOLUNTARIOS DE LA ESTRELLA", font=("Arial", 22, "bold")).pack()
ctk.CTkLabel(main_frame, text="DEPARTAMENTO DE PREVENCIÓN Y SEGURIDAD", font=("Arial", 16)).pack(pady=(0, 20))

# Repositorios de widgets para leer valores
entries = {}
segs = {}
checks = {}
materials = []

def make_label_entry(parent, text, key, width=150):
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(fill="x", padx=5, pady=2)
    ctk.CTkLabel(f, text=text, width=160, anchor="w").pack(side="left")
    e = ctk.CTkEntry(f, width=width)
    e.pack(side="left", padx=5)
    entries[key] = e
    return e

# --- SECCIÓN: DATOS DE IDENTIFICACIÓN ---
f_ident = ctk.CTkFrame(main_frame)
f_ident.pack(fill="x", padx=10, pady=5)

# Línea 1: Fecha, Formato, Nit, Teléfono
l1 = ctk.CTkFrame(f_ident, fg_color="transparent")
l1.pack(fill="x", padx=10, pady=5)
ctk.CTkLabel(l1, text="DÍA:").grid(row=0, column=0)
entries['dia'] = ctk.CTkEntry(l1, width=40); entries['dia'].grid(row=0, column=1, padx=2)
ctk.CTkLabel(l1, text="MES:").grid(row=0, column=2, padx=5)
entries['mes'] = ctk.CTkEntry(l1, width=40); entries['mes'].grid(row=0, column=3, padx=2)
ctk.CTkLabel(l1, text="AÑO:").grid(row=0, column=4, padx=5)
entries['anio'] = ctk.CTkEntry(l1, width=60); entries['anio'].grid(row=0, column=5, padx=2)
ctk.CTkLabel(l1, text="Formato:").grid(row=0, column=6, padx=15)
entries['formato'] = ctk.CTkEntry(l1, width=120); entries['formato'].grid(row=0, column=7)
ctk.CTkLabel(l1, text="Nit:").grid(row=0, column=8, padx=15)
entries['nit'] = ctk.CTkEntry(l1, width=150); entries['nit'].grid(row=0, column=9)
ctk.CTkLabel(l1, text="Teléfono:").grid(row=0, column=10, padx=15)
entries['telefono'] = ctk.CTkEntry(l1, width=120); entries['telefono'].grid(row=0, column=11)

# Establecimiento y Dirección
ctk.CTkLabel(f_ident, text="Establecimiento:").pack(anchor="w", padx=10)
entries['establecimiento'] = ctk.CTkEntry(f_ident, width=1000); entries['establecimiento'].pack(padx=10, pady=2)

l2 = ctk.CTkFrame(f_ident, fg_color="transparent")
l2.pack(fill="x", padx=10, pady=5)
ctk.CTkLabel(l2, text="Dirección No.").grid(row=0, column=0)
entries['direccion_no'] = ctk.CTkEntry(l2, width=150); entries['direccion_no'].grid(row=0, column=1, padx=5)
ctk.CTkLabel(l2, text="Barrio:").grid(row=0, column=2, padx=10)
entries['barrio'] = ctk.CTkEntry(l2, width=300); entries['barrio'].grid(row=0, column=3)
ctk.CTkLabel(l2, text="Área:").grid(row=0, column=4, padx=10)
entries['area'] = ctk.CTkEntry(l2, width=80); entries['area'].grid(row=0, column=5)
ctk.CTkLabel(l2, text="mts²").grid(row=0, column=6)

# --- SECCIÓN: PROPIEDAD Y PERSONAL ---
f_prop = ctk.CTkFrame(main_frame)
f_prop.pack(fill="x", padx=10, pady=5)

for t,k in [("Tipo Establecimiento:", 'tipo_establecimiento'), ("Propietario:", 'propietario'), ("Administrador:", 'administrador')]:
    r = ctk.CTkFrame(f_prop, fg_color="transparent")
    r.pack(fill="x", padx=10, pady=2)
    ctk.CTkLabel(r, text=t, width=160, anchor="w").pack(side="left")
    entries[k] = ctk.CTkEntry(r, width=400); entries[k].pack(side="left", padx=5)
    ctk.CTkLabel(r, text="C.C.:").pack(side="left")
    entries[k+'_cc'] = ctk.CTkEntry(r, width=150); entries[k+'_cc'].pack(side="left", padx=5)

# Personal y Niveles
l3 = ctk.CTkFrame(f_prop, fg_color="transparent")
l3.pack(fill="x", padx=10, pady=5)
for txt,key in [("No Empleados:",'no_empleados'), ("No Visitantes:",'no_visitantes'), ("No Niveles:",'no_niveles')]:
    ctk.CTkLabel(l3, text=txt).pack(side="left", padx=5)
    entries[key] = ctk.CTkEntry(l3, width=50); entries[key].pack(side="left", padx=5)
ctk.CTkLabel(l3, text="Mezanines:").pack(side="left", padx=10)
segs['mezanines'] = ctk.CTkSegmentedButton(l3, values=["SÍ", "NO"]); segs['mezanines'].pack(side="left")
ctk.CTkLabel(l3, text="Material:").pack(side="left", padx=10)
entries['material'] = ctk.CTkEntry(l3, width=150); entries['material'].pack(side="left")

# --- SECCIÓN: BLOQUES TÉCNICOS (CONSTRUCCIÓN, ELÉCTRICAS, ALMACENAMIENTO, ASEO) ---
f_grid = ctk.CTkFrame(main_frame)
f_grid.pack(fill="x", padx=10, pady=10)

def crear_bloque(titulo, items, columna):
    b = ctk.CTkFrame(f_grid)
    b.grid(row=0, column=columna, padx=5, pady=5, sticky="nsew")
    ctk.CTkLabel(b, text=titulo, font=("Arial", 11, "bold")).pack(pady=5)
    for it in items:
        f = ctk.CTkFrame(b, fg_color="transparent")
        f.pack(fill="x", padx=5)
        ctk.CTkLabel(f, text=it, font=("Arial", 10)).pack(side="left")
        key = f"blk_{titulo}_{it}"
        seg = ctk.CTkSegmentedButton(f, values=["B", "R", "M"], width=80)
        seg.pack(side="right", pady=1)
        segs[key] = seg

crear_bloque("CONSTRUCCIÓN", ["Concreto", "Bahareque", "Madera", "Otras"], 0)
crear_bloque("INST. ELÉCTRICAS", ["Canalizadas", "Externas", "Mixtas"], 1)
crear_bloque("ALMACENAMIENTO", ["Bueno", "Regular", "Malo", "Ventilación"], 2)
crear_bloque("ORDEN Y ASEO", ["Bueno", "Regular", "Malas"], 3)

# --- SECCIÓN: RIESGOS Y MATERIAL COMBUSTIBLE ---
f_riesgos = ctk.CTkFrame(main_frame)
f_riesgos.pack(fill="x", padx=10, pady=10)

# Riesgos de Incendio (Columna Izquierda)
c_izq = ctk.CTkFrame(f_riesgos, fg_color="transparent")
c_izq.grid(row=0, column=0, padx=20, sticky="n")
ctk.CTkLabel(c_izq, text="RIESGOS DE INCENDIO", font=("Arial", 12, "bold")).pack()
riesgos_lista = ["Veladoras", "Ins. Eléctricas", "Tablero breaker", "Tomacorrientes", "Cables Eléctricos", "Llamas", "Brasas", "Fumadores", "Basuras"]
for ri in riesgos_lista:
    f_ri = ctk.CTkFrame(c_izq, fg_color="transparent")
    f_ri.pack(fill="x")
    ctk.CTkLabel(f_ri, text=ri).pack(side="left")
    sb = ctk.CTkSegmentedButton(f_ri, values=["SÍ", "NO"], width=70)
    sb.pack(side="right", pady=1)
    segs[f"riesgo_{ri}"] = sb

# Material Combustible (Columna Derecha - Tabla)
c_der = ctk.CTkFrame(f_riesgos, fg_color="transparent")
c_der.grid(row=0, column=1, padx=20, sticky="n")
ctk.CTkLabel(c_der, text="MATERIAL COMBUSTIBLE", font=("Arial", 12, "bold")).pack()
for mat in ["Gas GLP", "Gas Natural", "Líquidos Inflam.", "Papel", "Madera", "Equipos Eléctricos", "Otros"]:
    f_mat = ctk.CTkFrame(c_der, fg_color="transparent")
    f_mat.pack(fill="x", pady=1)
    ctk.CTkLabel(f_mat, text=mat, width=120, anchor="w").pack(side="left")
    qty = ctk.CTkEntry(f_mat, placeholder_text="Cantidad", width=80); qty.pack(side="left", padx=2)
    desc = ctk.CTkEntry(f_mat, placeholder_text="Descripción", width=150); desc.pack(side="left")
    materials.append((mat, qty, desc))

# --- SECCIÓN: PROTECCIÓN Y SEGURIDAD HUMANA ---
f_prot = ctk.CTkFrame(main_frame)
f_prot.pack(fill="x", padx=10, pady=10)

# Carga Calórica
l_carga = ctk.CTkFrame(f_prot, fg_color="transparent")
l_carga.pack(fill="x", padx=10)
ctk.CTkLabel(l_carga, text="Carga Calórica:", font=("Arial", 11, "bold")).pack(side="left")
checks['carga_alta'] = ctk.CTkCheckBox(l_carga, text="Alta"); checks['carga_alta'].pack(side="left", padx=10)
checks['carga_media'] = ctk.CTkCheckBox(l_carga, text="Media"); checks['carga_media'].pack(side="left", padx=10)
checks['carga_baja'] = ctk.CTkCheckBox(l_carga, text="Baja"); checks['carga_baja'].pack(side="left", padx=10)

# Seguridad Humana (Tabla de estados)
ctk.CTkLabel(f_prot, text="SEGURIDAD HUMANA Y MATERIALES PELIGROSOS", font=("Arial", 12, "bold")).pack(pady=10)
items_sh = ["Salida de Emergencia", "Iluminación Emergencia", "Señalización", "Plan de Emergencias", "Extintores PQS/CO2", "Detector Humo/Temp"]
for ish in items_sh:
    f_sh = ctk.CTkFrame(f_prot, fg_color="transparent")
    f_sh.pack(fill="x", padx=100)
    ctk.CTkLabel(f_sh, text=ish, width=250, anchor="w").pack(side="left")
    seg = ctk.CTkSegmentedButton(f_sh, values=["Bueno", "Regular", "Malo"])
    seg.pack(side="right", pady=2)
    segs[f"sh_{ish}"] = seg

# --- SECCIÓN: RECOMENDACIONES (Campo Legal Obligatorio) ---
ctk.CTkLabel(main_frame, text="RECOMENDACIONES:", font=("Arial", 12, "bold"), text_color="orange").pack(pady=(20,0))
txt_recom = ctk.CTkTextbox(main_frame, width=1000, height=150)
txt_recom.pack(pady=10)

# --- SECCIÓN: VISTO BUENO Y RE-INSPECCIÓN ---
f_final = ctk.CTkFrame(main_frame)
f_final.pack(fill="x", padx=10, pady=10)

ctk.CTkLabel(f_final, text="CUMPLE CON LOS REQUISITOS PARA EL VISTO BUENO:").pack(side="left", padx=10)
segs['visto_bueno'] = ctk.CTkSegmentedButton(f_final, values=["SÍ", "NO"]); segs['visto_bueno'].pack(side="left")

# Re-inspección
f_re = ctk.CTkFrame(main_frame, fg_color="transparent")
f_re.pack(fill="x", padx=10)
ctk.CTkLabel(f_re, text="Re-inspección para el: Día").pack(side="left")
entries['re_dia'] = ctk.CTkEntry(f_re, width=40); entries['re_dia'].pack(side="left", padx=2)
ctk.CTkLabel(f_re, text="Mes").pack(side="left")
entries['re_mes'] = ctk.CTkEntry(f_re, width=40); entries['re_mes'].pack(side="left", padx=2)
ctk.CTkLabel(f_re, text="Año").pack(side="left")
entries['re_anio'] = ctk.CTkEntry(f_re, width=60); entries['re_anio'].pack(side="left", padx=2)

# Botón de guardar tras la sección de re-inspección
# Se crea más abajo, una vez definida la función save_to_excel

def gather_data():
    data = {}
    # simple entries
    for k,e in entries.items():
        try:
            data[k] = e.get()
        except Exception:
            data[k] = ''
    # segmented
    for k,s in segs.items():
        try:
            data[k] = s.get()
        except Exception:
            data[k] = ''
    # checks
    for k,c in checks.items():
        try:
            data[k] = bool(c.get())
        except Exception:
            data[k] = False
    # materials
    for mat, qty, desc in materials:
        data[f"mat_{mat}_cantidad"] = qty.get()
        data[f"mat_{mat}_descripcion"] = desc.get()
    # recomendaciones
    try:
        data['recomendaciones'] = txt_recom.get("0.0", "end").strip()
    except Exception:
        data['recomendaciones'] = ''
    return data

def save_to_excel():
    def choose_save_path(base_name):
        if not os.path.exists(base_name):
            return base_name
        try:
            with open(base_name, 'a'):
                pass
            return base_name
        except PermissionError:
            fallback = os.path.join(
                os.path.expanduser('~'),
                f"acta_inspeccion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            return fallback

    data = gather_data()
    df = pd.DataFrame([data])
    fn = 'acta_inspeccion.xlsx'
    save_path = choose_save_path(fn)
    try:
        if os.path.exists(save_path):
            existing = pd.read_excel(save_path)
            out = pd.concat([existing, df], ignore_index=True)
            out.to_excel(save_path, index=False)
        else:
            df.to_excel(save_path, index=False)
        message = f'Acta guardada en {save_path}'
        if save_path != fn:
            message += '\nEl archivo original estaba bloqueado o no tenía permisos de escritura, por lo que se guardó aquí.'
        messagebox.showinfo('Éxito', message)
    except PermissionError:
        messagebox.showerror(
            'Error',
            f'No se pudo guardar: permiso denegado al escribir en {save_path}. Cierra acta_inspeccion.xlsx si está abierto o usa otra carpeta.'
        )
    except Exception as ex:
        messagebox.showerror(
            'Error',
            f'No se pudo guardar: {ex}\nAsegúrate de tener permisos de escritura y cierra acta_inspeccion.xlsx si está abierto.'
        )

# Botón de guardar tras la sección de re-inspección
ctk.CTkButton(main_frame, text="GENERAR / GUARDAR ACTA", fg_color="#007a2f", font=("Arial", 16, "bold"), height=60, command=save_to_excel).pack(pady=(15, 30))

app.mainloop()