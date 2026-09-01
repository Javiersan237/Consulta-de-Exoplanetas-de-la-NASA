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
        """Busca exoplanetas que coincidan con todos los filtros seleccionados"""
        if not filters:
            return pd.DataFrame()
        
        result = self.df.copy()
        
        for column, value in filters.items():
            if value and column in self.df.columns:
                result = result[result[column].astype(str) == str(value)]
        
        available_cols = [col for col in self.result_columns if col in result.columns]
        result = result[available_cols].copy()
        result = result.reset_index(drop=True)
        
        return result
    
    def sort_dataframe(self, df: pd.DataFrame, column: str, ascending: bool = True) -> pd.DataFrame:
        """Ordena un DataFrame por la columna especificada"""
        if df.empty or column not in df.columns:
            return df
        
        return df.sort_values(by=column, ascending=ascending, na_position='last')
    
    def get_query_options(self) -> Dict[str, List[str]]:
        """Obtiene todas las opciones para los menús desplegables"""
        options = {}
        for col in self.query_columns:
            if col in self.df.columns:
                values = self.df[col].dropna().unique().tolist()
                # Convertir a string y ordenar (numérico primero)
                try:
                    numeric_vals = []
                    text_vals = []
                    for v in values:
                        try:
                            numeric_vals.append(float(v))
                        except (ValueError, TypeError):
                            text_vals.append(str(v))
                    numeric_vals.sort()
                    text_vals.sort()
                    result = [str(int(v)) if v.is_integer() else str(v) for v in numeric_vals] + text_vals
                    options[col] = result
                except:
                    options[col] = sorted([str(v) for v in values if pd.notna(v)])
        return options
    
    def get_total_count(self) -> int:
        """Retorna el número total de exoplanetas"""
        return len(self.df) if self.df is not None else 0