CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE OR REPLACE FUNCTION public.provision_employee_with_licenses(
    p_request_id VARCHAR,
    p_employee_id VARCHAR,
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_department VARCHAR,
    p_role VARCHAR,
    p_start_date DATE,
    p_employment_type VARCHAR,
    p_location VARCHAR,
    p_work_location VARCHAR,
    p_manager_id VARCHAR DEFAULT NULL,
    p_national_id VARCHAR DEFAULT NULL,
    p_shipping_address TEXT DEFAULT NULL,
    p_contact_phone VARCHAR DEFAULT NULL,
    p_medical_clearance_status BOOLEAN DEFAULT FALSE,
    p_product_ids VARCHAR[] DEFAULT ARRAY[]::VARCHAR[]
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_clean_first TEXT;
    v_clean_last TEXT;
    v_base_email TEXT;
    v_candidate_email TEXT;
    v_counter INT := 1;
    v_prod_id VARCHAR;
    v_total_seats BIGINT;
    v_assigned_seats BIGINT;
    v_new_assignment_id VARCHAR;
    v_assigned_licenses JSONB := '[]'::JSONB;
BEGIN
    -- 1. Generate normalized ASCII email and handle duplicates safely
    v_clean_first := lower(regexp_replace(unaccent(p_first_name), '[^a-zA-Z0-9]', '', 'g'));
    v_clean_last := lower(regexp_replace(unaccent(p_last_name), '[^a-zA-Z0-9]', '', 'g'));
    v_base_email := v_clean_first || '.' || v_clean_last;
    v_candidate_email := v_base_email || '@atossoftware.com';

    WHILE EXISTS (SELECT 1 FROM public.employees WHERE work_email = v_candidate_email) LOOP
        v_counter := v_counter + 1;
        v_candidate_email := v_base_email || v_counter::TEXT || '@atossoftware.com';
    END LOOP;

    -- 2. Insert Employee Record
    INSERT INTO public.employees (
        employee_id,
        onboarding_request_id,
        first_name,
        last_name,
        work_email,
        department,
        role,
        start_date,
        employment_type,
        location,
        work_location,
        manager_id,
        national_id,
        shipping_address,
        contact_phone,
        medical_clearance_status,
        status,
        updated_at
    ) VALUES (
        p_employee_id,
        p_request_id,
        p_first_name,
        p_last_name,
        v_candidate_email,
        p_department,
        p_role,
        p_start_date,
        p_employment_type,
        p_location,
        p_work_location,
        p_manager_id,
        p_national_id,
        p_shipping_address,
        p_contact_phone,
        p_medical_clearance_status,
        'active',
        NOW()
    );

    -- 3. Verify Seats & Insert License Assignments
    IF array_length(p_product_ids, 1) > 0 THEN
        FOREACH v_prod_id IN ARRAY p_product_ids LOOP
            -- Lock row for concurrency check
            SELECT total_seats INTO v_total_seats
            FROM public.software_products
            WHERE product_id = v_prod_id
            FOR UPDATE;

            IF NOT FOUND THEN
                RAISE EXCEPTION 'Software product % does not exist in catalog.', v_prod_id;
            END IF;

            -- Check active count against capacity (if seat limit is configured)
            IF v_total_seats IS NOT NULL THEN
                SELECT COUNT(*) INTO v_assigned_seats
                FROM public.license_assignments
                WHERE product_id = v_prod_id AND status = 'active';

                IF v_assigned_seats >= v_total_seats THEN
                    RAISE EXCEPTION 'Capacity exceeded for product %. Total seats: %, currently active: %.', 
                        v_prod_id, v_total_seats, v_assigned_seats;
                END IF;
            END IF;

            -- Insert license assignment
            v_new_assignment_id := 'LIC-' || upper(substr(md5(random()::text || clock_timestamp()::text), 1, 8));
            
            INSERT INTO public.license_assignments (
                assignment_id,
                employee_id,
                product_id,
                status,
                assigned_at,
                created_at,
                updated_at
            ) VALUES (
                v_new_assignment_id,
                p_employee_id,
                v_prod_id,
                'active',
                NOW(),
                NOW(),
                NOW()
            );

            v_assigned_licenses := v_assigned_licenses || jsonb_build_object(
                'assignment_id', v_new_assignment_id,
                'product_id', v_prod_id
            );
        END LOOP;
    END IF;

    RETURN jsonb_build_object(
        'success', true,
        'employee_id', p_employee_id,
        'work_email', v_candidate_email,
        'assignments', v_assigned_licenses
    );
END;
$$;