import os
import time
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

def conectar():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

def preparar_base_datos():
    for intento in range(10):
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS incidencias (
                    id SERIAL PRIMARY KEY,
                    titulo VARCHAR(150) NOT NULL,
                    descripcion TEXT,
                    estado VARCHAR(30) DEFAULT 'Pendiente',
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conexion.commit()
            cursor.close()
            conexion.close()
            print("Base de datos preparada correctamente")
            return

        except psycopg2.OperationalError:
            print("Esperando a PostgreSQL...")
            time.sleep(3)

    raise Exception("No se pudo conectar con PostgreSQL")

@app.route("/api/incidencias", methods=["GET"])
def listar_incidencias():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, titulo, descripcion, estado, fecha
        FROM incidencias
        ORDER BY id DESC
    """)

    filas = cursor.fetchall()
    cursor.close()
    conexion.close()

    resultado = [
        {
            "id": fila[0],
            "titulo": fila[1],
            "descripcion": fila[2],
            "estado": fila[3],
            "fecha": fila[4].isoformat()
        }
        for fila in filas
    ]

    return jsonify(resultado)

@app.route("/api/incidencias", methods=["POST"])
def crear_incidencia():
    datos = request.get_json(silent=True) or {}

    titulo = datos.get("titulo", "").strip()
    descripcion = datos.get("descripcion", "").strip()

    if not titulo:
        return jsonify({"error": "El título es obligatorio"}), 400

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO incidencias (titulo, descripcion)
        VALUES (%s, %s)
        RETURNING id
    """, (titulo, descripcion))

    nuevo_id = cursor.fetchone()[0]

    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Incidencia creada correctamente",
        "id": nuevo_id
    }), 201

@app.route("/api/health", methods=["GET"])
def comprobar_estado():
    return jsonify({"estado": "correcto"})

if __name__ == "__main__":
    preparar_base_datos()
    app.run(host="0.0.0.0", port=5000)