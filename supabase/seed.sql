SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- \restrict qkGSrOfkMEnrezsqOChGhjZknpNUafcG8v4hxUUY6wI4RZMQgbe1sqMpKf3ByjA

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: onboarding_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."onboarding_requests" ("request_id", "created_at", "employee_id", "first_name", "last_name", "department", "role", "start_date", "employment_type", "location", "work_location", "hr_manager_id", "notes", "status", "manager_id", "shipping_address", "contact_phone", "medical_clearance_status", "national_id", "medical_clearance_date") VALUES
	('ONB-E0B5A2A2', '2026-09-21 14:47:34.627305+00', 'EMP-00000017', 'VLAD', 'POPESCU', 'Finance, Legal & Corporate Governance', 'Financial Analyst', '2026-10-19', 'full-time', 'Romania, Timisoara', 'remote', 'EMP-0042', '', 'completed', 'MGR-622', '70 Main Street, Suite 8, Amsterdam', '+40 748 930 975', true, '5030909241124', '2026-09-20'),
	('ONB-F9615152', '2026-09-18 18:40:07.276707+00', 'EMP-00000015', 'Chinezu', 'Moreno', 'Software Engineering & Application Modernization', 'Junior Frontend Developer', '2026-09-18', 'full-time', 'Romania, Timisoara', 'remote', 'EMP-0042', 'assign a Standard laptop', 'completed', NULL, NULL, NULL, false, NULL, NULL),
	('ONB-BC3E1E2C', '2026-09-21 13:40:28.21471+00', 'EMP-00000016', 'IONUT', 'DUMITRESCU', 'Data Analytics, AI & Business Intelligence', 'Data Engineer', '2026-10-12', 'full-time', 'Romania, Timisoara', 'on-site', 'EMP-0042', '', 'completed', 'MGR-731', '86 King''s Road, Suite 11, Amsterdam', '+40 767 500 957', true, '5031110343512', '2026-09-12');


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."employees" ("employee_id", "created_at", "onboarding_request_id", "first_name", "last_name", "work_email", "department", "role", "start_date", "employment_type", "location", "work_location", "manager_id", "status", "updated_at", "national_id", "shipping_address", "contact_phone", "medical_clearance_status") VALUES
	('EMP-0001', '2000-08-17 09:00:00+00', NULL, 'John', 'Atos', 'john.atos@atossoftware.com', 'Management', 'CEO', '2000-08-17', 'full-time', 'France, Paris', 'hybrid', NULL, 'active', '2026-08-17 16:10:28.090355+00', NULL, NULL, NULL, false),
	('EMP-0042', '2000-08-25 18:00:00+00', NULL, 'Humanres', 'Ources', 'humanres.ources@atossoftware.com', 'hr', 'manager', '2001-09-05', 'full-time', 'France, Paris', 'on-site', NULL, 'active', '2026-08-17 16:17:13.122773+00', NULL, NULL, NULL, false),
	('EMP-00000015', '2026-09-18 19:08:26.203678+00', 'ONB-F9615152', 'Chinezu', 'Moreno', 'chinezu.moreno@atossoftware.com', 'Software Engineering & Application Modernization', 'Junior Frontend Developer', '2026-09-18', 'full-time', 'Romania, Timisoara', 'remote', NULL, 'active', '2026-09-18 22:08:26.202583+00', NULL, NULL, NULL, false),
	('EMP-00000016', '2026-09-21 13:41:23.765981+00', 'ONB-BC3E1E2C', 'IONUT', 'DUMITRESCU', 'ionut.dumitrescu@atossoftware.com', 'Data Analytics, AI & Business Intelligence', 'Data Engineer', '2026-10-12', 'full-time', 'Romania, Timisoara', 'on-site', 'MGR-731', 'active', '2026-09-21 16:41:23.764861+00', NULL, NULL, NULL, false),
	('EMP-00000017', '2026-09-21 14:50:06.712578+00', 'ONB-E0B5A2A2', 'VLAD', 'POPESCU', 'vlad.popescu@atossoftware.com', 'Finance, Legal & Corporate Governance', 'Financial Analyst', '2026-10-19', 'full-time', 'Romania, Timisoara', 'remote', 'MGR-622', 'active', '2026-09-21 17:50:06.711474+00', '5030909241124', '70 Main Street, Suite 8, Amsterdam', '+40 748 930 975', true);


--
-- Data for Name: software_products; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."software_products" ("product_id", "vendor", "name", "license_type", "total_seats", "requires_approval", "created_at", "updated_at") VALUES
	('PROD-GWS-01', 'Google', 'Google Workspace', 'seat-based', 1000, false, '2026-08-20 16:32:30.89529+00', '2026-08-20 16:32:30.89529+00'),
	('PROD-JIR-01', 'Atlassian', 'Jira', 'seat-based', 500, false, '2026-08-20 16:32:30.89529+00', '2026-08-20 16:32:30.89529+00'),
	('PROD-JET-01', 'JetBrains', 'JetBrains All Products Pack', 'subscription', 200, true, '2026-08-20 16:32:30.89529+00', '2026-08-20 16:32:30.89529+00'),
	('PROD-AWS-01', 'Amazon', 'AWS IAM Console', 'usage-based', NULL, true, '2026-08-20 16:32:30.89529+00', '2026-08-20 16:32:30.89529+00'),
	('PROD-GH-01', 'GitHub', 'GitHub Enterprise', 'seat-based', 1000, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00'),
	('PROD-SLK-01', 'Slack', 'Slack Enterprise Grid', 'seat-based', 2000, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00'),
	('PROD-FIG-01', 'Figma', 'Figma Professional', 'seat-based', 100, true, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00'),
	('PROD-NOT-01', 'Notion', 'Notion Enterprise', 'seat-based', 1000, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00'),
	('PROD-DD-01', 'Datadog', 'Datadog APM', 'usage-based', NULL, true, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00'),
	('PROD-DOC-01', 'Docker', 'Docker Business', 'seat-based', 300, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00'),
	('PROD-ZOO-01', 'Zoom', 'Zoom One Pro', 'seat-based', 1500, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00'),
	('PROD-M365-01', 'Microsoft', 'Microsoft 365 E3', 'seat-based', 1000, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00'),
	('PROD-PBI-01', 'Microsoft', 'PowerBI Pro', 'seat-based', 100, true, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00'),
	('PROD-DGR-01', 'JetBrains', 'DataGrip', 'subscription', 50, true, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00');


--
-- Data for Name: license_assignments; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."license_assignments" ("assignment_id", "employee_id", "product_id", "status", "assigned_at", "revoked_at", "updated_at", "created_at") VALUES
	('LIC-CD462466', 'EMP-00000017', 'PROD-NOT-01', 'active', '2026-09-21 17:50:06.722279+00', NULL, '2026-09-21 17:50:06.722287+00', '2026-09-21 17:50:06.722286+00'),
	('LIC-3F9E1510', 'EMP-00000017', 'PROD-GWS-01', 'active', '2026-09-21 17:50:06.722292+00', NULL, '2026-09-21 17:50:06.722294+00', '2026-09-21 17:50:06.722293+00'),
	('LIC-8F982BF9', 'EMP-00000017', 'PROD-ZOO-01', 'active', '2026-09-21 17:50:06.722297+00', NULL, '2026-09-21 17:50:06.722298+00', '2026-09-21 17:50:06.722298+00'),
	('LIC-35D64D56', 'EMP-00000017', 'PROD-JIR-01', 'active', '2026-09-21 17:50:06.722301+00', NULL, '2026-09-21 17:50:06.722302+00', '2026-09-21 17:50:06.722302+00'),
	('LIC-E849D5C3', 'EMP-00000017', 'PROD-SLK-01', 'active', '2026-09-21 17:50:06.722305+00', NULL, '2026-09-21 17:50:06.722307+00', '2026-09-21 17:50:06.722306+00'),
	('LIC-32A6C475', 'EMP-00000015', 'PROD-GH-01', 'active', '2026-09-18 22:08:26.212277+00', NULL, '2026-09-18 22:08:26.212282+00', '2026-09-18 22:08:26.212281+00'),
	('LIC-EAC83A63', 'EMP-00000015', 'PROD-JIR-01', 'active', '2026-09-18 22:08:26.212288+00', NULL, '2026-09-18 22:08:26.21229+00', '2026-09-18 22:08:26.212289+00'),
	('LIC-85293487', 'EMP-00000015', 'PROD-SLK-01', 'active', '2026-09-18 22:08:26.212293+00', NULL, '2026-09-18 22:08:26.212295+00', '2026-09-18 22:08:26.212294+00'),
	('LIC-5F100261', 'EMP-00000015', 'PROD-DOC-01', 'active', '2026-09-18 22:08:26.212298+00', NULL, '2026-09-18 22:08:26.212299+00', '2026-09-18 22:08:26.212298+00'),
	('LIC-FC244458', 'EMP-00000015', 'PROD-FIG-01', 'active', '2026-09-18 22:08:26.212302+00', NULL, '2026-09-18 22:08:26.212303+00', '2026-09-18 22:08:26.212303+00'),
	('LIC-7A23E0DC', 'EMP-00000015', 'PROD-NOT-01', 'active', '2026-09-18 22:08:26.212306+00', NULL, '2026-09-18 22:08:26.212307+00', '2026-09-18 22:08:26.212307+00'),
	('LIC-C712653E', 'EMP-00000015', 'PROD-JET-01', 'active', '2026-09-18 22:08:26.21231+00', NULL, '2026-09-18 22:08:26.212311+00', '2026-09-18 22:08:26.212311+00'),
	('LIC-22D6EB32', 'EMP-00000015', 'PROD-GWS-01', 'active', '2026-09-18 22:08:26.212314+00', NULL, '2026-09-18 22:08:26.212316+00', '2026-09-18 22:08:26.212315+00'),
	('LIC-94760469', 'EMP-00000015', 'PROD-ZOO-01', 'active', '2026-09-18 22:08:26.212318+00', NULL, '2026-09-18 22:08:26.21232+00', '2026-09-18 22:08:26.212319+00'),
	('LIC-AD6AAEA7', 'EMP-00000016', 'PROD-ZOO-01', 'active', '2026-09-21 16:41:23.773778+00', NULL, '2026-09-21 16:41:23.773783+00', '2026-09-21 16:41:23.773782+00'),
	('LIC-DE76A6BA', 'EMP-00000016', 'PROD-SLK-01', 'active', '2026-09-21 16:41:23.773787+00', NULL, '2026-09-21 16:41:23.773789+00', '2026-09-21 16:41:23.773788+00'),
	('LIC-878805A2', 'EMP-00000016', 'PROD-JIR-01', 'active', '2026-09-21 16:41:23.773793+00', NULL, '2026-09-21 16:41:23.773795+00', '2026-09-21 16:41:23.773793+00'),
	('LIC-DA86B63F', 'EMP-00000016', 'PROD-GWS-01', 'active', '2026-09-21 16:41:23.773797+00', NULL, '2026-09-21 16:41:23.773799+00', '2026-09-21 16:41:23.773798+00'),
	('LIC-21E8A608', 'EMP-00000016', 'PROD-NOT-01', 'active', '2026-09-21 16:41:23.773801+00', NULL, '2026-09-21 16:41:23.773803+00', '2026-09-21 16:41:23.773802+00');


--
-- Data for Name: product_assignment_rules; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."product_assignment_rules" ("rule_id", "department", "role", "product_id", "access_level", "is_mandatory", "requires_approval", "created_at") VALUES
	('R-SE-JIR-03', 'Software Engineering & Application Modernization', 'Senior Frontend Developer', 'PROD-JIR-01', 'admin', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-06', 'Software Engineering & Application Modernization', 'Senior Backend Engineer', 'PROD-JIR-01', 'admin', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-09', 'Software Engineering & Application Modernization', 'Senior Full-Stack Engineer', 'PROD-JIR-01', 'admin', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-10', 'Software Engineering & Application Modernization', 'Lead Software Engineer', 'PROD-JIR-01', 'admin', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-11', 'Software Engineering & Application Modernization', 'Software Architect', 'PROD-JIR-01', 'admin', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-AWS-01', 'Software Engineering & Application Modernization', 'Senior Backend Engineer', 'PROD-AWS-01', 'read-only', false, true, '2026-08-20 16:33:31.621335+00'),
	('R-SE-AWS-02', 'Software Engineering & Application Modernization', 'Lead Software Engineer', 'PROD-AWS-01', 'admin', false, true, '2026-08-20 16:33:31.621335+00'),
	('R-SE-AWS-03', 'Software Engineering & Application Modernization', 'Software Architect', 'PROD-AWS-01', 'admin', false, true, '2026-08-20 16:33:31.621335+00'),
	('R-CLD-105', 'Cloud Infrastructure & Platforms', 'Junior DevOps Engineer', 'PROD-AWS-01', 'developer', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-106', 'Cloud Infrastructure & Platforms', 'Junior DevOps Engineer', 'PROD-DD-01', 'viewer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-112', 'Cloud Infrastructure & Platforms', 'DevOps Engineer', 'PROD-AWS-01', 'developer', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-113', 'Cloud Infrastructure & Platforms', 'DevOps Engineer', 'PROD-DD-01', 'viewer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-119', 'Cloud Infrastructure & Platforms', 'Senior DevOps Engineer', 'PROD-AWS-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-120', 'Cloud Infrastructure & Platforms', 'Senior DevOps Engineer', 'PROD-DD-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-126', 'Cloud Infrastructure & Platforms', 'Junior Cloud Engineer', 'PROD-AWS-01', 'developer', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-127', 'Cloud Infrastructure & Platforms', 'Junior Cloud Engineer', 'PROD-DD-01', 'viewer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-133', 'Cloud Infrastructure & Platforms', 'Cloud Solutions Architect', 'PROD-AWS-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-134', 'Cloud Infrastructure & Platforms', 'Cloud Solutions Architect', 'PROD-DD-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-140', 'Cloud Infrastructure & Platforms', 'Site Reliability Engineer (SRE)', 'PROD-AWS-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-141', 'Cloud Infrastructure & Platforms', 'Site Reliability Engineer (SRE)', 'PROD-DD-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-147', 'Cloud Infrastructure & Platforms', 'Systems Administrator', 'PROD-AWS-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-148', 'Cloud Infrastructure & Platforms', 'Systems Administrator', 'PROD-DD-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-161', 'Cybersecurity & Digital Identity', 'Cybersecurity Engineer', 'PROD-AWS-01', 'auditor', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-166', 'Cybersecurity & Digital Identity', 'Penetration Tester', 'PROD-AWS-01', 'auditor', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-170', 'Cybersecurity & Digital Identity', 'IAM Specialist', 'PROD-AWS-01', 'security_admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-174', 'Cybersecurity & Digital Identity', 'GRC Consultant', 'PROD-M365-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-GLB-001', NULL, NULL, 'PROD-GWS-01', 'standard', true, false, '2026-08-20 17:00:00+00'),
	('R-GLB-002', NULL, NULL, 'PROD-SLK-01', 'standard', true, false, '2026-08-20 17:00:00+00'),
	('R-GLB-003', NULL, NULL, 'PROD-JIR-01', 'user', true, false, '2026-08-20 17:00:00+00'),
	('R-GLB-004', NULL, NULL, 'PROD-ZOO-01', 'standard', true, false, '2026-08-20 17:00:00+00'),
	('R-GLB-005', NULL, NULL, 'PROD-NOT-01', 'standard', true, false, '2026-08-20 17:00:00+00'),
	('R-CLD-ALL-001', 'Cloud Infrastructure & Platforms', NULL, 'PROD-GH-01', 'developer', true, false, '2026-08-20 17:00:00+00'),
	('R-CLD-ALL-002', 'Cloud Infrastructure & Platforms', NULL, 'PROD-DOC-01', 'standard', true, false, '2026-08-20 17:00:00+00'),
	('R-SE-ALL-001', 'Software Engineering & Application Modernization', NULL, 'PROD-GH-01', 'developer', true, false, '2026-08-20 17:00:00+00'),
	('R-SE-ALL-002', 'Software Engineering & Application Modernization', NULL, 'PROD-DOC-01', 'standard', true, false, '2026-08-20 17:00:00+00'),
	('R-SE-ALL-003', 'Software Engineering & Application Modernization', NULL, 'PROD-JET-01', 'standard', true, true, '2026-08-20 17:00:00+00'),
	('R-CYB-ALL-001', 'Cybersecurity & Digital Identity', NULL, 'PROD-DD-01', 'viewer', true, false, '2026-08-20 17:00:00+00'),
	('R-CYB-ALL-002', 'Cybersecurity & Digital Identity', NULL, 'PROD-DOC-01', 'standard', false, true, '2026-08-20 17:00:00+00');


--
-- Data for Name: workflow_runs; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."workflow_runs" ("run_id", "request_id", "suggested_licenses", "suggested_hardware", "policy_citations", "it_notes", "reviewed_by", "created_at", "updated_at", "discretionary_licenses") VALUES
	(53, 'ONB-F9615152', '[{"rule_id": "R-GLB-001", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Google Workspace", "vendor": "Google", "product_id": "PROD-GWS-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Slack Enterprise Grid", "vendor": "Slack", "product_id": "PROD-SLK-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-003", "access_level": "user", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Jira", "vendor": "Atlassian", "product_id": "PROD-JIR-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-004", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Zoom One Pro", "vendor": "Zoom", "product_id": "PROD-ZOO-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-005", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Notion Enterprise", "vendor": "Notion", "product_id": "PROD-NOT-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-001", "access_level": "developer", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "GitHub Enterprise", "vendor": "GitHub", "product_id": "PROD-GH-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Docker Business", "vendor": "Docker", "product_id": "PROD-DOC-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-003", "access_level": "standard", "is_mandatory": true, "requires_approval": true, "software_products": {"name": "JetBrains All Products Pack", "vendor": "JetBrains", "product_id": "PROD-JET-01", "license_type": "subscription"}}]', '{"laptop": "Developer Workstation (high-performance)", "peripherals": ["external monitor", "dock", "keyboard", "mouse"], "shipping_required": false}', '[{"tags": ["HW-POLICY-001", "COMPLIANCE-DEP-002"], "raw_citations": [], "flagged_exceptions": []}]', NULL, 'EMP-IT-01', '2026-09-18 19:08:12.758552+00', '2026-09-18 22:08:26.228957+00', '[{"name": "Figma Professional", "product_id": "PROD-FIG-01", "justification": "IT reviewer feedback requests Figma Professional license for discretionary use."}]'),
	(54, 'ONB-BC3E1E2C', '[{"rule_id": "R-GLB-001", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Google Workspace", "vendor": "Google", "product_id": "PROD-GWS-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Slack Enterprise Grid", "vendor": "Slack", "product_id": "PROD-SLK-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-003", "access_level": "user", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Jira", "vendor": "Atlassian", "product_id": "PROD-JIR-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-004", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Zoom One Pro", "vendor": "Zoom", "product_id": "PROD-ZOO-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-005", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Notion Enterprise", "vendor": "Notion", "product_id": "PROD-NOT-01", "license_type": "seat-based"}}]', '{"laptop": "High-Performance Developer Workstation", "peripherals": ["external monitor", "dock", "keyboard", "mouse"], "shipping_required": false}', '[{"tags": ["POL-HDW-302", "POL-HDW-201", "POL-HDW-202", "POL-NET-201", "POL-NET-202", "POL-NET-203"], "raw_citations": [{"code": "Policy_HDW", "section": "3. Work Location Logistics"}, {"code": "Policy_HDW", "section": "2. Hardware Allocation Protocol"}, {"code": "Policy_NET", "section": "2. Network Segmentation & Enclave Access"}, {"code": "Policy_NET", "section": "1. Purpose & Scope"}], "flagged_exceptions": []}]', NULL, 'EMP-0042', '2026-09-21 13:41:05.980501+00', '2026-09-21 16:41:23.792441+00', '[]'),
	(57, 'ONB-E0B5A2A2', '[{"rule_id": "R-GLB-001", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Google Workspace", "vendor": "Google", "product_id": "PROD-GWS-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Slack Enterprise Grid", "vendor": "Slack", "product_id": "PROD-SLK-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-003", "access_level": "user", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Jira", "vendor": "Atlassian", "product_id": "PROD-JIR-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-004", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Zoom One Pro", "vendor": "Zoom", "product_id": "PROD-ZOO-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-005", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Notion Enterprise", "vendor": "Notion", "product_id": "PROD-NOT-01", "license_type": "seat-based"}}]', '{"laptop": "Standard Enterprise Laptop", "peripherals": ["external monitor", "USB keyboard", "USB mouse"], "shipping_required": false}', '[{"tags": ["POL-HDW-301", "POL-NET-301", "POL-NET-302"], "raw_citations": [{"code": "Policy_HDW", "section": "3. Work Location Logistics"}, {"code": "Policy_NET", "section": "3. Work Location & Tunnel Configuration"}, {"code": "Policy_NET", "section": "2. Network Segmentation & Enclave Access"}, {"code": "Policy_NET", "section": "1. Purpose & Scope"}], "flagged_exceptions": []}]', NULL, 'EMP-0042', '2026-09-21 14:49:55.24308+00', '2026-09-21 17:50:06.738827+00', '[]');


--
-- Name: workflow_runs_run_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."workflow_runs_run_id_seq"', 57, true);


--
-- PostgreSQL database dump complete
--

-- \unrestrict qkGSrOfkMEnrezsqOChGhjZknpNUafcG8v4hxUUY6wI4RZMQgbe1sqMpKf3ByjA

RESET ALL;
