import React, { createContext, useContext, useEffect, useState } from 'react';
import { apiFetch } from '../../api/client';
import type { TokenResponse } from '../../api/types';

interface AuthContextValue {
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const STORAGE_KEY = 'toc_toc_token';

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const saved = window.localStorage.getItem(STORAGE_KEY);
    if (saved) {
      setToken(saved);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const data = await apiFetch<TokenResponse>('/auth/login-json', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    setToken(data.access_token);
    window.localStorage.setItem(STORAGE_KEY, data.access_token);
  };

  const logout = () => {
    setToken(null);
    window.localStorage.removeItem(STORAGE_KEY);
  };

  return (
    <AuthContext.Provider
      value={{ token, isAuthenticated: !!token, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextValue => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return ctx;
};


