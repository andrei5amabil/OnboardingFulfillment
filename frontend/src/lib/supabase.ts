import { createClient } from '@supabase/supabase-js';

const supabaseUrl = `${window.location.origin}/supabase`;
const supabaseAnonKey =
  import.meta.env.VITE_SUPABASE_KEY ||
  'sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);