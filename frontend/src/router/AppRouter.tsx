import React from 'react';
import {
  BrowserRouter,
  Navigate,
  Outlet,
  Route,
  Routes,
  Link,
} from 'react-router-dom';
import { LoginPage } from '../features/auth/LoginPage';
import { useAuth } from '../features/auth/AuthContext';
import { ProductsPage } from '../features/products/ProductsPage';
import { ProductDetailPage } from '../features/products/ProductDetailPage';
import { IndicesPage } from '../features/indices/IndicesPage';

const ProtectedLayout: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="app-layout">
      <header className="app-header">
        <h1>TocToc Precios</h1>
        <nav>
          <Link to="/products">Productos</Link>
          <Link to="/indices">Índice diario</Link>
        </nav>
        <button onClick={logout}>Salir</button>
      </header>
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
};

export const AppRouter: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={
            isAuthenticated ? (
              <Navigate to="/products" replace />
            ) : (
              <LoginPage onSuccess={() => {}} />
            )
          }
        />
        <Route path="/" element={<ProtectedLayout />}>
          <Route index element={<Navigate to="products" replace />} />
          <Route path="products" element={<ProductsPage />} />
          <Route path="products/:id" element={<ProductDetailPage />} />
          <Route path="indices" element={<IndicesPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};


