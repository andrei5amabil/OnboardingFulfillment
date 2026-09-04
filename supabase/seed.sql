SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- \restrict AJq9uEUlQMLXuUazYWBzn2HFTLvtD5Ft6ZdUlyYEUFpVjhIGH6OgNzc8DRm8D9F

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

INSERT INTO "public"."onboarding_requests" ("request_id", "created_at", "employee_id", "first_name", "last_name", "department", "role", "start_date", "employment_type", "location", "work_location", "hr_manager_id", "notes", "status") VALUES
	('ONB-47E6F6D5', '2026-08-18 14:39:38.03218+00', 'EMP-0006', 'Son', 'Sonion', 'Software Engineering & Application Modernization', 'Junior Frontend Developer', '2026-08-18', 'full-time', 'Romania, Timisoara', 'remote', 'EMP-0042', '', 'generating_plan');


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."employees" ("employee_id", "created_at", "onboarding_request_id", "first_name", "last_name", "work_email", "department", "role", "start_date", "employment_type", "location", "work_location", "manager_id", "status", "updated_at") VALUES
	('EMP-0001', '2000-08-17 09:00:00+00', NULL, 'John', 'Atos', 'john.atos@atossoftware.com', 'Management', 'CEO', '2000-08-17', 'full-time', 'France, Paris', 'hybrid', NULL, 'active', '2026-08-17 16:10:28.090355+00'),
	('EMP-0042', '2000-08-25 18:00:00+00', NULL, 'Humanres', 'Ources', 'humanres.ources@atossoftware.com', 'hr', 'manager', '2001-09-05', 'full-time', 'France, Paris', 'on-site', NULL, 'active', '2026-08-17 16:17:13.122773+00');


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

INSERT INTO "public"."workflow_runs" ("run_id", "request_id", "suggested_licenses", "suggested_hardware", "policy_citations", "it_notes", "reviewed_by", "created_at", "updated_at") VALUES
	(23, 'ONB-47E6F6D5', '[{"rule_id": "R-GLB-001", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Google Workspace", "vendor": "Google", "product_id": "PROD-GWS-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Slack Enterprise Grid", "vendor": "Slack", "product_id": "PROD-SLK-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-003", "access_level": "user", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Jira", "vendor": "Atlassian", "product_id": "PROD-JIR-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-004", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Zoom One Pro", "vendor": "Zoom", "product_id": "PROD-ZOO-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-005", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Notion Enterprise", "vendor": "Notion", "product_id": "PROD-NOT-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-001", "access_level": "developer", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "GitHub Enterprise", "vendor": "GitHub", "product_id": "PROD-GH-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Docker Business", "vendor": "Docker", "product_id": "PROD-DOC-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-003", "access_level": "standard", "is_mandatory": true, "requires_approval": true, "software_products": {"name": "JetBrains All Products Pack", "vendor": "JetBrains", "product_id": "PROD-JET-01", "license_type": "subscription"}}]', '{}', '[]', NULL, NULL, '2026-09-04 23:26:36.803843+00', '2026-09-04 23:26:36.803843+00');


--
-- Name: workflow_runs_run_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."workflow_runs_run_id_seq"', 23, true);


--
-- PostgreSQL database dump complete
--

-- \unrestrict AJq9uEUlQMLXuUazYWBzn2HFTLvtD5Ft6ZdUlyYEUFpVjhIGH6OgNzc8DRm8D9F

RESET ALL;
