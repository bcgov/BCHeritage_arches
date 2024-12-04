import os


def format_files_into_sql(files: [str], sql_dir: str):
    sql_string = ""
    for filename in files:
        file_path = os.path.join(sql_dir, filename)
        with open(file_path) as file:
            sql_string = sql_string + "\n" + file.read()
    return sql_string
