import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=True)

from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
# Service role key is required for auth.admin operations
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SECRET_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")

admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

USERS_TO_SEED = [
    {
        "email": "admin@atossoftware.com",
        "password": "Password123!",
        "role": "admin",
        "employee_id": "EMP-00000000",
        "first_name": "System",
        "last_name": "Administrator",
        "department": "IT",
        "job_role": "IT System Administrator",
    },
    {
        "email": "hr@atossoftware.com",
        "password": "Password123!",
        "role": "hr_manager",
        "employee_id": "EMP-00000042",
        "first_name": "Elena",
        "last_name": "Ionescu",
        "department": "People & Culture",
        "job_role": "HR Lead",
    },
    {
        "email": "it@atossoftware.com",
        "password": "Password123!",
        "role": "it_manager",
        "employee_id": "EMP-00000010",
        "first_name": "Mihai",
        "last_name": "Radu",
        "department": "IT Operations",
        "job_role": "IT Provisioning Lead",
    },
]

def seed_users():
    print("Seeding Enterprise Users & Auth Credentials...\n")

    for u in USERS_TO_SEED:
        print(f"Processing {u['role']} ({u['email']})...")

        # 1. Ensure employee record exists in public.employees
        emp_record = {
            "employee_id": u["employee_id"],
            "first_name": u["first_name"],
            "last_name": u["last_name"],
            "work_email": u["email"],
            "department": u["department"],
            "role": u["job_role"],
            "start_date": "2026-01-01",
            "employment_type": "full_time",
            "location": "Timișoara",
            "work_location": "onsite",
            "status": "active",
        }
        admin_client.table("employees").upsert(emp_record, on_conflict="employee_id").execute()

        # 2. Create or fetch auth identity in auth.users
        auth_id = None
        try:
            auth_user = admin_client.auth.admin.create_user({
                "email": u["email"],
                "password": u["password"],
                "email_confirm": True,
            })
            auth_id = auth_user.user.id
            print(f"Created auth.users entry (ID: {auth_id})")
        except Exception as e:
            err_str = str(e)
            if "already registered" in err_str or "already exists" in err_str:
                # Find existing user ID
                list_users = admin_client.auth.admin.list_users()
                for existing in list_users:
                    if existing.email == u["email"]:
                        auth_id = existing.id
                        break
                print(f"auth.users entry already exists (ID: {auth_id})")
            else:
                print(f"   ❌ Failed to create auth user: {e}")
                continue

        if not auth_id:
            continue

        # 3. Create or update public.users record
        profile_record = {
            "user_id": auth_id,
            "email": u["email"],
            "employee_id": u["employee_id"],
            "role": u["role"],
            "is_active": True,
        }
        admin_client.table("users").upsert(profile_record, on_conflict="user_id").execute()
        print(f"   ✅ Synchronized public.users profile with role '{u['role']}'")

    print("\nSeeding completed successfully.")

if __name__ == "__main__":
    seed_users()