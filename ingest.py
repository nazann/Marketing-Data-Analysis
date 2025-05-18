import os
import pandas as pd
from sqlalchemy import create_engine, text

# PostgreSQL connection
passw = os.getenv('PASSWORD')
user=os.getenv('USER')

engine = create_engine(f"postgresql://{user}:{passw}@localhost:5433/Marketing_Analytics")

DATA_FOLDER = "./data"

def parse_column_file(column_file):
    df = pd.read_csv(column_file)
    col_defs = []
    for _, row in df.iterrows():
        name = row["name"]
        dtype = row["type"]
        length = int(row["length"])

        if dtype.upper() == "INTEGER":
            col_type = "INTEGER"
        elif dtype.upper() == "STRING":
            col_type = f"VARCHAR({length})"
        else:
            col_type = "TEXT"  # fallback

        col_defs.append(f'"{name}" {col_type}')
    return ", ".join(col_defs)

def main():
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".csv"):
            table_name = os.path.splitext(file)[0]
            csv_path = os.path.join(DATA_FOLDER, file)
            column_file = os.path.join(DATA_FOLDER, f"{table_name}.columns")

            if os.path.exists(column_file):
                print(f" Processing table: {table_name}")

                # Generate CREATE TABLE SQL
                table_name=table_name.split('.')[1]
                schema_sql = parse_column_file(column_file)
                create_sql = f'DROP TABLE IF EXISTS "{table_name}"; CREATE TABLE "{table_name}" ({schema_sql});'
                
                with engine.connect() as conn:
                    conn.execute(text(create_sql))

                # Load CSV
                df = pd.read_csv(csv_path)
                df.to_sql(table_name, engine, if_exists="replace", index=False)
                print(f" Processing table: {table_name} DONE!")
            else:
                print(f" Missing .column file for {table_name}, skipping.")

if __name__ == "__main__":
    main()
