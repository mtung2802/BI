import os
import sys
import io
import argparse
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Giúp CMD Windows in tiếng Việt ổn hơn.
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME"),
}

STG_SCHEMA = os.getenv("DB_SCHEMA_STAGING", "staging")
RAW_TABLE = os.getenv("RAW_TABLE", "masan_case_xlsx")


def q(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def clean_cell(value):
    if pd.isna(value):
        return None
    # Giữ ngày tháng dạng text để file py-marketing.py tự parse thống nhất.
    return str(value)


def main():
    parser = argparse.ArgumentParser(description="Import Excel Masan case vào PostgreSQL staging table")
    parser.add_argument("--excel", default=str(BASE_DIR / "masan_case.xlsx"), help="Đường dẫn file Excel")
    parser.add_argument("--sheet", default=0, help="Tên sheet hoặc số thứ tự sheet, mặc định sheet đầu tiên")
    parser.add_argument("--replace", action="store_true", help="Xóa và tạo lại bảng raw trước khi import")
    args = parser.parse_args()

    excel_path = Path(args.excel)
    if not excel_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file Excel: {excel_path}")

    missing = [k for k, v in DB_CONFIG.items() if not v]
    if missing:
        raise ValueError(f"Thiếu thông tin trong file .env: {missing}")

    # Nếu người dùng nhập --sheet 0/1 dạng số, chuyển sang int.
    sheet = args.sheet
    if isinstance(sheet, str) and sheet.isdigit():
        sheet = int(sheet)

    df = pd.read_excel(excel_path, sheet_name=sheet)
    if df.empty:
        raise ValueError("File Excel không có dữ liệu")

    # Đổi tên cột sang string và bỏ khoảng trắng đầu/cuối.
    df.columns = [str(c).strip() for c in df.columns]
    rows = [tuple(clean_cell(v) for v in row) for row in df.itertuples(index=False, name=None)]

    full_table = f"{q(STG_SCHEMA)}.{q(RAW_TABLE)}"
    col_defs = ",\n        ".join(f"{q(c)} TEXT" for c in df.columns)
    col_names = ", ".join(q(c) for c in df.columns)

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(f"CREATE SCHEMA IF NOT EXISTS {q(STG_SCHEMA)};")
            if args.replace:
                cur.execute(f"DROP TABLE IF EXISTS {full_table};")
            cur.execute(f"CREATE TABLE IF NOT EXISTS {full_table} (\n        {col_defs}\n    );")
            if args.replace:
                execute_values(cur, f"INSERT INTO {full_table} ({col_names}) VALUES %s", rows)
            else:
                # Nếu không replace, vẫn insert thêm dữ liệu vào bảng hiện có.
                execute_values(cur, f"INSERT INTO {full_table} ({col_names}) VALUES %s", rows)
        conn.commit()

    print("Import Excel vào PostgreSQL thành công")
    print(f"Schema: {STG_SCHEMA}")
    print(f"Table: {RAW_TABLE}")
    print(f"Rows inserted: {len(rows)}")
    print(f"Columns: {len(df.columns)}")


if __name__ == "__main__":
    main()
