import React, { createContext, useContext, useEffect, useState } from 'react';
import type { User } from '@supabase/supabase-js';
import { supabase } from '../lib/supabase';

export type UserRole = 'admin' | 'hr_manager' | 'it_manager' | 'new_hire';

interface AuthContextType {
  user: User | null;
  role: UserRole | null;
  employeeId: string | null;
  token: string | null;
  loading: boolean;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [role, setRole] = useState<UserRole | null>(null);
  const [employeeId, setEmployeeId] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const syncUserProfile = async (userId: string) => {
    try {
        const { data, error } = await supabase
        .from('users')
        .select('role, employee_id')
        .eq('user_id', userId)
        .single();

        console.log('User profile fetch:', { data, error });

        if (error) {
        console.error('Error fetching user profile:', error.message);
        return;
        }

        if (data) {
        setRole(data.role as UserRole);
        setEmployeeId(data.employee_id);
        }
      } catch (err) {
          console.error('Failed to sync profile', err);
    }};

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session) {
        setUser(session.user);
        setToken(session.access_token);
        syncUserProfile(session.user.id).finally(() => setLoading(false));
      } else {
        setLoading(false);
      }
    });

    const { data: listener } = supabase.auth.onAuthStateChange(async (_event, session) => {
      if (session) {
        setUser(session.user);
        setToken(session.access_token);
        await syncUserProfile(session.user.id);
      } else {
        setUser(null);
        setRole(null);
        setToken(null);
        setEmployeeId(null);
      }
      setLoading(false);
    });

    return () => listener.subscription.unsubscribe();
  }, []);

  const signOut = async () => {
    await supabase.auth.signOut();
  };

  return (
    <AuthContext.Provider value={{ user, role, employeeId, token, loading, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);