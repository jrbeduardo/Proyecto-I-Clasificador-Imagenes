import json
from pathlib import Path

nb_path = Path('notebooks/comparar_dos_imagenes_embeddings.ipynb')
nb = json.loads(nb_path.read_text(encoding='utf-8'))

repls = [
    # ResNet query cell
    (
        "ax[0].set_title('Consulta')",
        "ax[0].set_title(nombres[query_idx].replace(' | ', '\\n'), fontsize=8)"
    ),
    (
        "ax[j].set_title(f'#{j}\\n{d[i]:.3f}')",
        "ax[j].set_title(f'#{j}  {d[i]:.3f}\\n' + nombres[i].replace(' | ', '\\n'), fontsize=8)"
    ),
    # ViT query cell
    (
        'ax[0].set_title("Consulta")',
        'ax[0].set_title(nombres_vit[query_idx_vit].replace(" | ", "\\n"), fontsize=8)'
    ),
    (
        'ax[j].set_title(f"#{j}\\n{d_vit[i]:.3f}")',
        'ax[j].set_title(f"#{j}  {d_vit[i]:.3f}\\n" + nombres_vit[i].replace(" | ", "\\n"), fontsize=8)'
    ),
]

changed_cells = 0
for cell in nb.get('cells', []):
    src = ''.join(cell.get('source', []))
    new_src = src
    for old, new in repls:
        new_src = new_src.replace(old, new)

    if new_src != src:
        cell['source'] = [new_src]
        changed_cells += 1

nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
print('Patched cells:', changed_cells)
