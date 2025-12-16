import React, { useEffect, useState } from 'react';
import { useAuth } from '../auth/AuthContext';
import { apiFetch } from '../../api/client';
import type { DailyIndexPoint } from '../../api/types';

export const IndicesPage: React.FC = () => {
  const { token } = useAuth();
  const today = new Date().toISOString().slice(0, 10);
  const [fromDate, setFromDate] = useState<string>(today);
  const [toDate, setToDate] = useState<string>(today);
  const [points, setPoints] = useState<DailyIndexPoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    if (!token) return;
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({
        from: fromDate,
        to: toDate,
      });
      const data = await apiFetch<DailyIndexPoint[]>(
        `/indices/daily?${params.toString()}`,
        {},
        token,
      );
      setPoints(data);
    } catch (err) {
      console.error(err);
      setError('No se pudo cargar el índice diario.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div>
      <h2>Índice diario de precios</h2>
      <div className="filters">
        <label>
          Desde
          <input
            type="date"
            value={fromDate}
            onChange={(e) => setFromDate(e.target.value)}
          />
        </label>
        <label>
          Hasta
          <input
            type="date"
            value={toDate}
            onChange={(e) => setToDate(e.target.value)}
          />
        </label>
        <button onClick={load}>Actualizar</button>
      </div>
      {loading && <p>Cargando...</p>}
      {error && <p className="error">{error}</p>}
      {!loading && !error && (
        <div className="scatter-container">
          {points.length === 0 && <p>No hay datos para el rango elegido.</p>}
          <ul className="scatter-list">
            {points.map((p) => (
              <li key={p.date}>
                <span>{p.date}</span>
                <span>{p.index_value.toFixed(2)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};



