#!/usr/bin/env python3
"""
Script para extraer información de archivos .torrent
"""
import os
import struct

def decode_bencode(data, index=0):
    """Decodifica datos bencode manualmente"""
    if data[index:index+1] == b'i':
        # Integer
        index += 1
        end = data.index(b'e', index)
        return int(data[index:end]), end + 1
    elif data[index:index+1] == b'l':
        # List
        index += 1
        result = []
        while data[index:index+1] != b'e':
            item, index = decode_bencode(data, index)
            result.append(item)
        return result, index + 1
    elif data[index:index+1] == b'd':
        # Dictionary
        index += 1
        result = {}
        while data[index:index+1] != b'e':
            key, index = decode_bencode(data, index)
            value, index = decode_bencode(data, index)
            result[key] = value
        return result, index + 1
    elif data[index:index+1].isdigit():
        # String
        colon = data.index(b':', index)
        length = int(data[index:colon])
        start = colon + 1
        end = start + length
        return data[start:end], end
    else:
        raise ValueError(f"Invalid bencode data at index {index}")

def parse_torrent(filepath):
    """Lee y parsea un archivo torrent"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    torrent_data, _ = decode_bencode(data)
    
    info = {}
    
    # Información básica
    if b'announce' in torrent_data:
        info['Tracker'] = torrent_data[b'announce'].decode('utf-8', errors='ignore')
    
    if b'creation date' in torrent_data:
        from datetime import datetime
        info['Fecha de creación'] = datetime.fromtimestamp(torrent_data[b'creation date']).strftime('%Y-%m-%d %H:%M:%S')
    
    if b'created by' in torrent_data:
        info['Creado por'] = torrent_data[b'created by'].decode('utf-8', errors='ignore')
    
    if b'comment' in torrent_data:
        info['Comentario'] = torrent_data[b'comment'].decode('utf-8', errors='ignore')
    
    # Información del contenido
    if b'info' in torrent_data:
        torrent_info = torrent_data[b'info']
        
        if b'name' in torrent_info:
            info['Nombre'] = torrent_info[b'name'].decode('utf-8', errors='ignore')
        
        if b'length' in torrent_info:
            size = torrent_info[b'length']
            info['Tamaño'] = f"{size:,} bytes ({size / (1024**3):.2f} GB)"
        elif b'files' in torrent_info:
            total_size = sum(f[b'length'] for f in torrent_info[b'files'])
            num_files = len(torrent_info[b'files'])
            info['Número de archivos'] = num_files
            info['Tamaño total'] = f"{total_size:,} bytes ({total_size / (1024**3):.2f} GB)"
            
            # Listar primeros archivos
            info['Archivos'] = []
            for file_info in torrent_info[b'files'][:10]:  # Mostrar primeros 10
                path_parts = [p.decode('utf-8', errors='ignore') for p in file_info[b'path']]
                filepath = '/'.join(path_parts)
                size = file_info[b'length']
                info['Archivos'].append(f"{filepath} ({size:,} bytes)")
        
        if b'piece length' in torrent_info:
            info['Tamaño de pieza'] = f"{torrent_info[b'piece length']:,} bytes"
    
    return info

if __name__ == '__main__':
    torrent_file = '../data/oxford-iiit-pet-b18bbd9ba03d50b0f7f479acc9f4228a408cecc1.torrent'
    
    print("=" * 70)
    print("INFORMACIÓN DEL ARCHIVO TORRENT")
    print("=" * 70)
    print()
    
    try:
        info = parse_torrent(torrent_file)
        
        for key, value in info.items():
            if key == 'Archivos':
                print(f"\n{key}:")
                for i, file in enumerate(value, 1):
                    print(f"  {i}. {file}")
            else:
                print(f"{key}: {value}")
        
        print("\n" + "=" * 70)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        import traceback
        traceback.print_exc()
