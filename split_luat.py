"""
Module tách văn bản luật thành nhiều file nhỏ, mỗi file là một Điều luật.
Cách dùng:
    python split_luat.py luat_lao_dong.pdf
"""

import re #thư viện xử lý biểu thức chính quy, tìm kiếm, thay thế và tách chuỗi
import sys #thư viện hệ thống, xử lý tham số dòng lệnh
from pathlib import Path #thư viện xử lý đường dẫn tệp và thư mục
import PyPDF2 #thư viện đọc file PDF


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Đọc text từ file PDF"""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            t = page.extract_text() or ""
            text += t + "\n"
    return text


def split_law_by_articles(text: str):
    """Tách văn bản thành danh sách các điều luật"""
    # Chuẩn hóa dòng
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    norm_text = "\n".join(lines)

    # Regex: "Điều X. Tên điều"
    pattern = re.compile(r"(Điều\s*\d+\.\s+[.]*)", flags=re.UNICODE)

    matches = list(pattern.finditer(norm_text))
    print(f"Đã tìm thấy {len(matches)} điều luật.")

    dieu_list = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(norm_text)
        chunk = norm_text[start:end].strip()
        dieu_list.append(chunk)

    return dieu_list

def save_articles(dieu_list, out_dir: Path):
    """Lưu từng điều ra file .txt"""
    out_dir.mkdir(exist_ok=True)
    for idx, chunk in enumerate(dieu_list, start=1):
        filename = out_dir / f"Dieu_{idx:03d}.txt"
        filename.write_text(chunk, encoding="utf-8")
    print(f"Đã lưu {len(dieu_list)} file vào thư mục {out_dir}")

def run(pdf_file: str):
    pdf_path = Path(pdf_file)
    text = extract_text_from_pdf(pdf_path)
    dieu_list = split_law_by_articles(text)
    out_dir = Path("../data/luat_lao_dong_dieu") 
    save_articles(dieu_list, out_dir)
    return dieu_list


def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python split_luat.py <file_pdf>")
        return

    pdf_path = Path(sys.argv[1])
    text = extract_text_from_pdf(pdf_path)
    dieu_list = split_law_by_articles(text)
    save_articles(dieu_list, pdf_path.with_suffix("").name + "_dieu")


if __name__ == "__main__":
    main()