SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- \restrict JIWXu6qxDYyndTZILdQNrNMUN0zRUzQBpU6LAsLzh9g4mr1hV6hHHiFpVWNSBXd

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
	('ONB-47E6F6D5', '2026-08-18 14:39:38.03218+00', 'EMP-0006', 'Son', 'Sonion', 'Software Engineering & Application Modernization', 'Junior Frontend Developer', '2026-08-18', 'full-time', 'Romania, Timisoara', 'remote', 'EMP-0042', '', 'pending_onboarding');


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
	('R-SE-GWS-01', 'Software Engineering & Application Modernization', 'Junior Frontend Developer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-01', 'Software Engineering & Application Modernization', 'Junior Frontend Developer', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-GWS-02', 'Software Engineering & Application Modernization', 'Frontend Developer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-02', 'Software Engineering & Application Modernization', 'Frontend Developer', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-GWS-03', 'Software Engineering & Application Modernization', 'Senior Frontend Developer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-03', 'Software Engineering & Application Modernization', 'Senior Frontend Developer', 'PROD-JIR-01', 'admin', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-GWS-04', 'Software Engineering & Application Modernization', 'Junior Backend Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-04', 'Software Engineering & Application Modernization', 'Junior Backend Engineer', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-GWS-05', 'Software Engineering & Application Modernization', 'Backend Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-05', 'Software Engineering & Application Modernization', 'Backend Engineer', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-GWS-06', 'Software Engineering & Application Modernization', 'Senior Backend Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-06', 'Software Engineering & Application Modernization', 'Senior Backend Engineer', 'PROD-JIR-01', 'admin', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-GWS-07', 'Software Engineering & Application Modernization', 'Junior Full-Stack Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-07', 'Software Engineering & Application Modernization', 'Junior Full-Stack Engineer', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-GWS-08', 'Software Engineering & Application Modernization', 'Full-Stack Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-08', 'Software Engineering & Application Modernization', 'Full-Stack Engineer', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-GWS-09', 'Software Engineering & Application Modernization', 'Senior Full-Stack Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-09', 'Software Engineering & Application Modernization', 'Senior Full-Stack Engineer', 'PROD-JIR-01', 'admin', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-GWS-10', 'Software Engineering & Application Modernization', 'Lead Software Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-10', 'Software Engineering & Application Modernization', 'Lead Software Engineer', 'PROD-JIR-01', 'admin', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-GWS-11', 'Software Engineering & Application Modernization', 'Software Architect', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JIR-11', 'Software Engineering & Application Modernization', 'Software Architect', 'PROD-JIR-01', 'admin', true, false, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JET-01', 'Software Engineering & Application Modernization', 'Frontend Developer', 'PROD-JET-01', 'standard', true, true, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JET-02', 'Software Engineering & Application Modernization', 'Backend Engineer', 'PROD-JET-01', 'standard', true, true, '2026-08-20 16:33:31.621335+00'),
	('R-SE-JET-03', 'Software Engineering & Application Modernization', 'Full-Stack Engineer', 'PROD-JET-01', 'standard', true, true, '2026-08-20 16:33:31.621335+00'),
	('R-SE-AWS-01', 'Software Engineering & Application Modernization', 'Senior Backend Engineer', 'PROD-AWS-01', 'read-only', false, true, '2026-08-20 16:33:31.621335+00'),
	('R-SE-AWS-02', 'Software Engineering & Application Modernization', 'Lead Software Engineer', 'PROD-AWS-01', 'admin', false, true, '2026-08-20 16:33:31.621335+00'),
	('R-SE-AWS-03', 'Software Engineering & Application Modernization', 'Software Architect', 'PROD-AWS-01', 'admin', false, true, '2026-08-20 16:33:31.621335+00'),
	('R-CLD-100', 'Cloud Infrastructure & Platforms', 'Junior DevOps Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-101', 'Cloud Infrastructure & Platforms', 'Junior DevOps Engineer', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-102', 'Cloud Infrastructure & Platforms', 'Junior DevOps Engineer', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-103', 'Cloud Infrastructure & Platforms', 'Junior DevOps Engineer', 'PROD-GH-01', 'developer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-104', 'Cloud Infrastructure & Platforms', 'Junior DevOps Engineer', 'PROD-DOC-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-105', 'Cloud Infrastructure & Platforms', 'Junior DevOps Engineer', 'PROD-AWS-01', 'developer', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-106', 'Cloud Infrastructure & Platforms', 'Junior DevOps Engineer', 'PROD-DD-01', 'viewer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-107', 'Cloud Infrastructure & Platforms', 'DevOps Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-108', 'Cloud Infrastructure & Platforms', 'DevOps Engineer', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-109', 'Cloud Infrastructure & Platforms', 'DevOps Engineer', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-110', 'Cloud Infrastructure & Platforms', 'DevOps Engineer', 'PROD-GH-01', 'developer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-111', 'Cloud Infrastructure & Platforms', 'DevOps Engineer', 'PROD-DOC-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-112', 'Cloud Infrastructure & Platforms', 'DevOps Engineer', 'PROD-AWS-01', 'developer', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-113', 'Cloud Infrastructure & Platforms', 'DevOps Engineer', 'PROD-DD-01', 'viewer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-114', 'Cloud Infrastructure & Platforms', 'Senior DevOps Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-115', 'Cloud Infrastructure & Platforms', 'Senior DevOps Engineer', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-116', 'Cloud Infrastructure & Platforms', 'Senior DevOps Engineer', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-117', 'Cloud Infrastructure & Platforms', 'Senior DevOps Engineer', 'PROD-GH-01', 'developer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-118', 'Cloud Infrastructure & Platforms', 'Senior DevOps Engineer', 'PROD-DOC-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-119', 'Cloud Infrastructure & Platforms', 'Senior DevOps Engineer', 'PROD-AWS-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-120', 'Cloud Infrastructure & Platforms', 'Senior DevOps Engineer', 'PROD-DD-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-121', 'Cloud Infrastructure & Platforms', 'Junior Cloud Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-122', 'Cloud Infrastructure & Platforms', 'Junior Cloud Engineer', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-123', 'Cloud Infrastructure & Platforms', 'Junior Cloud Engineer', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-124', 'Cloud Infrastructure & Platforms', 'Junior Cloud Engineer', 'PROD-GH-01', 'developer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-125', 'Cloud Infrastructure & Platforms', 'Junior Cloud Engineer', 'PROD-DOC-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-126', 'Cloud Infrastructure & Platforms', 'Junior Cloud Engineer', 'PROD-AWS-01', 'developer', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-127', 'Cloud Infrastructure & Platforms', 'Junior Cloud Engineer', 'PROD-DD-01', 'viewer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-128', 'Cloud Infrastructure & Platforms', 'Cloud Solutions Architect', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-129', 'Cloud Infrastructure & Platforms', 'Cloud Solutions Architect', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-130', 'Cloud Infrastructure & Platforms', 'Cloud Solutions Architect', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-131', 'Cloud Infrastructure & Platforms', 'Cloud Solutions Architect', 'PROD-GH-01', 'developer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-132', 'Cloud Infrastructure & Platforms', 'Cloud Solutions Architect', 'PROD-DOC-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-133', 'Cloud Infrastructure & Platforms', 'Cloud Solutions Architect', 'PROD-AWS-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-134', 'Cloud Infrastructure & Platforms', 'Cloud Solutions Architect', 'PROD-DD-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-135', 'Cloud Infrastructure & Platforms', 'Site Reliability Engineer (SRE)', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-136', 'Cloud Infrastructure & Platforms', 'Site Reliability Engineer (SRE)', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-137', 'Cloud Infrastructure & Platforms', 'Site Reliability Engineer (SRE)', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-138', 'Cloud Infrastructure & Platforms', 'Site Reliability Engineer (SRE)', 'PROD-GH-01', 'developer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-139', 'Cloud Infrastructure & Platforms', 'Site Reliability Engineer (SRE)', 'PROD-DOC-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-140', 'Cloud Infrastructure & Platforms', 'Site Reliability Engineer (SRE)', 'PROD-AWS-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-141', 'Cloud Infrastructure & Platforms', 'Site Reliability Engineer (SRE)', 'PROD-DD-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-142', 'Cloud Infrastructure & Platforms', 'Systems Administrator', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-143', 'Cloud Infrastructure & Platforms', 'Systems Administrator', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-144', 'Cloud Infrastructure & Platforms', 'Systems Administrator', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-145', 'Cloud Infrastructure & Platforms', 'Systems Administrator', 'PROD-GH-01', 'developer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-146', 'Cloud Infrastructure & Platforms', 'Systems Administrator', 'PROD-DOC-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-147', 'Cloud Infrastructure & Platforms', 'Systems Administrator', 'PROD-AWS-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CLD-148', 'Cloud Infrastructure & Platforms', 'Systems Administrator', 'PROD-DD-01', 'admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-149', 'Cybersecurity & Digital Identity', 'Junior Security Analyst', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-150', 'Cybersecurity & Digital Identity', 'Junior Security Analyst', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-151', 'Cybersecurity & Digital Identity', 'Junior Security Analyst', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-152', 'Cybersecurity & Digital Identity', 'Junior Security Analyst', 'PROD-DD-01', 'viewer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-153', 'Cybersecurity & Digital Identity', 'SOC Analyst', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-154', 'Cybersecurity & Digital Identity', 'SOC Analyst', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-155', 'Cybersecurity & Digital Identity', 'SOC Analyst', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-156', 'Cybersecurity & Digital Identity', 'SOC Analyst', 'PROD-DD-01', 'viewer', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-157', 'Cybersecurity & Digital Identity', 'Cybersecurity Engineer', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-158', 'Cybersecurity & Digital Identity', 'Cybersecurity Engineer', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-159', 'Cybersecurity & Digital Identity', 'Cybersecurity Engineer', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-160', 'Cybersecurity & Digital Identity', 'Cybersecurity Engineer', 'PROD-DOC-01', 'standard', false, true, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-161', 'Cybersecurity & Digital Identity', 'Cybersecurity Engineer', 'PROD-AWS-01', 'auditor', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-162', 'Cybersecurity & Digital Identity', 'Penetration Tester', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-163', 'Cybersecurity & Digital Identity', 'Penetration Tester', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-164', 'Cybersecurity & Digital Identity', 'Penetration Tester', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-165', 'Cybersecurity & Digital Identity', 'Penetration Tester', 'PROD-DOC-01', 'standard', false, true, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-166', 'Cybersecurity & Digital Identity', 'Penetration Tester', 'PROD-AWS-01', 'auditor', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-167', 'Cybersecurity & Digital Identity', 'IAM Specialist', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-168', 'Cybersecurity & Digital Identity', 'IAM Specialist', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-169', 'Cybersecurity & Digital Identity', 'IAM Specialist', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-170', 'Cybersecurity & Digital Identity', 'IAM Specialist', 'PROD-AWS-01', 'security_admin', true, true, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-171', 'Cybersecurity & Digital Identity', 'GRC Consultant', 'PROD-GWS-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-172', 'Cybersecurity & Digital Identity', 'GRC Consultant', 'PROD-SLK-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-173', 'Cybersecurity & Digital Identity', 'GRC Consultant', 'PROD-JIR-01', 'user', true, false, '2026-08-20 16:40:43.380417+00'),
	('R-CYB-174', 'Cybersecurity & Digital Identity', 'GRC Consultant', 'PROD-M365-01', 'standard', true, false, '2026-08-20 16:40:43.380417+00');


--
-- PostgreSQL database dump complete
--

-- \unrestrict JIWXu6qxDYyndTZILdQNrNMUN0zRUzQBpU6LAsLzh9g4mr1hV6hHHiFpVWNSBXd

RESET ALL;
