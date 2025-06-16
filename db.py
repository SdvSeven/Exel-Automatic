import pandas as pd
import sqlite3
import ntpath  # для обработки путей к файлам

DB_PATH = "main.db"

def list_tables_from_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
    tables = df['name'].tolist()
    conn.close()
    return tables

def load_tables_from_db(table_names, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    dfs = []
    for t in table_names:
        df = pd.read_sql_query(f"SELECT * FROM '{t}'", conn)
        dfs.append(df)
    conn.close()
    return dfs

def table_exists(cursor, table_name):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    return cursor.fetchone() is not None

def write_to_sql(conn, df, table_name):
    cursor = conn.cursor()
    if table_exists(cursor, table_name):
        override = input(f"Таблица '{table_name}' уже существует. Перезаписать? [Y/N]: ").strip().lower()
        if override not in ['y', 'yes', 'да']:
            print(f"Пропущено: {table_name}")
            return
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Таблица '{table_name}' успешно записана.")

def sanitize_path(path: str) -> str:
    return path.strip().strip('"').strip("'")

def import_file_to_db(file_path, db_path=DB_PATH):
    file_path = sanitize_path(file_path)
    ext = ntpath.splitext(file_path)[1][1:].lower()
    base = ntpath.basename(file_path)
    name = ntpath.splitext(base)[0]

    try:
        conn = sqlite3.connect(db_path)
        if ext in ['xlsx', 'xls', 'xlsm', 'xlsb', 'odf', 'ods', 'odt']:
            xls = pd.ExcelFile(file_path, engine='openpyxl')
            for sheet in xls.sheet_names:
                df = xls.parse(sheet)
                table_name = f"{name}_{sheet}"
                write_to_sql(conn, df, table_name)
        elif ext == 'csv':
            df = pd.read_csv(file_path)
            write_to_sql(conn, df, name)
        else:
            print("Неподдерживаемое расширение файла:", ext)
            return
        conn.commit()
        conn.close()
        print(f"Файл '{file_path}' успешно импортирован в '{db_path}'.")
    except Exception as e:
        print("Ошибка при импорте файла:", e)

# Пример использования:
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Использование: python script.py путь_к_файлу")
    else:
        import_file_to_db(sys.argv[1])
