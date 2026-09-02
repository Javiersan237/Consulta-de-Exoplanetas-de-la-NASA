"""
Motor de búsqueda y filtrado de exoplanetas
"""
import pandas as pd
from typing import Dict, Optional, List

class QueryEngine:
    """Realiza búsquedas eficientes sobre los datos de exoplanetas"""
    
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.query_columns = ['pl_discyear', 'pl_discmethod', 'pl_hostname', 'pl_discfacility']
        self.result_columns = ['pl_hostname', 'pl_discyear', 'pl_discmethod', 'pl_discfacility']
    
    def search(self, filters: Dict[str, Optional[str]]) -> pd.DataFrame:
        """
        Busca exoplanetas que coincidan con todos los filtros seleccionados
        
        Args:
            filters: Diccionario con {columna: valor} para filtrar
        
        Returns:
            DataFrame con los resultados (solo columnas de consulta)
        """
        if not filters:
            return pd.DataFrame()
        
        # Comenzar con una copia del DataFrame completo
        result = self.df.copy()
        
        # Aplicar cada filtro
        for column, value in filters.items():
            if value and column in self.df.columns:
                # Convertir valor a string para comparación consistente
                result = result[result[column].astype(str) == str(value)]
        
        # Seleccionar solo las columnas de resultado
        available_cols = [col for col in self.result_columns if col in result.columns]
        result = result[available_cols].copy()
        
        # Resetear índice para evitar problemas
        result = result.reset_index(drop=True)
        
        return result
    
    def sort_dataframe(self, df: pd.DataFrame, column: str, ascending: bool = True) -> pd.DataFrame:
        """
        Ordena un DataFrame por la columna especificada
        SIN distinguir entre mayúsculas y minúsculas para texto
        
        Args:
            df: DataFrame a ordenar
            column: Nombre de la columna
            ascending: True para ascendente, False para descendente
        
        Returns:
            DataFrame ordenado
        """
        if df.empty or column not in df.columns:
            return df
        
        # Crear una copia para no modificar el original
        sorted_df = df.copy()
        
        # Verificar si la columna es de tipo string (texto)
        if pd.api.types.is_string_dtype(sorted_df[column]) or sorted_df[column].dtype == 'object':
            # Crear una columna temporal con el texto en minúsculas para ordenar
            sorted_df['_sort_key'] = sorted_df[column].astype(str).str.lower()
            
            # Ordenar usando la columna temporal
            sorted_df = sorted_df.sort_values(
                by='_sort_key', 
                ascending=ascending, 
                na_position='last'
            )
            
            # Eliminar la columna temporal
            sorted_df = sorted_df.drop(columns=['_sort_key'])
        else:
            # Para columnas numéricas, ordenar normalmente
            sorted_df = sorted_df.sort_values(
                by=column, 
                ascending=ascending, 
                na_position='last'
            )
        
        return sorted_df.reset_index(drop=True)
    
    def get_query_options(self) -> Dict[str, List[str]]:
        """
        Obtiene todas las opciones para los menús desplegables
        """
        options = {}
        for col in self.query_columns:
            if col in self.df.columns:
                # Obtener valores únicos no nulos
                values = self.df[col].dropna().unique().tolist()
                # Convertir a string y ordenar
                values = sorted([str(v) for v in values if pd.notna(v)])
                options[col] = values
        return options
    
    def get_total_count(self) -> int:
        """Retorna el número total de exoplanetas"""
        return len(self.df) if self.df is not None else 0