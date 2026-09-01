"""
Interfaz gráfica para el Consultor de Exoplanetas de la NASA
Con colores oficiales de la NASA y temática espacial
"""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from data_loader import ExoplanetDataLoader
from query_engine import QueryEngine

class ExoplanetApp:
    """Aplicación principal de consulta de exoplanetas"""
    
    COLORS = {
        'nasa_blue': '#0B3D91',
        'nasa_red': '#FC3D21',
        'nasa_white': '#FFFFFF',
        'nasa_light_blue': '#4A8FE4',
        'bg_primary': '#0B0B1A',
        'bg_secondary': '#1A1A3A',
        'bg_combobox': '#0D1B2A',
        'bg_panel': '#2C1A4D',               # Fondo morado para paneles
        'text_primary': '#FFFFFF',
        'text_secondary': '#A0C4E8',
        'border_color': '#4A8FE4',
        'border_panel': '#A78BFA',           # Borde morado claro
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("🪐 NASA Exoplanet Explorer")
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        
        self.center_window()
        
        self.data_loader = None
        self.query_engine = None
        self.bg_image = None
        self.bg_canvas = None
        
        self.setup_styles()
        self.setup_background()
        self.create_widgets()
        self.load_data()
    
    def center_window(self):
        self.root.update_idletasks()
        width = 1100
        height = 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        self.root.configure(bg=self.COLORS['bg_primary'])
        
        style.configure(
            'NASA.TFrame',
            background=self.COLORS['bg_secondary'],
            relief='flat'
        )
        
        # ------------------- PANEL CON BORDE ALINEADO -------------------
        style.configure(
            'NASA.TLabelframe',
            background=self.COLORS['bg_panel'],      # Fondo morado
            foreground=self.COLORS['text_primary'],
            relief='solid',
            borderwidth=3,                           # Borde más delgado
            bordercolor=self.COLORS['border_panel']
        )
        
        # Título alineado con el borde superior
        style.configure(
            'NASA.TLabelframe.Label',
            background=self.COLORS['bg_panel'],      # Mismo fondo morado
            foreground='#FFFFFF',
            font=('Helvetica', 12, 'bold'),
            relief='flat',
            borderwidth=0,
            padding=(8, 1)                           # padding vertical mínimo
        )
        # -------------------------------------------------------------
        
        style.configure(
            'NASA.TLabel',
            background=self.COLORS['bg_panel'],
            foreground=self.COLORS['text_primary'],
            font=('Helvetica', 10)
        )
        
        style.configure(
            'NASA.TCombobox',
            background=self.COLORS['bg_combobox'],
            foreground='#FFFFFF',
            fieldbackground=self.COLORS['bg_combobox'],
            selectbackground=self.COLORS['nasa_blue'],
            selectforeground='white',
            borderwidth=2,
            relief='solid',
            bordercolor=self.COLORS['border_color']
        )
        style.map(
            'NASA.TCombobox',
            fieldbackground=[('readonly', self.COLORS['bg_combobox'])],
            background=[('active', self.COLORS['nasa_blue'])],
            foreground=[('active', '#FFFFFF')]
        )
        
        style.configure(
            'Status.TLabel',
            background=self.COLORS['bg_primary'],
            foreground=self.COLORS['text_secondary'],
            font=('Helvetica', 9, 'italic')
        )
    
    def setup_background(self):
        from PIL import Image, ImageTk
        
        imagen_path = Path(__file__).parent.parent / "images" / "Imagen_Fondo_NASA.png"
        
        if not imagen_path.exists():
            print("❌ Imagen no encontrada")
            return
        
        try:
            img = Image.open(imagen_path)
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img_resized)
            
            self.bg_canvas = tk.Canvas(
                self.root,
                width=width,
                height=height,
                highlightthickness=0,
                bg=self.COLORS['bg_primary']
            )
            self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW)
            self.bg_canvas.lower()
            
            def on_resize(event):
                if hasattr(self, 'bg_canvas') and self.bg_canvas:
                    try:
                        img = Image.open(imagen_path)
                        img_resized = img.resize((event.width, event.height), Image.Resampling.LANCZOS)
                        self.bg_image = ImageTk.PhotoImage(img_resized)
                        self.bg_canvas.delete("all")
                        self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW)
                        self.bg_canvas.config(width=event.width, height=event.height)
                        self.bg_canvas.lower()
                    except Exception as e:
                        print(f"⚠️ Error al redimensionar: {e}")
            
            self.root.bind('<Configure>', on_resize)
            
        except Exception as e:
            print(f"❌ Error al cargar la imagen: {e}")
    
    def create_widgets(self):
        main_container = tk.Frame(self.root, bg='')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        center_frame = tk.Frame(main_container, bg='')
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.create_query_panel(center_frame)
        self.create_results_panel(center_frame)
    
    def create_query_panel(self, parent):
        query_frame = ttk.LabelFrame(
            parent, 
            text="🚀 PANEL DE CONSULTA", 
            style='NASA.TLabelframe',
            padding="20"
        )
        query_frame.pack(pady=(0, 15), fill=tk.X)
        
        self.query_vars = {}
        self.comboboxes = {}
        
        fields = [
            ("📅 Año de Descubrimiento", "pl_discyear", 0),
            ("🔭 Método de Descubrimiento", "pl_discmethod", 1),
            ("⭐ Estrella Anfitriona", "pl_hostname", 2),
            ("🏛️ Instalación de Descubrimiento", "pl_discfacility", 3)
        ]
        
        for label_text, col_name, row in fields:
            label = ttk.Label(
                query_frame,
                text=label_text,
                style='NASA.TLabel',
                font=('Helvetica', 10, 'bold')
            )
            label.grid(row=row, column=0, sticky=tk.W, padx=(0, 15), pady=8)
            
            var = tk.StringVar()
            self.query_vars[col_name] = var
            
            combo = ttk.Combobox(
                query_frame,
                textvariable=var,
                state="readonly",
                width=45,
                style='NASA.TCombobox',
                font=('Helvetica', 10)
            )
            combo.grid(row=row, column=1, sticky=tk.W, pady=8)
            self.comboboxes[col_name] = combo
        
        button_frame = ttk.Frame(query_frame, style='NASA.TFrame')
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        self.search_btn = tk.Button(
            button_frame,
            text="🔍 BUSCAR",
            command=self.perform_search,
            width=20,
            height=1,
            bg=self.COLORS['nasa_blue'],
            fg='white',
            font=('Helvetica', 11, 'bold'),
            relief='flat',
            padx=10,
            pady=8,
            cursor='hand2',
            activebackground=self.COLORS['nasa_light_blue'],
            activeforeground='white',
            borderwidth=0
        )
        self.search_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🧹 LIMPIAR",
            command=self.clear_all,
            width=20,
            height=1,
            bg=self.COLORS['nasa_red'],
            fg='white',
            font=('Helvetica', 11, 'bold'),
            relief='flat',
            padx=10,
            pady=8,
            cursor='hand2',
            activebackground='#FF6B4A',
            activeforeground='white',
            borderwidth=0
        )
        self.clear_btn.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(
            query_frame,
            text="🔄 Inicializando...",
            style='Status.TLabel'
        )
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
    
    def create_results_panel(self, parent):
        results_frame = ttk.LabelFrame(
            parent,
            text="📊 RESULTADOS",
            style='NASA.TLabelframe',
            padding="20"
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_label = ttk.Label(
            results_frame,
            text="🪐 Los resultados aparecerán aquí después de buscar",
            style='NASA.TLabel',
            font=('Helvetica', 14, 'italic'),
            foreground=self.COLORS['text_secondary']
        )
        self.result_label.pack(expand=True, pady=40)
    
    def load_data(self):
        try:
            self.status_label.config(text="⏳ Cargando datos desde la NASA...")
            self.root.update()
            
            data_loader = ExoplanetDataLoader()
            df = data_loader.load_data()
            
            self.data_loader = data_loader
            self.query_engine = QueryEngine(df)
            
            self.populate_comboboxes()
            
            self.status_label.config(
                text=f"✅ {len(df):,} exoplanetas cargados | Listo para explorar el universo 🚀"
            )
            
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los datos:\n\n{str(e)}")
            self.status_label.config(text="❌ Error al cargar datos")
    
    def populate_comboboxes(self):
        if self.query_engine is None:
            return
        
        options = self.query_engine.get_query_options()
        
        for col, combo in self.comboboxes.items():
            if col in options:
                values = [''] + options[col]
                combo['values'] = values
                combo.set('')
    
    def perform_search(self):
        filters = {}
        for col, var in self.query_vars.items():
            value = var.get().strip()
            if value:
                filters[col] = value
        
        if not filters:
            messagebox.showerror(
                "Error de Búsqueda",
                "❌ Debes seleccionar al menos un criterio de búsqueda."
            )
            return
        
        filtros_texto = "\n".join([f"  • {k}: {v}" for k, v in filters.items()])
        self.result_label.config(
            text=f"🔍 Búsqueda ejecutada con {len(filters)} filtro(s):\n\n{filtros_texto}\n\n🪐 (Resultados completos en el Issue #5)"
        )
        self.status_label.config(text=f"✅ Búsqueda con {len(filters)} filtro(s)")
    
    def clear_all(self):
        for var in self.query_vars.values():
            var.set('')
        
        self.result_label.config(text="🪐 Los resultados aparecerán aquí después de buscar")
        self.status_label.config(text="🧹 Panel limpiado | Listo para nueva búsqueda")

def main():
    root = tk.Tk()
    app = ExoplanetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()