import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import { apiFetch } from '../../api/client';
import type { ProductDetail } from '../../api/types';

export const ProductDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { token } = useAuth();
  const [detail, setDetail] = useState<ProductDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const run = async () => {
      if (!token || !id) return;
      setLoading(true);
      setError(null);
      try {
        const data = await apiFetch<ProductDetail>(
          `/products/${id}`,
          {},
          token,
        );
        setDetail(data);
      } catch (err) {
        console.error(err);
        setError('No se pudo cargar el detalle del producto.');
      } finally {
        setLoading(false);
      }
    };
    void run();
  }, [id, token]);

  if (loading) return <p>Cargando...</p>;
  if (error) return <p className="error">{error}</p>;
  if (!detail) return <p>No hay información del producto.</p>;

  return (
    <div>
      <h2>{detail.name}</h2>
      <p>
        Código: <strong>{detail.code}</strong> | Unidad:{' '}
        <strong>{detail.unit}</strong>
      </p>
      <h3>Histórico de precios por cadena</h3>
      <table className="data-table">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Cadena</th>
            <th>Precio</th>
          </tr>
        </thead>
        <tbody>
          {detail.history.map((p) => (
            <tr key={`${p.date}-${p.chain_id}`}>
              <td>{p.date}</td>
              <td>{p.chain_name}</td>
              <td>{p.price.toLocaleString('es-CO')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};


