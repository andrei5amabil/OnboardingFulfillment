SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- \restrict OGVlIrDtnvLs0XcAphwAnuQ4F0OtPqXJBvWkM9S7d9fi1PWg6glBqXmxEYr2Sik

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
	('ONB-47E6F6D5', '2026-08-18 14:39:38.03218+00', 'EMP-0006', 'Son', 'Sonion', 'Software Engineering & Application Modernization', 'Junior Frontend Developer', '2026-08-18', 'full-time', 'Romania, Timisoara', 'remote', 'EMP-0042', '', 'pending_onboarding'),
	('ONB-3EF3CF0C', '2026-08-17 17:01:16.626444+00', 'EMP-0004', 'Eypee', 'Ai', 'it', 'Lead Backend Developer', '2026-08-27', 'full-time', 'Romania, Timisoara', 'remote', 'EMP-0042', '', 'pending_onboarding'),
	('ONB-0AD7EC13', '2026-08-17 20:03:39.698228+00', 'EMP-0005', 'Large L.', 'Model', 'it', 'Junior Frontend Developer', '2025-08-13', 'full-time', 'Romania, Timisoara', 'remote', 'EMP-0042', '', 'pending_onboarding'),
	('ONB-026590A0', '2026-08-17 16:21:35.279116+00', 'EMP-0003', 'Ionean', 'Gajat', 'engineering', 'Junior Backend Developer', '2026-08-27', 'full-time', 'Romania, Timisoara', 'remote', 'EMP-0042', '', 'pending_onboarding'),
	('ONB-001', '2026-08-17 16:14:07.080871+00', 'EMP-0002', 'Jack', 'Employee', 'IT', 'Helpdesk', '2026-08-28', 'full-time', 'Romania, Timisoara', 'hybrid', 'EMP-0042', NULL, 'pending_onboarding');


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."employees" ("employee_id", "created_at", "onboarding_request_id", "first_name", "last_name", "work_email", "department", "role", "start_date", "employment_type", "location", "work_location", "manager_id", "status", "updated_at") VALUES
	('EMP-0001', '2000-08-17 09:00:00+00', NULL, 'John', 'Atos', 'john.atos@atossoftware.com', 'Management', 'CEO', '2000-08-17', 'full-time', 'France, Paris', 'hybrid', NULL, 'active', '2026-08-17 16:10:28.090355+00'),
	('EMP-0042', '2000-08-25 18:00:00+00', NULL, 'Humanres', 'Ources', 'humanres.ources@atossoftware.com', 'hr', 'manager', '2001-09-05', 'full-time', 'France, Paris', 'on-site', NULL, 'active', '2026-08-17 16:17:13.122773+00');


--
-- PostgreSQL database dump complete
--

-- \unrestrict OGVlIrDtnvLs0XcAphwAnuQ4F0OtPqXJBvWkM9S7d9fi1PWg6glBqXmxEYr2Sik

RESET ALL;
