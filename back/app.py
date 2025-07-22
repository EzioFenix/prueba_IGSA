# app.py

from flask import Flask, request, jsonify
import pyodbc
from config import Config

app = Flask(__name__)

# Función para conectar a SQL Server
def get_connection():
    try:
        conn = pyodbc.connect(Config.CONNECTION_STRING)
        return conn
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

# 🟢 Ruta de prueba
@app.route('/', methods=['GET'])
def home():
    return jsonify({"mensaje": "API Flask + SQL Server funcionando correctamente"}), 200


# 🔹 1. GET: Obtener todos los registros
@app.route('/victormiguelbarrerapena', methods=['GET'])
def get_all():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cursor = conn.cursor()
    try:
        query = "SELECT id, titulo, descripcion, estado, fechaCreacion FROM victormiguelbarrerapena"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Convertir resultados a lista de diccionarios
        registros = []
        for row in rows:
            registros.append({
                "id": row.id,
                "titulo": row.titulo,
                "descripcion": row.descripcion,
                "estado": row.estado,
                "fechaCreacion": row.fechaCreacion.strftime('%Y-%m-%d %H:%M:%S') if row.fechaCreacion else None
            })

        return jsonify(registros), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener datos: {str(e)}"}), 500
    finally:
        conn.close()


# 🔹 2. POST: Crear un nuevo registro
@app.route('/victormiguelbarrerapena', methods=['POST'])
def create():
    data = request.get_json()

    # Validar campos obligatorios
    if not data or 'titulo' not in data or 'estado' not in data:
        return jsonify({"error": "Los campos 'titulo' y 'estado' son obligatorios"}), 400

    titulo = data['titulo']
    descripcion = data.get('descripcion', None)  # Opcional
    estado = data['estado']

    conn = get_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO victormiguelbarrerapena (titulo, descripcion, estado)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (titulo, descripcion, estado))
        conn.commit()

        # Obtener el ID del nuevo registro
        cursor.execute("SELECT SCOPE_IDENTITY()")  # Obtiene el último ID insertado
        nuevo_id = int(cursor.fetchone()[0])

        return jsonify({
            "mensaje": "Registro creado exitosamente",
            "id": nuevo_id
        }), 201
    except Exception as e:
        conn.rollback()  # Deshacer si hay error
        return jsonify({"error": f"No se pudo crear el registro: {str(e)}"}), 500
    finally:
        conn.close()


# 🔹 3. PUT: Actualizar un registro por ID
@app.route('/victormiguelbarrerapena/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()

    if not data or 'titulo' not in data or 'estado' not in data:
        return jsonify({"error": "Los campos 'titulo' y 'estado' son obligatorios"}), 400

    titulo = data['titulo']
    descripcion = data.get('descripcion')
    estado = data['estado']

    conn = get_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cursor = conn.cursor()
    try:
        # Verificar si el registro existe
        cursor.execute("SELECT id FROM victormiguelbarrerapena WHERE id = ?", (id,))
        if not cursor.fetchone():
            return jsonify({"error": "Registro no encontrado"}), 404

        # Actualizar
        query = """
        UPDATE victormiguelbarrerapena
        SET titulo = ?, descripcion = ?, estado = ?
        WHERE id = ?
        """
        cursor.execute(query, (titulo, descripcion, estado, id))
        conn.commit()

        return jsonify({"mensaje": "Registro actualizado correctamente"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"No se pudo actualizar: {str(e)}"}), 500
    finally:
        conn.close()


# 🔹 4. DELETE: Eliminar un registro por ID
@app.route('/victormiguelbarrerapena/<int:id>', methods=['DELETE'])
def delete(id):
    conn = get_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cursor = conn.cursor()
    try:
        # Verificar si existe
        cursor.execute("SELECT id FROM victormiguelbarrerapena WHERE id = ?", (id,))
        if not cursor.fetchone():
            return jsonify({"error": "Registro no encontrado"}), 404

        # Eliminar
        cursor.execute("DELETE FROM victormiguelbarrerapena WHERE id = ?", (id,))
        conn.commit()

        return jsonify({"mensaje": "Registro eliminado correctamente"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"No se pudo eliminar: {str(e)}"}), 500
    finally:
        conn.close()


# 🚀 Iniciar la app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)