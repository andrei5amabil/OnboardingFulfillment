import uuid
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.db.client import supabase

def run_verification():
    print("🚀 [1/3] Testing Happy Path Provisioning...")
    test_req_id = f"TEST-ONB-{uuid.uuid4().hex[:6].upper()}"
    test_emp_id = f"EMP-{uuid.uuid4().hex[:6].upper()}"

    # Fetch an existing product ID from software_products
    prod_res = supabase.table("software_products").select("product_id").limit(1).execute()
    test_prod_id = prod_res.data[0]["product_id"] if prod_res.data else None

    # 1. Test Happy Path
    payload = {
        "p_request_id": test_req_id,
        "p_employee_id": test_emp_id,
        "p_first_name": "Radu-Ștefan",
        "p_last_name": "Mureșan",
        "p_department": "Engineering",
        "p_role": "Backend Engineer",
        "p_start_date": "2026-11-01",
        "p_employment_type": "full-time",
        "p_location": "Romania",
        "p_work_location": "remote",
        "p_product_ids": [test_prod_id] if test_prod_id else [],
    }

    res = supabase.rpc("provision_employee_with_licenses", payload).execute()
    data = res.data
    print(f"   ✅ RPC Result: {data}")
    assert data.get("work_email") == "radustefan.muresan@atossoftware.com", f"Email normalization failed: {data.get('work_email')}"

    # Verify rows exist in DB
    emp_check = supabase.table("employees").select("*").eq("employee_id", test_emp_id).execute()
    assert len(emp_check.data) == 1, "Employee record not inserted."

    lic_check = supabase.table("license_assignments").select("*").eq("employee_id", test_emp_id).execute()
    if test_prod_id:
        assert len(lic_check.data) == 1, "License assignment not inserted."
    print("   ✅ Happy path verified.")

    # 2. Test Email Collision Suffix
    print("\n🚀 [2/3] Testing Email Collision Handling...")
    dup_emp_id = f"EMP-{uuid.uuid4().hex[:6].upper()}"
    payload["p_employee_id"] = dup_emp_id
    payload["p_request_id"] = f"TEST-ONB-{uuid.uuid4().hex[:6].upper()}"
    payload["p_product_ids"] = []

    dup_res = supabase.rpc("provision_employee_with_licenses", payload).execute()
    print(f"   ✅ Second candidate email: {dup_res.data.get('work_email')}")
    assert dup_res.data.get("work_email") == "radustefan.muresan2@atossoftware.com"

    # 3. Test Atomic Rollback on Capacity Exceeded
    print("\n🚀 [3/3] Testing Atomic Rollback on Zero-Seat Constraint...")
    fail_emp_id = f"EMP-{uuid.uuid4().hex[:6].upper()}"
    fail_req_id = f"TEST-ONB-{uuid.uuid4().hex[:6].upper()}"
    cap_prod_id = f"TEST-PROD-{uuid.uuid4().hex[:4].upper()}"

    # Insert a dummy product with total_seats = 0
    supabase.table("software_products").insert({
        "product_id": cap_prod_id,
        "name": f"Dummy Zero-Seat Tool {cap_prod_id}",
        "license_type": "seat-based",
        "total_seats": 0,
    }).execute()

    rollback_payload = {
        "p_request_id": fail_req_id,
        "p_employee_id": fail_emp_id,
        "p_first_name": "Fail",
        "p_last_name": "Candidate",
        "p_department": "Engineering",
        "p_role": "Tester",
        "p_start_date": "2026-11-01",
        "p_employment_type": "full-time",
        "p_location": "Romania",
        "p_work_location": "onsite",
        "p_product_ids": [cap_prod_id],
    }

    try:
        supabase.rpc("provision_employee_with_licenses", rollback_payload).execute()
        print("   ❌ FAILED: RPC should have raised a capacity exception!")
    except Exception as exc:
        print(f"   ✅ Expected exception caught: {exc}")

    # Confirm employee was NOT created (clean rollback)
    orphan_check = supabase.table("employees").select("*").eq("employee_id", fail_emp_id).execute()
    assert len(orphan_check.data) == 0, "Dirty state detected! Employee row exists despite failed transaction."
    print("   ✅ Transactional rollback verified: No dirty rows written to employees table.")

    # Cleanup test product
    supabase.table("software_products").delete().eq("product_id", cap_prod_id).execute()
    print("\n🎉 All database transactional properties passed successfully!")

if __name__ == "__main__":
    run_verification()