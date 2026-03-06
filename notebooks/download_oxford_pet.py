#!/usr/bin/env python3
"""
Script para descargar el Oxford-IIIT Pet Dataset
"""
import os
import urllib.request
from tqdm import tqdm

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_file(url, output_path):
    """Descarga un archivo con barra de progreso"""
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=os.path.basename(output_path)) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def main():
    print("=" * 70)
    print("DESCARGA DEL OXFORD-IIIT PET DATASET")
    print("=" * 70)
    print()
    
    # URLs directas (sin torrent)
    base_url = "https://www.robots.ox.ac.uk/~vgg/data/pets/data/"
    files = {
        'images.tar.gz': base_url + 'images.tar.gz',
        'annotations.tar.gz': base_url + 'annotations.tar.gz'
    }
    
    # Crear carpeta de destino (relativa a data/)
    output_dir = '../data/oxford-iiit-pet'
    os.makedirs(output_dir, exist_ok=True)
    
    for filename, url in files.items():
        output_path = os.path.join(output_dir, filename)
        
        # Verificar si ya existe
        if os.path.exists(output_path):
            print(f"✓ {filename} ya existe, saltando...")
            continue
        
        print(f"Descargando {filename}...")
        try:
            download_file(url, output_path)
            print(f"✓ {filename} descargado exitosamente")
        except Exception as e:
            print(f"✗ Error descargando {filename}: {e}")
    
    print()
    print("=" * 70)
    print("DESCARGA COMPLETA")
    print("=" * 70)
    print(f"\nArchivos guardados en: {os.path.abspath(output_dir)}")
    print("\nPara extraer los archivos:")
    print("  tar -xzf ../data/oxford-iiit-pet/images.tar.gz -C ../data/oxford-iiit-pet/")
    print("  tar -xzf ../data/oxford-iiit-pet/annotations.tar.gz -C ../data/oxford-iiit-pet/")

if __name__ == '__main__':
    main()
