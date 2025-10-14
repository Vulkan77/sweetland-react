import { useState } from 'react';

const Login = ({ onLogin, onShowRegister }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('🔍 Intentando login con:', email);
      const result = await onLogin(email, password);
      console.log('🔍 Resultado del login:', result);
      
      if (!result.success) {
        setError(result.error);
      }
    } catch (err) {
      console.error('🔍 Error en login:', err);
      setError('Error de conexión con el servidor');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#0d6efd',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '400px'
      }}>
        {/* Mensaje de bienvenida */}
        <div style={{
          textAlign: 'center',
          color: 'white',
          marginBottom: '40px'
        }}>
          <h1 style={{ 
            fontWeight: 'bold', 
            marginBottom: '20px',
            fontSize: '2.5rem'
          }}>
            🎂 Sweetland by Anny
          </h1>
          <p style={{ 
            fontSize: '1.2rem',
            opacity: 0.9,
            marginBottom: '5px'
          }}>
            Bienvenido a tu panel de gestión
          </p>
          <p style={{ 
            fontSize: '0.9rem',
            opacity: 0.7
          }}>
            Sistema administrativo Sweetland By Amy
          </p>
        </div>

        {/* Card de login */}
        <div style={{
          backgroundColor: 'white',
          borderRadius: '12px',
          padding: '30px',
          boxShadow: '0 10px 30px rgba(0,0,0,0.2)'
        }}>
          <h4 style={{
            textAlign: 'center',
            marginBottom: '25px',
            color: '#333'
          }}>
            Iniciar Sesión
          </h4>
          
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '20px' }}>
              <input
                type="email"
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '1rem'
                }}
                placeholder="Correo electrónico"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading}
              />
            </div>
            
            <div style={{ marginBottom: '25px' }}>
              <input
                type="password"
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #ddd',
                  borderRadius: '6px',
                  fontSize: '1rem'
                }}
                placeholder="Contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
              />
            </div>
            
            <button 
              type="submit" 
              style={{
                width: '100%',
                padding: '12px',
                backgroundColor: loading ? '#6c757d' : '#0d6efd',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                fontSize: '1rem',
                fontWeight: '500',
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
              disabled={loading}
            >
              {loading ? 'Cargando...' : 'Entrar'}
            </button>
          </form>

          {error && (
            <div style={{
              backgroundColor: '#f8d7da',
              color: '#721c24',
              padding: '10px',
              borderRadius: '6px',
              marginTop: '20px',
              textAlign: 'center',
              fontSize: '0.9rem'
            }}>
              {error}
            </div>
          )}

          <div style={{
            textAlign: 'center',
            marginTop: '20px',
            paddingTop: '20px',
            borderTop: '1px solid #eee'
          }}>
            <small style={{ color: '#666' }}>
              ¿No tienes cuenta?{' '}
              <button 
                onClick={onShowRegister}
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#0d6efd',
                  textDecoration: 'underline',
                  cursor: 'pointer'
                }}
                disabled={loading}
              >
                Registrarse
              </button>
            </small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;