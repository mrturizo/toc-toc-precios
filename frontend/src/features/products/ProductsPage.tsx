import React, { useEffect, useState } from 'react';
import { useAuth } from '../auth/AuthContext';
import { apiFetch } from '../../api/client';
import type { ProductSummary } from '../../api/types';

export const ProductsPage: React.FC = () => {
  const { token } = useAuth();
  const [date, setDate] = useState<string>(() =>
    new Date().toISOString().slice(0, 10),
  );
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [products, setProducts] = useState<ProductSummary[]>([]);

  const load = async () => {
    if (!token) return;
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({ date });
      if (search) params.append('search', search);
      const data = await apiFetch<ProductSummary[]>(
        `/products?${params.toString()}`,
        {},
        token,
      );
      setProducts(data);
    } catch (err) {
      console.error(err);
      setError('No se pudieron cargar los productos.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [date]);

  return (
    <div>
      <h2>Productos y precios por cadena</h2>
      <div className="filters">
        <label>
          Fecha
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </label>
        <label>
          Buscar
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Nombre o código"
          />
        </label>
        <button onClick={load}>Aplicar filtros</button>
      </div>
      {loading && <p>Cargando...</p>}
      {error && <p className="error">{error}</p>}
      {!loading && !error && (
        <table className="data-table">
          <thead>
            <tr>
              <th>Producto</th>
              <th>Unidad</th>
              <th colSpan={3}>Precios por cadena</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.id}>
                <td>
                  <a href={`/products/${p.id}`}>{p.name}</a>
                </td>
                <td>{p.unit}</td>
                <td>
                  {p.prices.map((pr) => (
                    <div key={pr.chain_id}>
                      {pr.chain_name}: {pr.price.toLocaleString('es-CO')}
                    </div>
                  ))}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};


