-- Migration unit 1: schema_changes
-- Transaction mode: transactional
-- Boundary reason: default

GRANT DELETE, INSERT, SELECT, UPDATE ON public.employees TO anon;

GRANT DELETE, INSERT, SELECT, UPDATE ON public.employees TO authenticated;

GRANT DELETE, INSERT, SELECT, UPDATE ON public.employees TO service_role;