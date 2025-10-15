import React, { useState } from 'react';

const PedidoForm = ({ productos, onSubmit, onClose, titulo = "➕ Nuevo Pedido" }) => {
  const [formData, setFormData] = useState({
    cliente_nombre: '',
    cliente_telefono: '',
    telefono: '', // Campo adicional para la DB
    direccion: '',
    detalles: []
  });
  const [productoSeleccionado, setProductoSeleccionado] = useState('');
  const [cantidad, setCantidad] = useState(1);
  const [error, setError] = useState('');

  const agregarProducto = () => {
    if (!productoSeleccionado || cantidad < 1) {
      setError('Selecciona un producto y cantidad válida');
      return;
    }

    const producto = productos.find(p => p.id_producto === parseInt(productoSeleccionado));
    if (!producto) {
      setError('Producto no encontrado');
      return;
    }

    const subtotal = producto.precio * cantidad;
    const nuevoDetalle = {
      producto_id: producto.id_producto,
      producto_nombre: producto.nombre,
      cantidad: cantidad,
      precio_unitario: producto.precio,
      subtotal: subtotal
    };

    setFormData(prev => ({
      ...prev,
      detalles: [...prev.detalles, nuevoDetalle]
    }));

    setProductoSeleccionado('');
    setCantidad(1);
    setError('');
  };

  const eliminarProducto = (index) => {
    setFormData(prev => ({
      ...prev,
      detalles: prev.detalles.filter((_, i) => i !== index)
    }));
  };

  const calcularTotal = () => {
    return formData.detalles.reduce((total, detalle) => total + detalle.subtotal, 0);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.cliente_nombre || !formData.cliente_telefono || !formData.direccion) {
      setError('Todos los campos del cliente son obligatorios');
      return;
    }

    if (formData.detalles.length === 0) {
      setError('Debe agregar al menos un producto al pedido');
      return;
    }

    try {
      // Asegurarse de incluir el campo telefono para la DB
      const pedidoData = {
        ...formData,
        telefono: formData.cliente_telefono, // Mismo valor para ambos campos
        total: calcularTotal(),
        usuario_id: 1
      };

      await onSubmit(pedidoData);
    } catch (error) {
      setError('Error al crear el pedido: ' + error.message);
    }
  };

  return (
    <div className="modal fade show d-block" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
      <div className="modal-dialog modal-lg">
        <div className="modal-content">
          <div className="modal-header bg-success text-white">
            <h5 className="modal-title">{titulo}</h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body">
              {error && <div className="alert alert-danger">{error}</div>}

              <div className="row mb-3">
                <div className="col-md-6">
                  <label className="form-label">Nombre del Cliente *</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.cliente_nombre}
                    onChange={(e) => setFormData(prev => ({...prev, cliente_nombre: e.target.value}))}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label">Teléfono *</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.cliente_telefono}
                    onChange={(e) => setFormData(prev => ({
                      ...prev, 
                      cliente_telefono: e.target.value,
                      telefono: e.target.value // Actualizar ambos campos
                    }))}
                    required
                  />
                </div>
              </div>

              <div className="mb-3">
                <label className="form-label">Dirección de Entrega *</label>
                <textarea
                  className="form-control"
                  rows="2"
                  value={formData.direccion}
                  onChange={(e) => setFormData(prev => ({...prev, direccion: e.target.value}))}
                  required
                />
              </div>

              <div className="card mb-3">
                <div className="card-header bg-light">
                  <h6 className="mb-0">🛒 Agregar Productos</h6>
                </div>
                <div className="card-body">
                  <div className="row g-2">
                    <div className="col-md-6">
                      <select
                        className="form-select"
                        value={productoSeleccionado}
                        onChange={(e) => setProductoSeleccionado(e.target.value)}
                      >
                        <option value="">Seleccionar producto...</option>
                        {productos.map(producto => (
                          <option key={producto.id_producto} value={producto.id_producto}>
                            {producto.nombre} - ${producto.precio.toLocaleString()}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="col-md-3">
                      <input
                        type="number"
                        className="form-control"
                        min="1"
                        value={cantidad}
                        onChange={(e) => setCantidad(parseInt(e.target.value) || 1)}
                      />
                    </div>
                    <div className="col-md-3">
                      <button
                        type="button"
                        className="btn btn-primary w-100"
                        onClick={agregarProducto}
                      >
                        ➕ Agregar
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              {formData.detalles.length > 0 && (
                <div className="table-responsive">
                  <table className="table table-sm">
                    <thead className="table-dark">
                      <tr>
                        <th>Producto</th>
                        <th>Cantidad</th>
                        <th>Precio Unitario</th>
                        <th>Subtotal</th>
                        <th>Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      {formData.detalles.map((detalle, index) => (
                        <tr key={index}>
                          <td>{detalle.producto_nombre}</td>
                          <td>{detalle.cantidad}</td>
                          <td>${detalle.precio_unitario.toLocaleString()}</td>
                          <td>${detalle.subtotal.toLocaleString()}</td>
                          <td>
                            <button
                              type="button"
                              className="btn btn-danger btn-sm"
                              onClick={() => eliminarProducto(index)}
                            >
                              🗑️
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                    <tfoot>
                      <tr>
                        <td colSpan="3" className="text-end fw-bold">Total:</td>
                        <td className="fw-bold text-success">${calcularTotal().toLocaleString()}</td>
                        <td></td>
                      </tr>
                    </tfoot>
                  </table>
                </div>
              )}
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>
                Cancelar
              </button>
              <button type="submit" className="btn btn-success">
                ✅ Crear Pedido
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default PedidoForm;