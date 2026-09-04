DELETE FROM public.product_assignment_rules r
WHERE r.role IS NOT NULL
  AND EXISTS (
      SELECT 1 
      FROM public.product_assignment_rules parent
      WHERE parent.role IS NULL
        AND parent.product_id = r.product_id
        AND parent.access_level = r.access_level
        AND parent.is_mandatory = r.is_mandatory
        AND parent.requires_approval = r.requires_approval
        AND (parent.department IS NULL OR parent.department = r.department)
  );