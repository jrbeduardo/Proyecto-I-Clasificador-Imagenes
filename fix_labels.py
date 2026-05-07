import json

with open("notebooks/comparar_dos_imagenes_embeddings.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

fixed = 0
for cell in nb["cells"]:
    if cell.get("id") == "140acaa8":
        src = "".join(cell["source"])
        new_src = src.replace(
            "nombres.append(path.name)",
            "nombres.append(file_meta_by_name.get(path.name, path.name))"
        )
        if new_src != src:
            cell["source"] = [new_src]
            fixed += 1
            print("RESNET: fixed")
        else:
            print("RESNET: already fixed or pattern not found")
            print("  snippet:", repr(src[src.find("nombres.append"):src.find("nombres.append")+60]))

    if cell.get("id") == "f12cb6d4":
        src = "".join(cell["source"])
        new_src = src.replace(
            "nombres_vit.append(path.name)",
            "nombres_vit.append(file_meta_by_name.get(path.name, path.name))"
        )
        if new_src != src:
            cell["source"] = [new_src]
            fixed += 1
            print("VIT: fixed")
        else:
            print("VIT: already fixed or pattern not found")
            print("  snippet:", repr(src[src.find("nombres_vit.append"):src.find("nombres_vit.append")+70]))

print(f"Total cells fixed: {fixed}")

with open("notebooks/comparar_dos_imagenes_embeddings.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Saved.")
