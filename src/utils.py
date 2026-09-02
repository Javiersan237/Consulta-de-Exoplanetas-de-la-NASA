"""
Utilidades para el proyecto de exoplanetas
"""
import webbrowser
from typing import Optional

def generate_nasa_url(hostname: str) -> str:
    """
    Genera el URL de la página de resumen del planeta confirmado en NASA
    
    Args:
        hostname: Nombre de la estrella anfitriona
    
    Returns:
        URL completa para la página de la NASA
    """
    if not hostname or str(hostname).strip() == '':
        return "#"
    
    # Limpiar el nombre para URL
    clean_name = str(hostname).strip().replace(' ', '%20')
    return f"https://exoplanetarchive.ipac.caltech.edu/overview/{clean_name}"

def open_nasa_url(hostname: str) -> None:
    """
    Abre la página de NASA en una nueva pestaña del navegador
    
    Args:
        hostname: Nombre de la estrella anfitriona
    """
    url = generate_nasa_url(hostname)
    if url != "#":
        webbrowser.open_new_tab(url)