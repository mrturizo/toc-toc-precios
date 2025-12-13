import React, { useState } from 'react';
import { useAuth } from './AuthContext';

interface Props {
  onSuccess?: () => void;
}

export const LoginPage: React.FC<Props> = ({ onSuccess }) => {
  const { login } = useAuth();
  const [email, setEmail] = useState('demo@toctoc.com');
  const [password, setPassword] = useState('demo1234');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(email, password);
      if (onSuccess) {
        onSuccess();
      }
    } catch (err) {
      console.error(err);
      setError('Credenciales inválidas o error de conexión.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-layout">
      <div className="auth-card">
        <h1>TocToc Precios</h1>
        <p>Inicia sesión para ver el tablero de precios.</p>
        <form onSubmit={handleSubmit} className="auth-form">
          <label>
            Correo
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>
          <label>
            Contraseña
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          {error && <div className="auth-error">{error}</div>}
          <button type="submit" disabled={loading}>
            {loading ? 'Ingresando...' : 'Entrar'}
          </button>
        </form>
        <p className="auth-hint">
          Demo: <code>demo@toctoc.com</code> / <code>demo1234</code>
        </p>
      </div>
    </div>
  );
};


