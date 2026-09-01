Title: Enterprise IT Asset & Hardware Provisioning Standard
1. Purpose and Scope
1.1. This policy establishes the mandatory guidelines for the allocation, tracking, and reclamation of physical IT assets (laptops, peripherals, mobile devices).
1.2. Asset provisioning is strictly driven by the employee's role and designated work location as submitted in the approved HR onboarding request.  
2. Role-Based Hardware Allocation
2.1. Standardized Matrix: Hardware models are pre-determined based on department and computational requirements. For example, a "Data Analyst" role is mapped to receive a high-performance device (e.g., Laptop Dell XPS 15) to support intensive data processing tasks.
2.2. Deterministic Execution: The orchestration agent must format the requested hardware into the plan, which will be executed by the allocate_asset(emp_id, asset_type) deterministic tool.
2.3. Stock Verification: Before final execution, the system must cross-reference the required assets against the Inventory / IT Asset Records table in the Supabase structured data layer.  
3. Work Location Modifiers
3.1. Remote Employees: Employees designated with a "work_location": "remote" must be allocated a standard corporate laptop and a secure remote-worker peripheral bundle. The system must automatically generate a shipping ticket to the employee's provided address.
3.2. On-Site Employees: Employees assigned to a physical corporate office location will have their hardware routed to the local IT Helpdesk for desk setup prior to their start_date.  
4. Exception Handling & HITL Approval
4.1. Non-Standard Requests: Requests for supplementary hardware (e.g., additional monitors, specialized testing devices) not mapped to the baseline role require explicit justification.
4.2. IT Admin Oversight: The IT Admin must physically inspect the proposed hardware plan and verify the current stock of available hardware in the Human-in-the-Loop (HITL) Dashboard before clicking "Approve".
4.3. Stock Deficits: If a required asset is out of stock, the execution engine must halt the hardware provisioning phase, initiate a fallback alert to the SysAdmin, and mark the status as failed.  
5. Offboarding & Asset Reclamation
5.1. Inventory Reconciliation: Upon initiation of an offboarding request, the automated system must generate a complete inventory of all physical equipment assigned to the departing employee.
5.2. Asset Return Tasks: The system must automatically dispatch "Asset return tasks" to the employee and their manager, providing shipping labels or drop-off instructions based on their location.
5.3. Compliance Block: The final offboarding Compliance Report cannot be generated until the IT department marks the physical hardware as successfully received and wiped in the inventory database.  
