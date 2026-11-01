import { supabase } from './supabase';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/+$/, '');

export async function fetchWithAuth(endpoint: string, options: RequestInit = {}): Promise<Response> {
  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;

  if (!token) {
    console.warn('⚠️ No active Supabase access token found in session.');
  }

  const headers = new Headers(options.headers || {});
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  if (endpoint.startsWith('http')) {
    return fetch(endpoint, { ...options, headers });
  }

  const cleanEndpoint = endpoint.replace(/^(\/api)+/, '');
  const normalizedEndpoint = cleanEndpoint.startsWith('/') ? cleanEndpoint : `/${cleanEndpoint}`;
  const url = `${API_BASE_URL}${normalizedEndpoint}`;

  return fetch(url, { ...options, headers });
}