import json
with open("notebooks/comparar_dos_imagenes_embeddings.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)
for cell in nb["cells"]:
    if cell.get("id") == "140acaa8":
        src = cell["source"]
        print("TYPE:", type(src))
        if isinstance(src, list):
            full = "".join(src)
        else:
            full = src
        print("LAST 200 chars:", repr(full[-200:]))
        # Check if file_meta_by_name is referenced
        if "file_meta_by_name" in full:
            print("file_meta_by_name IS in source")
        else:
            print("file_meta_by_name NOT IN SOURCE!")
        break
