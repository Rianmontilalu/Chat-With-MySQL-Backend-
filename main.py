import os
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import errorcode
from langchain_openai import OpenAI
from dotenv import load_dotenv
import re


app = Flask(__name__)

def get_table_fields(cursor, table_name):
    try:
        cursor.execute(f"DESCRIBE {table_name};")
        columns = cursor.fetchall()
        field_names = [column[0].decode('utf-8') if isinstance(column[0], bytearray) else column[0] for column in columns]
        return field_names
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

def get_database_schema(cursor):
    try:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        schema = {}
        for (table_name,) in tables:
            table_name_str = table_name.decode('utf-8') if isinstance(table_name, bytearray) else table_name
            schema[table_name_str] = get_table_fields(cursor, table_name_str)
        return schema
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {}



# Setup OpenAI API key dari ENV

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_key=openai_api_key)

# Route untuk endpoint '/'
@app.route('/')
def index():
    return jsonify({"message": "Selamat datang di API Backend Chat with MySQL (Kelompok Glue 4)"})

# Route untuk endpoint '/query'
@app.route('/query', methods=['POST'])
def query():
    try:
        # Ambil data JSON dari request
        data = request.json
        question = data['question']

        # Konfigurasi MySQL
        user = data['user']
        password = data['password']
        host = data['host']
        port = data['port']
        database = data['database']

        config = {
            'user': user, 
            'password': password,
            'host': host,
            'port': port,
            'database': database,
            'raise_on_warnings': True,
            'ssl_disabled': True
        }
        

        
        # Konek ke database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Ngambil Skema Database
        # schema = get_database_schema(cursor)

        try:
            schema = get_database_schema(cursor)
        except Exception as e:
            print(e)
            return jsonify({"error db schema": str(e)})
        

        # Bikin pertanyaan
        schema_str = '\n'.join(f"- {table}: {', '.join(fields)}" for table, fields in schema.items())
        prompt_query = f"""Berdasarkan skema database ({database}) dibawah, tuliskan query SQL yang dapat menjawab pertanyaan user berikut, tulis query SQL tanpa penjelasan apapun:
        {schema_str}
        
        Pertanyaan user: {question}"""

        response_query = llm(prompt_query)

        # Bersihkan query
        sql_query = response_query.replace("?", "").replace("\\n", "\n").strip()

        match = re.search(r'\bSELECT\b', sql_query, re.IGNORECASE)

        if match:
            sql_query_cleaned = sql_query[match.start():]
        else:
            sql_query_cleaned = sql_query

        print(sql_query_cleaned)

        # Eksekusi query
        cursor.execute(sql_query_cleaned)
        result = cursor.fetchall()

        print(result)

        cursor.close()
        cnx.close()

        prompt_jawaban = f"""Berdasarkan pertanyaan user dibawah dan berdasarkan data yang sudah di dapat dari database ({database}), berikan kalimat jawaban yang sesuai:
        Pertanyaan user: {question}
        Hasil Query: {result}"""

        response_jawaban = llm(prompt_jawaban)
        return jsonify({"jawaban": response_jawaban})
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return jsonify({"error": "Salah username atau password, cek lagi!"})
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return jsonify({"error": "Databasenya ngga ada!"})
        else:
            return jsonify({"error": str(err)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
