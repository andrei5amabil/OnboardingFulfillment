-- Migration unit 1: schema_changes
-- Transaction mode: transactional
-- Boundary reason: default

CREATE TABLE public.license_assignments (
  assignment_id character varying        NOT NULL,
  employee_id   character varying        NOT NULL,
  product_id    character varying        NOT NULL,
  status        character varying        DEFAULT 'active'::character varying NOT NULL,
  assigned_at   timestamp with time zone DEFAULT now() NOT NULL,
  revoked_at    timestamp with time zone,
  updated_at    timestamp with time zone DEFAULT now() NOT NULL,
  created_at    timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE public.license_assignments
  ADD CONSTRAINT license_assignments_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE public.license_assignments
  ADD CONSTRAINT license_assignments_pkey PRIMARY KEY (assignment_id);

GRANT ALL ON public.license_assignments TO anon;

GRANT ALL ON public.license_assignments TO authenticated;

GRANT ALL ON public.license_assignments TO service_role;

CREATE TABLE public.product_assignment_rules (
  rule_id           character varying        NOT NULL,
  department        character varying,
  role              character varying,
  product_id        character varying        NOT NULL,
  access_level      character varying        DEFAULT 'standard'::character varying NOT NULL,
  is_mandatory      boolean                  DEFAULT true NOT NULL,
  requires_approval boolean                  DEFAULT false NOT NULL,
  created_at        timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE public.product_assignment_rules
  ADD CONSTRAINT product_assignment_rules_pkey PRIMARY KEY (rule_id);

GRANT ALL ON public.product_assignment_rules TO anon;

GRANT ALL ON public.product_assignment_rules TO authenticated;

GRANT ALL ON public.product_assignment_rules TO service_role;

CREATE TABLE public.software_products (
  product_id        character varying        NOT NULL,
  vendor            character varying,
  name              character varying        NOT NULL,
  license_type      character varying        NOT NULL,
  total_seats       bigint,
  requires_approval boolean                  DEFAULT false NOT NULL,
  created_at        timestamp with time zone DEFAULT now() NOT NULL,
  updated_at        timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE public.software_products
  ADD CONSTRAINT software_products_name_key UNIQUE (name);

ALTER TABLE public.software_products
  ADD CONSTRAINT software_products_pkey PRIMARY KEY (product_id);

ALTER TABLE public.license_assignments
  ADD CONSTRAINT license_assignments_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.software_products(product_id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE public.product_assignment_rules
  ADD CONSTRAINT product_assignment_rules_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.software_products(product_id) ON UPDATE CASCADE ON DELETE CASCADE;

GRANT ALL ON public.software_products TO anon;

GRANT ALL ON public.software_products TO authenticated;

GRANT ALL ON public.software_products TO service_role;