from flask import Flask, request, render_template
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- Load model HuggingFace ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Load database từ JSON ---
with open("../data/embeddings/luat_lao_dong_embeddings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

# --- Hàm tìm kiếm ---
def search_law(query: str, top_k: int = 3, threshold: float = 0.3):
    query_vec = model.encode(query).reshape(1, -1)
    corpus_embeddings = np.array([d["embedding"] for d in db])
    sims = cosine_similarity(query_vec, corpus_embeddings)[0]

    # Lấy top_k điều gần nhất
    top_idx = sims.argsort()[-top_k:][::-1]

    results = []
    for idx in top_idx:
        if sims[idx] >= threshold:
            results.append({
                "id": db[idx]["id"],
                "score": float(sims[idx]),
                "text": db[idx]["text"]
            })
    return results


# --- Flask app ---
app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    if request.method == "POST":
        query = request.form["query"]
        results = search_law(query, top_k=2)
    return render_template("home.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
