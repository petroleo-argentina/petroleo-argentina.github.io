import duckdb
con = duckdb.connect()
print(con.execute("DESCRIBE SELECT * FROM read_csv_auto('data/raw/energia/serie-produccion-petroleo-total-pais-desde-1950.csv')").fetchall())
print(con.execute("SELECT * FROM read_csv_auto('data/raw/energia/serie-produccion-petroleo-total-pais-desde-1950.csv') ORDER BY 1 DESC LIMIT 10").df())
