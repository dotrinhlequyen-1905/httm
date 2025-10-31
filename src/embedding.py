import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

# --- B1: Load model HuggingFace ---
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 chiều

# --- B2: Đọc các file txt trong thư mục ---
dieu_dir = Path("../data/luat_lao_dong_dieu")   # thư mục chứa Dieu_001.txt, Dieu_002.txt...
files = sorted(dieu_dir.glob("Dieu_*.txt"))

dieu_list = []
for i, file in enumerate(files, start=1):
    text = file.read_text(encoding="utf-8").strip()
    dieu_list.append({"id": i, "text": text})

print(f"Đã đọc {len(dieu_list)} điều luật")

# --- B3: Tính embedding ---
for d in dieu_list:
    d["embedding"] = model.encode(d["text"]).tolist()

# --- B4: Lưu ra JSON ---
embeddings_dir = Path("../data/embeddings")
embeddings_dir.mkdir(parents=True, exist_ok=True)
out_file = embeddings_dir / "luat_lao_dong_embeddings.json"
out_file.write_text(json.dumps(dieu_list, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"✅ Đã lưu {len(dieu_list)} embeddings vào {out_file}")

