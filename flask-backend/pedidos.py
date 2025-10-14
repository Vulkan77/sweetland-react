from flask import Blueprint, jsonify, request
from flask_login import login_required
from extensions import mysql
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")

@pedidos_bp.route("/", methods=["GET"])
@login_required
def get_pedidos():
    try:
        logger.debug("Ejecutando consulta de pedidos")
        cursor = mysql.connection.cursor()
        
        # Primero verificar si existe el campo 'estado'
        cursor.execute("SHOW COLUMNS FROM pedidos LIKE 'estado'")
        tiene_estado = cursor.fetchone()
        
        if tiene_estado:
            # Consulta CON campo estado
            cursor.execute("""
                SELECT 
                    p.id_pedido, 
                    u.nombre AS cliente_nombre,
                    u.telefono AS cliente_telefono,
                    p.fecha_pedido, 
                    p.estado,
                    p.total,
                    p.direccion,
                    COUNT(dp.id_detalle) as total_productos
                FROM pedidos p
                LEFT JOIN usuarios u ON p.usuario_id = u.id_usuario
                LEFT JOIN detalle_pedidos dp ON p.id_pedido = dp.pedido_id
                GROUP BY p.id_pedido, u.nombre, u.telefono
                ORDER BY p.fecha_pedido DESC
            """)
        else:
            # Consulta SIN campo estado
            cursor.execute("""
                SELECT 
                    p.id_pedido, 
                    u.nombre AS cliente_nombre,
                    u.telefono AS cliente_telefono,
                    p.fecha_pedido, 
                    p.total,
                    p.direccion,
                    p.telefono,
                    COUNT(dp.id_detalle) as total_productos
                FROM pedidos p
                LEFT JOIN usuarios u ON p.usuario_id = u.id_usuario
                LEFT JOIN detalle_pedidos dp ON p.id_pedido = dp.pedido_id
                GROUP BY p.id_pedido, u.nombre, u.telefono
                ORDER BY p.fecha_pedido DESC
            """)
        
        filas = cursor.fetchall()
        logger.debug(f"Pedidos encontrados: {len(filas)}")
        
        cursor.close()

        pedidos = []
        for f in filas:
            if tiene_estado:
                pedido = {
                    "id": f[0],
                    "cliente_nombre": f[1] or "Cliente no registrado",
                    "cliente_telefono": f[2] or "Sin teléfono",
                    "fecha_pedido": f[3].strftime('%Y-%m-%d %H:%M:%S') if f[3] else None,
                    "estado": f[4] or "pendiente",
                    "total": float(f[5]) if f[5] else 0,
                    "direccion": f[6] or "Sin dirección",
                    "total_productos": f[7]
                }
            else:
                pedido = {
                    "id": f[0],
                    "cliente_nombre": f[1] or "Cliente no registrado",
                    "cliente_telefono": f[2] or "Sin teléfono",
                    "fecha_pedido": f[3].strftime('%Y-%m-%d %H:%M:%S') if f[3] else None,
                    "estado": "pendiente",  # Valor por defecto
                    "total": float(f[4]) if f[4] else 0,
                    "direccion": f[5] or "Sin dirección",
                    "total_productos": f[7]
                }
            pedidos.append(pedido)
            logger.debug(f"Pedido procesado: {pedido}")

        return jsonify(pedidos)
        
    except Exception as e:
        logger.error(f"Error en get_pedidos: {str(e)}")
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@pedidos_bp.route("/<int:id>/detalles", methods=["GET"])
@login_required
def get_detalles_pedido(id):
    try:
        logger.debug(f"Solicitando detalles del pedido {id}")
        cursor = mysql.connection.cursor()
        
        # Verificar que el pedido existe
        cursor.execute("SELECT id_pedido FROM pedidos WHERE id_pedido = %s", (id,))
        pedido_existe = cursor.fetchone()
        
        if not pedido_existe:
            cursor.close()
            return jsonify({"error": f"Pedido {id} no encontrado"}), 404
        
        # Verificar si existe precio_unitario en detalle_pedidos
        cursor.execute("SHOW COLUMNS FROM detalle_pedidos LIKE 'precio_unitario'")
        tiene_precio_unitario = cursor.fetchone()
        
        if tiene_precio_unitario:
            # Consulta CON precio_unitario
            cursor.execute("""
                SELECT 
                    dp.id_detalle,
                    dp.producto_id,
                    p.nombre AS producto_nombre,
                    p.categoria,
                    dp.cantidad,
                    dp.precio_unitario,
                    dp.subtotal
                FROM detalle_pedidos dp
                INNER JOIN productos p ON dp.producto_id = p.id_producto
                WHERE dp.pedido_id = %s
            """, (id,))
        else:
            # Consulta SIN precio_unitario - calcularlo
            cursor.execute("""
                SELECT 
                    dp.id_detalle,
                    dp.producto_id,
                    p.nombre AS producto_nombre,
                    p.categoria,
                    dp.cantidad,
                    dp.subtotal,
                    p.precio as precio_referencia
                FROM detalle_pedidos dp
                INNER JOIN productos p ON dp.producto_id = p.id_producto
                WHERE dp.pedido_id = %s
            """, (id,))
        
        detalles = cursor.fetchall()
        cursor.close()
        
        logger.debug(f"Detalles encontrados para pedido {id}: {len(detalles)}")
        
        detalles_formateados = []
        for detalle in detalles:
            if tiene_precio_unitario:
                detalle_info = {
                    "id": detalle[0],
                    "producto_id": detalle[1],
                    "producto_nombre": detalle[2],
                    "categoria": detalle[3],
                    "cantidad": detalle[4],
                    "precio_unitario": float(detalle[5]) if detalle[5] else 0,
                    "subtotal": float(detalle[6]) if detalle[6] else 0
                }
            else:
                # Calcular precio unitario basado en subtotal / cantidad
                cantidad = detalle[4] or 1
                subtotal = float(detalle[5]) if detalle[5] else 0
                precio_unitario = subtotal / cantidad if cantidad > 0 else 0
                
                detalle_info = {
                    "id": detalle[0],
                    "producto_id": detalle[1],
                    "producto_nombre": detalle[2],
                    "categoria": detalle[3],
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "subtotal": subtotal
                }
            detalles_formateados.append(detalle_info)
            logger.debug(f"Detalle: {detalle_info}")

        return jsonify(detalles_formateados)
        
    except Exception as e:
        logger.error(f"Error en get_detalles_pedido: {str(e)}")
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@pedidos_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_pedido(id):
    try:
        cursor = mysql.connection.cursor()
        
        # Verificar si existe el campo 'estado'
        cursor.execute("SHOW COLUMNS FROM pedidos LIKE 'estado'")
        tiene_estado = cursor.fetchone()
        
        if tiene_estado:
            cursor.execute("""
                SELECT p.id_pedido, u.nombre, u.telefono, p.fecha_pedido, 
                       p.estado, p.total, p.direccion
                FROM pedidos p
                LEFT JOIN usuarios u ON p.usuario_id = u.id_usuario
                WHERE p.id_pedido = %s
            """, (id,))
        else:
            cursor.execute("""
                SELECT p.id_pedido, u.nombre, u.telefono, p.fecha_pedido, 
                       p.total, p.direccion
                FROM pedidos p
                LEFT JOIN usuarios u ON p.usuario_id = u.id_usuario
                WHERE p.id_pedido = %s
            """, (id,))
            
        f = cursor.fetchone()
        cursor.close()
        
        if not f:
            return jsonify({"error": "Pedido no encontrado"}), 404

        if tiene_estado:
            pedido = {
                "id_pedido": f[0],
                "cliente_nombre": f[1] or "Cliente no registrado",
                "cliente_telefono": f[2] or "Sin teléfono",
                "fecha_pedido": f[3].strftime('%Y-%m-%d %H:%M:%S') if f[3] else None,
                "estado": f[4] or "pendiente",
                "total": float(f[5]) if f[5] else 0,
                "direccion": f[6] or "Sin dirección"
            }
        else:
            pedido = {
                "id_pedido": f[0],
                "cliente_nombre": f[1] or "Cliente no registrado",
                "cliente_telefono": f[2] or "Sin teléfono",
                "fecha_pedido": f[3].strftime('%Y-%m-%d %H:%M:%S') if f[3] else None,
                "estado": "pendiente",
                "total": float(f[4]) if f[4] else 0,
                "direccion": f[5] or "Sin dirección"
            }
        return jsonify(pedido)
        
    except Exception as e:
        logger.error(f"Error en get_pedido: {str(e)}")
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@pedidos_bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_pedido(id):
    try:
        data = request.get_json()
        total = data.get("total")
        direccion = data.get("direccion")
        telefono = data.get("telefono")
        estado = data.get("estado")

        cursor = mysql.connection.cursor()
        
        # Verificar si existe el campo 'estado'
        cursor.execute("SHOW COLUMNS FROM pedidos LIKE 'estado'")
        tiene_estado = cursor.fetchone()
        
        if tiene_estado and estado:
            cursor.execute("""
                UPDATE pedidos 
                SET total=%s, direccion=%s, telefono=%s, estado=%s 
                WHERE id_pedido=%s
            """, (total, direccion, telefono, estado, id))
        else:
            cursor.execute("""
                UPDATE pedidos 
                SET total=%s, direccion=%s, telefono=%s
                WHERE id_pedido=%s
            """, (total, direccion, telefono, id))
            
        mysql.connection.commit()
        cursor.close()
        return jsonify({"mensaje": "Pedido actualizado correctamente"})
        
    except Exception as e:
        logger.error(f"Error en update_pedido: {str(e)}")
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@pedidos_bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_pedido(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM detalle_pedidos WHERE pedido_id = %s", (id,))
        cursor.execute("DELETE FROM pedidos WHERE id_pedido = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"mensaje": "Pedido eliminado correctamente"})
        
    except Exception as e:
        logger.error(f"Error en delete_pedido: {str(e)}")
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@pedidos_bp.route("/", methods=["POST"])
@login_required
def create_pedido():
    try:
        data = request.get_json()
        
        usuario_id = data.get("usuario_id")
        cliente_nombre = data.get("cliente_nombre")
        cliente_telefono = data.get("cliente_telefono")
        direccion = data.get("direccion")
        total = data.get("total", 0)
        
        cursor = mysql.connection.cursor()
        
        # Verificar si existe el campo 'estado'
        cursor.execute("SHOW COLUMNS FROM pedidos LIKE 'estado'")
        tiene_estado = cursor.fetchone()
        
        if tiene_estado:
            cursor.execute("""
                INSERT INTO pedidos (usuario_id, cliente_nombre, cliente_telefono, direccion, total, estado, fecha_pedido)
                VALUES (%s, %s, %s, %s, %s, 'pendiente', NOW())
            """, (usuario_id, cliente_nombre, cliente_telefono, direccion, total))
        else:
            cursor.execute("""
                INSERT INTO pedidos (usuario_id, cliente_nombre, cliente_telefono, direccion, total, fecha_pedido)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (usuario_id, cliente_nombre, cliente_telefono, direccion, total))
        
        pedido_id = cursor.lastrowid
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({
            "mensaje": "Pedido creado correctamente",
            "id_pedido": pedido_id
        }), 201
        
    except Exception as e:
        logger.error(f"Error en create_pedido: {str(e)}")
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500

@pedidos_bp.route("/<int:id>/estado", methods=["PUT"])
@login_required
def update_estado_pedido(id):
    try:
        data = request.get_json()
        nuevo_estado = data.get("estado")
        
        # Validar estados permitidos
        estados_permitidos = ['pendiente', 'confirmado', 'en_preparacion', 'completado', 'cancelado']
        if nuevo_estado not in estados_permitidos:
            return jsonify({"error": "Estado no válido"}), 400

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE pedidos 
            SET estado = %s 
            WHERE id_pedido = %s
        """, (nuevo_estado, id))
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({
            "mensaje": f"Estado del pedido actualizado a '{nuevo_estado}'",
            "estado": nuevo_estado
        })
        
    except Exception as e:
        logger.error(f"Error en update_estado_pedido: {str(e)}")
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500