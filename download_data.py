"""
Script para descargar automáticamente los datos de exoplanetas de la NASA
"""
import urllib.request
import sys
from pathlib import Path

def download_exoplanet_data():
    """
    Descarga el archivo CSV del NASA Exoplanet Archive
    """
    print("🚀 Descargando datos de exoplanetas de la NASA...")
    print("=" * 50)
    
    # URL del archivo (PS = Planetary Systems)
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+ps&format=csv"
    
    # Crear directorio data si no existe
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Ruta del archivo
    file_path = data_dir / "exoplanets.csv"
    
    try:
        print(f"📥 Descargando desde: {url[:80]}...")
        print(f"📁 Guardando en: {file_path}")
        print("\n⏳ Descargando... (esto puede tomar unos segundos)")
        
        # Barra de progreso
        def report_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, int(downloaded * 100 / total_size)) if total_size > 0 else 0
            bar = "█" * (percent // 2) + "░" * (50 - percent // 2)
            print(f"\r📥 [{bar}] {percent}% completado", end="")
        
        # Descargar
        urllib.request.urlretrieve(url, file_path, report_progress)
        print("\n")
        
        # Verificar que el archivo se creó
        if file_path.exists():
            size = file_path.stat().st_size / (1024 * 1024)
            print(f"✅ ¡Descarga completada exitosamente!")
            print(f"📊 Tamaño del archivo: {size:.2f} MB")
            print(f"📁 Ubicación: {file_path}")
            
            # Mostrar primeras líneas
            print("\n📋 Vista previa del archivo:")
            print("-" * 50)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:3]
                for i, line in enumerate(lines):
                    if i == 0:
                        print("Columnas:", line.strip()[:100] + "..." if len(line) > 100 else line.strip())
                    else:
                        print("Datos:  ", line.strip()[:100] + "..." if len(line) > 100 else line.strip())
            print("-" * 50)
            
            print("\n✅ Issue #1 completado: Datos descargados correctamente")
            
        else:
            print("❌ Error: El archivo no se creó correctamente")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n💡 También puedes descargar manualmente desde:")
        print("   https://exoplanetarchive.ipac.caltech.edu/")
        sys.exit(1)

if __name__ == "__main__":
    download_exoplanet_data()