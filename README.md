# Business Intelligence - Masan Marketing Analysis

Du an xay dung he thong BI phan tich hieu qua marketing va doanh thu ban le cua Masan.

## Thanh phan chinh

- `masan_case.xlsx`: du lieu nguon.
- `import_excel_to_postgres.py`: import du lieu Excel vao PostgreSQL staging.
- `sql-marketing.sql`: tao schema `dw`, cac bang dimension va fact.
- `py-marketing.py`: ETL tu staging sang data warehouse.
- `pbi-marketing.pbix`: dashboard Power BI.
- `data/`: du lieu export tu cac visual Power BI de doi chieu so lieu bao cao.
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
psql -d <database_name> -f sql-marketing.sql
```

3. Import Excel vao staging:

```powershell
python import_excel_to_postgres.py --replace
```

4. Chay ETL vao schema `dw`:

```powershell
python py-marketing.py
```

5. Mo `pbi-marketing.pbix` bang Power BI Desktop va refresh du lieu.

## Luu y bao mat

File `.env` chua thong tin ket noi database va khong duoc dua len GitHub.
