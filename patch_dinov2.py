import json
from pathlib import Path

NOTEBOOK = Path("notebooks/comparar_dos_imagenes_embeddings.ipynb")

DINO_CODE = """# ===== DINOv2 (ViT) como extractor de embeddings =====
# Sustituye ViT-B/16 por DINOv2. Mantengo nombres de variables (embeddings_vit, etc.)
# para que las celdas posteriores sigan funcionando.
import torchvision.transforms as T

# Recomendado: dinov2_vitb14 (mejor) o dinov2_vits14 (mas rapido)
dino_model_name = \"dinov2_vitb14\"

device = torch.device(\"cuda\" if torch.cuda.is_available() else \"cpu\")
model_vit = torch.hub.load(\"facebookresearch/dinov2\", dino_model_name)
model_vit = model_vit.to(device).eval()

# Preprocesado estilo ImageNet; DINOv2 normalmente usa 224x224
tfm_vit = T.Compose(
    [
        T.Resize(256, interpolation=T.InterpolationMode.BICUBIC),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ]
)

embeddings_vit = []
nombres_vit = []
image_paths_valid_vit = []

with torch.no_grad():
    for path in image_paths:
        try:
            img = Image.open(path).convert(\"RGB\")
            x = tfm_vit(img).unsqueeze(0).to(device)

            # Salida: (1, D). Para dinov2_vitb14, D=768.
            emb = model_vit(x).squeeze(0)
            emb = F.normalize(emb, dim=0)

            embeddings_vit.append(emb.detach().cpu().numpy())
            nombres_vit.append(file_meta_by_name.get(path.name, path.name))
            image_paths_valid_vit.append(path)
        except Exception:
            continue

if len(embeddings_vit) < 2:
    raise ValueError(\"Se requieren al menos 2 imagenes validas para comparar con DINOv2.\")

embeddings_vit = np.stack(embeddings_vit, axis=0)  # (N, D)
print(f\"DINOv2 ({dino_model_name}) embeddings extraidos:\", embeddings_vit.shape)
print(\"Imagenes validas DINOv2:\", len(image_paths_valid_vit))
"""


def normalize_source(source):
    if isinstance(source, str):
        return source
    if isinstance(source, list):
        return "\n".join(line.rstrip("\n") for line in source)
    return ""


def main():
    nb_path = NOTEBOOK
    if not nb_path.exists():
        raise SystemExit(f"Notebook no encontrado: {nb_path}")

    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    patched = 0

    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = normalize_source(cell.get("source", ""))

        # Detecta la celda de ViT-B/16 por imports/pesos
        if "from torchvision.models import vit_b_16" in src and "ViT_B_16_Weights" in src:
            cell["source"] = [line + "\n" for line in DINO_CODE.splitlines()]
            patched += 1

    if patched == 0:
        raise SystemExit("No se encontro ninguna celda ViT-B/16 para reemplazar.")

    nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Patched cells: {patched}")


if __name__ == "__main__":
    main()
