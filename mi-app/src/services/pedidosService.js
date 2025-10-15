// src/services/pedidosService.js
const API_URL = 'http://localhost:5000';

export const pedidosService = {
  // Obtener todos los pedidos
  async getPedidos() {
    try {
      const response = await fetch(`${API_URL}/pedidos`, {
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error('Error al cargar pedidos');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error en pedidosService.getPedidos:', error);
      throw error;
    }
  },

  // Obtener detalles de un pedido específico
  async getDetallesPedido(pedidoId) {
    try {
      const response = await fetch(`${API_URL}/pedidos/${pedidoId}/detalles`, {
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error('Error al cargar detalles del pedido');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error en pedidosService.getDetallesPedido:', error);
      throw error;
    }
  },

  // Crear nuevo pedido
  async createPedido(pedidoData) {
    try {
      const response = await fetch(`${API_URL}/pedidos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(pedidoData)
      });
      
      if (!response.ok) {
        throw new Error('Error al crear pedido');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error en pedidosService.createPedido:', error);
      throw error;
    }
  },

  // Actualizar pedido
  // En el método updatePedido del pedidosService.js
async updatePedido(pedidoId, pedidoData) {
  try {
    console.log('🔍 [UPDATE PEDIDO] Datos enviados:', {
      pedidoId,
      pedidoData
    });

    const response = await fetch(`${API_URL}/pedidos/${pedidoId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(pedidoData)
    });
    
    console.log('🔍 [UPDATE PEDIDO] Respuesta del servidor:', {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok
    });
    
    if (!response.ok) {
      // Intentar obtener el mensaje de error detallado
      let errorDetail = '';
      try {
        const errorData = await response.json();
        errorDetail = errorData.error || 'Sin detalles';
        console.error('🔍 [UPDATE PEDIDO] Error del servidor:', errorData);
      } catch (e) {
        errorDetail = await response.text();
        console.error('🔍 [UPDATE PEDIDO] Error sin JSON:', errorDetail);
      }
      throw new Error(`Error al actualizar pedido: ${response.status} - ${errorDetail}`);
    }
    
    const result = await response.json();
    console.log('🔍 [UPDATE PEDIDO] Éxito:', result);
    return result;
    
  } catch (error) {
    console.error('❌ [UPDATE PEDIDO] Error completo:', error);
    throw error;
  }
},

  // Eliminar pedido
  async deletePedido(pedidoId) {
    try {
      const response = await fetch(`${API_URL}/pedidos/${pedidoId}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error('Error al eliminar pedido');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error en pedidosService.deletePedido:', error);
      throw error;
    }
  },

  // Actualizar estado del pedido
  async updateEstadoPedido(pedidoId, nuevoEstado) {
    try {
      console.log('🔍 Intentando actualizar estado:', { pedidoId, nuevoEstado });
      
      const response = await fetch(`${API_URL}/pedidos/${pedidoId}/estado`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ estado: nuevoEstado })
      });
      
      console.log('🔍 Respuesta del servidor - Status:', response.status);
      console.log('🔍 Respuesta del servidor - OK:', response.ok);
      
      if (!response.ok) {
        let errorMessage = `Error ${response.status}: ${response.statusText}`;
        try {
          const errorData = await response.json();
          console.error('🔍 Error del servidor:', errorData);
          errorMessage = errorData.error || errorMessage;
        } catch (e) {
          console.error('🔍 No se pudo parsear error del servidor');
        }
        throw new Error(errorMessage);
      }
      
      const result = await response.json();
      console.log('🔍 Respuesta exitosa:', result);
      return result;
      
    } catch (error) {
      console.error('Error en pedidosService.updateEstadoPedido:', error);
      throw error;
    }
  },

  // NUEVOS MÉTODOS PARA GESTIÓN DE DETALLES

  // Crear nuevo detalle de pedido
  async createDetallePedido(detalleData) {
    try {
      const response = await fetch(`${API_URL}/detalle_pedidos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(detalleData)
      });
      
      if (!response.ok) {
        throw new Error('Error al crear detalle del pedido');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error en pedidosService.createDetallePedido:', error);
      throw error;
    }
  },

  // Actualizar detalle de pedido
  async updateDetallePedido(detalleId, detalleData) {
    try {
      const response = await fetch(`${API_URL}/detalle_pedidos/${detalleId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(detalleData)
      });
      
      if (!response.ok) {
        throw new Error('Error al actualizar detalle del pedido');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error en pedidosService.updateDetallePedido:', error);
      throw error;
    }
  },

  // Eliminar detalle de pedido
  async deleteDetallePedido(detalleId) {
    try {
      const response = await fetch(`${API_URL}/detalle_pedidos/${detalleId}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error('Error al eliminar detalle del pedido');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error en pedidosService.deleteDetallePedido:', error);
      throw error;
    }
  },

  // Obtener todos los detalles (para debugging)
  async getTodosDetalles() {
    try {
      const response = await fetch(`${API_URL}/detalle_pedidos`, {
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error('Error al cargar todos los detalles');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error en pedidosService.getTodosDetalles:', error);
      throw error;
    }
  }
};