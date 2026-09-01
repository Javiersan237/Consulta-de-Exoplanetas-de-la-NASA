"""
Interfaz gráfica para el Consultor de Exoplanetas de la NASA
Con colores oficiales de la NASA y temática espacial
"""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import sys
import pandas as pd

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
        'bg_panel': '#2C1A4D',
        'text_primary': '#FFFFFF',
        'text_secondary': '#A0C4E8',
        'border_color': '#4A8FE4',
        'border_panel': '#A78BFA',
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
        self.current_results = pd.DataFrame()
        
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
        
        style.configure(
            'NASA.TLabelframe',
            background=self.COLORS['bg_panel'],
            foreground=self.COLORS['text_primary'],
            relief='solid',
            borderwidth=3,
            bordercolor=self.COLORS['border_panel']
        )
        
        style.configure(
            'NASA.TLabelframe.Label',
            background=self.COLORS['bg_panel'],
            foreground='#FFFFFF',
            font=('Helvetica', 12, 'bold'),
            relief='flat',
            borderwidth=0,
            padding=(8, 1)
        )
        
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
        
        # Estilo para la tabla (Treeview)
        style.configure(
            'NASA.Treeview',
            background='#1A1A3A',
            foreground='#FFFFFF',
            fieldbackground='#1A1A3A',
            borderwidth=1,
            relief='solid'
        )
        style.configure(
            'NASA.Treeview.Heading',
            background=self.COLORS['nasa_blue'],
            foreground='#FFFFFF',
            font=('Helvetica', 10, 'bold'),
            borderwidth=1,
            relief='solid'
        )
        style.map(
            'NASA.Treeview',
            background=[('selected', self.COLORS['nasa_light_blue'])],
            foreground=[('selected', '#FFFFFF')]
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
        """Crea el panel de resultados con tabla"""
        results_frame = ttk.LabelFrame(
            parent,
            text="📊 RESULTADOS",
            style='NASA.TLabelframe',
            padding="15"
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para la tabla y scrollbars
        table_frame = ttk.Frame(results_frame, style='NASA.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview (tabla)
        columns = ('pl_hostname', 'pl_discyear', 'pl_discmethod', 'pl_discfacility')
        column_headers = {
            'pl_hostname': '⭐ Estrella Anfitriona',
            'pl_discyear': '📅 Año',
            'pl_discmethod': '🔭 Método',
            'pl_discfacility': '🏛️ Instalación'
        }
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            style='NASA.Treeview',
            height=12
        )
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=column_headers[col])
            self.tree.column(col, width=150, anchor=tk.W, minwidth=100)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Label para cuando no hay resultados
        self.empty_label = ttk.Label(
            results_frame,
            text="🪐 Los resultados aparecerán aquí después de buscar",
            style='NASA.TLabel',
            font=('Helvetica', 14, 'italic'),
            foreground=self.COLORS['text_secondary']
        )
        self.empty_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
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
        """Ejecuta la búsqueda real y muestra los resultados"""
        # Recolectar filtros
        filters = {}
        for col, var in self.query_vars.items():
            value = var.get().strip()
            if value:
                filters[col] = value
        
        # Validar que haya al menos un filtro
        if not filters:
            messagebox.showerror(
                "Error de Búsqueda",
                "❌ Debes seleccionar al menos un criterio de búsqueda."
            )
            return
        
        try:
            self.status_label.config(text="⏳ Buscando exoplanetas...")
            self.root.update()
            
            # Ejecutar búsqueda
            results = self.query_engine.search(filters)
            self.current_results = results
            
            # Mostrar resultados
            self.display_results(results)
            
            if len(results) == 0:
                self.status_label.config(text="🔍 No se encontraron resultados")
            else:
                self.status_label.config(text=f"✅ {len(results)} resultados encontrados")
                
        except Exception as e:
            messagebox.showerror("Error de Búsqueda", f"Error al buscar:\n\n{str(e)}")
            self.status_label.config(text="❌ Error en la búsqueda")
    
    def display_results(self, results: pd.DataFrame):
        """Muestra los resultados en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ocultar/mostrar empty_label
        if results.empty:
            self.empty_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            return
        else:
            self.empty_label.place_forget()
        
        # Insertar datos
        for _, row in results.iterrows():
            values = []
            for col in ['pl_hostname', 'pl_discyear', 'pl_discmethod', 'pl_discfacility']:
                val = row.get(col, '')
                if pd.isna(val):
                    val = ''
                values.append(str(val))
            
            self.tree.insert('', 'end', values=values)
    
    def clear_all(self):
        """Limpia todas las selecciones y resultados"""
        # Limpiar comboboxes
        for var in self.query_vars.values():
            var.set('')
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Mostrar empty_label
        self.empty_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Resetear resultados
        self.current_results = pd.DataFrame()
        
        self.status_label.config(text="🧹 Panel limpiado | Listo para nueva búsqueda")

def main():
    root = tk.Tk()
    app = ExoplanetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()