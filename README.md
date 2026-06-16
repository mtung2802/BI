# Business Intelligence - Masan Marketing Analysis

Du an xay dung he thong BI phan tich hieu qua marketing va doanh thu ban le cua Masan.

## Thanh phan chinh

- `dataset/masan_case.xlsx`: du lieu nguon.
- `etl/import_excel_to_postgres.py`: import du lieu Excel vao PostgreSQL staging.
- `sql/sql-marketing.sql`: tao schema `dw`, cac bang dimension va fact.
- `etl/py-marketing.py`: ETL tu staging sang data warehouse.
- `dashboard/pbi-marketing.pbix`: dashboard Power BI.
- `report/Bao cao.pdf`: bao cao cuoi ky.
- `requirements-marketing.txt`: cac thu vien Python can cai dat.

## Cong nghe su dung

- PostgreSQL
- Python
- pandas
- psycopg2
- Power BI

## Cai dat thu vien

```powershell
pip install -r requirements-marketing.txt
```

## Quy trinh chay

1. Tao database PostgreSQL va cau hinh thong tin ket noi trong file `.env`.
2. Tao data warehouse:

```powershell
psql -d <database_name> -f sql/sql-marketing.sql
```

3. Import Excel vao staging:

```powershell
python etl/import_excel_to_postgres.py --replace
```

4. Chay ETL vao schema `dw`:

```powershell
python etl/py-marketing.py
```

5. Mo `dashboard/pbi-marketing.pbix` bang Power BI Desktop va refresh du lieu.

## Luu y bao mat

File `.env` chua thong tin ket noi database va khong duoc dua len GitHub.
