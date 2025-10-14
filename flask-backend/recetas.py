from flask import Blueprint, jsonify, request
from flask_login import login_required
from extensions import mysql

recetas_bp = Blueprint("recetas", __name__, url_prefix="/recetas")

# ================================
# Obtener todas las recetas
# ================================
@recetas_bp.route("/", methods=["GET"])
@login_required
def get_recetas():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT r.id_receta, r.id_producto, r.id_ingrediente, r.cantidad_necesaria,
               p.nombre AS producto, i.nombre AS ingrediente
        FROM recetas r
        LEFT JOIN productos p ON r.id_producto = p.id_producto
        LEFT JOIN ingredientes i ON r.id_ingrediente = i.id_ingrediente
    """)
    filas = cursor.fetchall()
    cursor.close()

    recetas = []
    for f in filas:
        recetas.append({
            "id_receta": f[0],
            "id_producto": f[1],
            "id_ingrediente": f[2],
            "cantidad_necesaria": f[3],
            "producto": f[4],       # nombre producto
            "ingrediente": f[5]     # nombre ingrediente
        })
    return jsonify(recetas)

# ================================
# Obtener una receta por ID
# ================================
@recetas_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_receta(id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT r.id_receta, r.id_producto, r.id_ingrediente, r.cantidad_necesaria,
               p.nombre AS producto, i.nombre AS ingrediente
        FROM recetas r
        LEFT JOIN productos p ON r.id_producto = p.id_producto
        LEFT JOIN ingredientes i ON r.id_ingrediente = i.id_ingrediente
        WHERE r.id_receta = %s
    """, (id,))
    f = cursor.fetchone()
    cursor.close()

    if not f:
        return jsonify({"error": "Receta no encontrada"}), 404

    receta = {
        "id_receta": f[0],
        "id_producto": f[1],
        "id_ingrediente": f[2],
        "cantidad_necesaria": f[3],
        "producto": f[4],
        "ingrediente": f[5]
    }
    return jsonify(receta)

# ================================
# Crear nueva receta
# ================================
@recetas_bp.route("/", methods=["POST"])
@login_required
def add_receta():
    data = request.get_json()
    id_producto = data.get("id_producto")
    id_ingrediente = data.get("id_ingrediente")
    cantidad_necesaria = data.get("cantidad_necesaria")

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO recetas (id_producto, id_ingrediente, cantidad_necesaria)
        VALUES (%s, %s, %s)
    """, (id_producto, id_ingrediente, cantidad_necesaria))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": "Receta agregada correctamente"})

# ================================
# Actualizar receta
# ================================
@recetas_bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_receta(id):
    data = request.get_json()
    id_producto = data.get("id_producto")
    id_ingrediente = data.get("id_ingrediente")
    cantidad_necesaria = data.get("cantidad_necesaria")

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE recetas
        SET id_producto=%s, id_ingrediente=%s, cantidad_necesaria=%s
        WHERE id_receta=%s
    """, (id_producto, id_ingrediente, cantidad_necesaria, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": "Receta actualizada correctamente"})

# ================================
# Eliminar receta
# ================================
@recetas_bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_receta(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM recetas WHERE id_receta=%s", (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Receta eliminada correctamente"})
