"""
Módulo para carga eficiente de datos de exoplanetas desde CSV
"""
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any

class ExoplanetDataLoader:
    """
    Carga y preprocesa los datos del archivo CSV de la NASA
    Optimizado para minimizar el tiempo de inicio de la aplicación
    """
    
    # Mapeo de columnas del proyecto a columnas reales del CSV
    COLUMN_MAPPING = {
        'pl_name': 'pl_name',           # Nombre del planeta
        'pl_hostname': 'hostname',      # Estrella anfitriona
        'pl_discyear': 'disc_year',     # Año de descubrimiento
        'pl_discmethod': 'discoverymethod',  # Método de descubrimiento
        'pl_discfacility': 'disc_facility'   # Instalación de descubrimiento
    }
    
    def __init__(self, file_path: Optional[str] = None):
        if file_path is None:
            project_root = Path(__file__).parent.parent
            file_path = project_root / "data" / "exoplanets.csv"
        
        self.file_path = Path(file_path)
        self.df: Optional[pd.DataFrame] = None
        self.loading_time: float = 0
        
    def load_data(self) -> pd.DataFrame:
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"❌ Archivo no encontrado: {self.file_path}\n"
                f"💡 Ejecuta 'python download_data.py' primero."
            )
        
        print(f"📂 Cargando datos desde: {self.file_path}")
        print("⏳ Optimizando carga...")
        
        try:
            import time
            start_time = time.time()
            
            # Obtener columnas reales del CSV
            df_sample = pd.read_csv(self.file_path, nrows=1)
            available_cols = df_sample.columns.tolist()
            
            # Verificar qué columnas existen
            cols_to_load = []
            for target_col, real_col in self.COLUMN_MAPPING.items():
                if real_col in available_cols:
                    cols_to_load.append(real_col)
                else:
                    print(f"⚠️  Advertencia: Columna '{real_col}' no encontrada para '{target_col}'")
            
            if not cols_to_load:
                raise ValueError(
                    f"❌ No se encontraron columnas requeridas.\n"
                    f"Columnas disponibles: {', '.join(available_cols[:10])}..."
                )
            
            print(f"📊 Columnas a cargar: {', '.join(cols_to_load)}")
            
            # Definir tipos de datos optimizados
            dtype_map = {}
            for col in cols_to_load:
                if col == 'disc_year':  # Solo esta columna es numérica
                    dtype_map[col] = 'Int64'
                else:  # El resto son strings
                    dtype_map[col] = 'string'
            
            # Cargar los datos
            self.df = pd.read_csv(
                self.file_path,
                usecols=cols_to_load,
                dtype=dtype_map,
                low_memory=False,
                encoding='utf-8'
            )
            
            # Renombrar columnas a los nombres estándar del proyecto
            rename_map = {v: k for k, v in self.COLUMN_MAPPING.items() if v in self.df.columns}
            self.df = self.df.rename(columns=rename_map)
            
            # Limpieza de datos
            initial_count = len(self.df)
            
            # Eliminar filas sin nombre de planeta
            if 'pl_name' in self.df.columns:
                self.df = self.df.dropna(subset=['pl_name'])
            
            # Eliminar filas sin nombre de estrella
            if 'pl_hostname' in self.df.columns:
                self.df = self.df.dropna(subset=['pl_hostname'])
            
            # Convertir año a entero
            if 'pl_discyear' in self.df.columns:
                self.df['pl_discyear'] = pd.to_numeric(
                    self.df['pl_discyear'],
                    errors='coerce'
                ).astype('Int64')
            
            self.loading_time = time.time() - start_time
            final_count = len(self.df)
            
            print(f"\n✅ Datos cargados exitosamente!")
            print(f"📊 Total de exoplanetas: {final_count:,}")
            print(f"⏱️  Tiempo de carga: {self.loading_time:.2f} segundos")
            print(f"📋 Columnas finales: {', '.join(self.df.columns)}")
            
            return self.df
            
        except Exception as e:
            raise Exception(f"❌ Error al cargar los datos: {str(e)}")
    
    def get_unique_values(self, column: str) -> List[str]:
        if self.df is None or column not in self.df.columns:
            return []
        
        unique_vals = self.df[column].dropna().unique().tolist()
        unique_vals = [str(val) for val in unique_vals if pd.notna(val)]
        
        try:
            numeric_vals = []
            text_vals = []
            for val in unique_vals:
                try:
                    numeric_vals.append(float(val))
                except (ValueError, TypeError):
                    text_vals.append(val)
            
            numeric_vals.sort()
            text_vals.sort()
            result = [str(v) for v in numeric_vals] + text_vals
            return result
        except:
            return sorted(unique_vals)
    
    def get_columns(self) -> List[str]:
        return self.df.columns.tolist() if self.df is not None else []
    
    def get_info(self) -> Dict[str, Any]:
        if self.df is None:
            return {}
        
        info = {
            'total_records': len(self.df),
            'columns': self.df.columns.tolist(),
            'loading_time': self.loading_time,
            'memory_usage': self.df.memory_usage(deep=True).sum() / (1024 * 1024),
        }
        
        if 'pl_discyear' in self.df.columns:
            info['years_range'] = {
                'min': int(self.df['pl_discyear'].min()),
                'max': int(self.df['pl_discyear'].max())
            }
        
        return info