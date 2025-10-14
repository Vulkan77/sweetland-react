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
  async updatePedido(pedidoId, pedidoData) {
    try {
      const response = await fetch(`${API_URL}/pedidos/${pedidoId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(pedidoData)
      });
      
      if (!response.ok) {
        throw new Error('Error al actualizar pedido');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error en pedidosService.updatePedido:', error);
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
      const response = await fetch(`${API_URL}/pedidos/${pedidoId}/estado`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ estado: nuevoEstado })
      });
      
      if (!response.ok) {
        throw new Error('Error al actualizar estado del pedido');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error en pedidosService.updateEstadoPedido:', error);
      throw error;
    }
  }
};