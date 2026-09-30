SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- \restrict gquNArdCePZV1i8gqDyBmv614sHDM1CCt0swDKPhDTY8s4fqJf0YZufMBg4CEkl

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
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."audit_log_entries" ("instance_id", "id", "payload", "created_at", "ip_address") VALUES
	('00000000-0000-0000-0000-000000000000', 'a9e78e78-d32b-41fb-9ed3-5edb1d1166d2', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"jack.doe@atossoftware.com","user_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","user_phone":""}}', '2026-09-30 14:18:06.649877+00', ''),
	('00000000-0000-0000-0000-000000000000', '66545493-3385-4812-a434-e7e80efdc056', '{"action":"login","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2026-09-30 14:20:50.922507+00', ''),
	('00000000-0000-0000-0000-000000000000', 'ae7472a4-6843-48d9-9307-739e04fff2d2', '{"action":"logout","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"account"}', '2026-09-30 14:31:07.322334+00', ''),
	('00000000-0000-0000-0000-000000000000', '475cec17-d444-4dd3-9d4b-f862ef8d50b3', '{"action":"login","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2026-09-30 14:31:22.304018+00', ''),
	('00000000-0000-0000-0000-000000000000', '434ebf5d-8285-4f2e-b384-c07f6b055bcf', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-09-30 15:33:08.138208+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e1a4335b-fdd2-4966-8cc8-ee4efd908bad', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-09-30 15:33:08.138788+00', '');


--
-- Data for Name: custom_oauth_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."users" ("instance_id", "id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "invited_at", "confirmation_token", "confirmation_sent_at", "recovery_token", "recovery_sent_at", "email_change_token_new", "email_change", "email_change_sent_at", "last_sign_in_at", "raw_app_meta_data", "raw_user_meta_data", "is_super_admin", "created_at", "updated_at", "phone", "phone_confirmed_at", "phone_change", "phone_change_token", "phone_change_sent_at", "email_change_token_current", "email_change_confirm_status", "banned_until", "reauthentication_token", "reauthentication_sent_at", "is_sso_user", "deleted_at", "is_anonymous") VALUES
	('00000000-0000-0000-0000-000000000000', '1c2632b0-cb5a-41e0-b9a5-040a99396e85', 'authenticated', 'authenticated', 'jack.doe@atossoftware.com', '$2a$10$u.CqJeSNFb9DD2Wbvmh7guCaPCShBJnYqFvDzHvt9x3EPPnbn6Ity', '2026-09-30 14:18:06.650902+00', NULL, '', NULL, '', NULL, '', '', NULL, '2026-09-30 14:31:22.304906+00', '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-09-30 14:18:06.645756+00', '2026-09-30 15:33:08.13993+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false);


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."identities" ("provider_id", "user_id", "identity_data", "provider", "last_sign_in_at", "created_at", "updated_at", "id") VALUES
	('1c2632b0-cb5a-41e0-b9a5-040a99396e85', '1c2632b0-cb5a-41e0-b9a5-040a99396e85', '{"sub": "1c2632b0-cb5a-41e0-b9a5-040a99396e85", "email": "jack.doe@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-09-30 14:18:06.648849+00', '2026-09-30 14:18:06.648885+00', '2026-09-30 14:18:06.648885+00', 'd832770c-fe9f-4ad5-82a3-90e4a33a45cc');


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: oauth_clients; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."sessions" ("id", "user_id", "created_at", "updated_at", "factor_id", "aal", "not_after", "refreshed_at", "user_agent", "ip", "tag", "oauth_client_id", "refresh_token_hmac_key", "refresh_token_counter", "scopes") VALUES
	('6c69ef1f-2964-4ca1-804d-4b97725a75a3', '1c2632b0-cb5a-41e0-b9a5-040a99396e85', '2026-09-30 14:31:22.304952+00', '2026-09-30 15:33:08.140375+00', NULL, 'aal1', NULL, '2026-09-30 15:33:08.14034', 'Mozilla/5.0 (X11; Linux x86_64; rv:156.0) Gecko/20100101 Firefox/156.0', '172.19.0.1', NULL, NULL, NULL, NULL, NULL);


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."mfa_amr_claims" ("session_id", "created_at", "updated_at", "authentication_method", "id") VALUES
	('6c69ef1f-2964-4ca1-804d-4b97725a75a3', '2026-09-30 14:31:22.306549+00', '2026-09-30 14:31:22.306549+00', 'password', 'cb8b0389-efd1-4fa7-95a6-0a96e9e96af5');


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: oauth_authorizations; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: oauth_client_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: oauth_consents; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."refresh_tokens" ("instance_id", "id", "token", "user_id", "revoked", "created_at", "updated_at", "parent", "session_id") VALUES
	('00000000-0000-0000-0000-000000000000', 2, 'hznsa25ldr7n', '1c2632b0-cb5a-41e0-b9a5-040a99396e85', true, '2026-09-30 14:31:22.305869+00', '2026-09-30 15:33:08.139105+00', NULL, '6c69ef1f-2964-4ca1-804d-4b97725a75a3'),
	('00000000-0000-0000-0000-000000000000', 3, 'ouxm3plqs2z2', '1c2632b0-cb5a-41e0-b9a5-040a99396e85', false, '2026-09-30 15:33:08.139528+00', '2026-09-30 15:33:08.139528+00', 'hznsa25ldr7n', '6c69ef1f-2964-4ca1-804d-4b97725a75a3');


--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: webauthn_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: webauthn_credentials; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."employees" ("employee_id", "created_at", "onboarding_request_id", "first_name", "last_name", "work_email", "department", "role", "start_date", "employment_type", "location", "work_location", "manager_id", "status", "updated_at", "national_id", "shipping_address", "contact_phone", "medical_clearance_status") VALUES
	('EMP-0001', '2000-08-17 09:00:00+00', NULL, 'John', 'Atos', 'john.atos@atossoftware.com', 'Management', 'CEO', '2000-08-17', 'full-time', 'France, Paris', 'hybrid', NULL, 'active', '2026-08-17 16:10:28.090355+00', NULL, NULL, NULL, false),
	('EMP-0042', '2000-08-25 18:00:00+00', NULL, 'Humanres', 'Ources', 'humanres.ources@atossoftware.com', 'hr', 'manager', '2001-09-05', 'full-time', 'France, Paris', 'on-site', NULL, 'active', '2026-08-17 16:17:13.122773+00', NULL, NULL, NULL, false),
	('EMP-00000019', '2026-09-29 22:07:16.663967+00', 'ONB-65FCAEE9', 'Diana', 'Radu', 'diana.radu@atossoftware.com', 'Data Analytics, AI & Business Intelligence', 'Machine Learning Engineer', '2026-10-25', 'full-time', 'Romania, Timisoara', 'hybrid', 'MGR-897', 'active', '2026-09-30 01:07:16.663141+00', '6010616189766', '202 King''s Road, Suite 30, Timisoara', '+40 743 698 610', true),
	('EMP-IT-01', '2026-09-22 10:43:17+00', NULL, 'Torfals', 'Gentoo', 'torfals.gentoo@atossoftware.com', 'IT', 'Manager', '2026-09-30', 'full-time', 'Timisoara, Romania', 'onsite', 'EMP-IT-01', 'active', '2026-09-30 10:47:02.372285+00', '5050223450023', 'Cuca Macaii', '+40 756 678 223', true),
	('EMP-00000002', '2026-09-30 14:15:10+00', NULL, 'Jack', 'Doe', 'jack.doe@atossoftware.com', 'IT', 'Admin', '2026-09-16', 'full-time', 'Timisoara, Romania', 'remote', NULL, 'active', '2026-09-30 14:16:35+00', '500234126745', NULL, '+40234887659', true);


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
	('LIC-06C8C28B', 'EMP-00000019', 'PROD-ZOO-01', 'active', '2026-09-30 01:07:16.672337+00', NULL, '2026-09-30 01:07:16.672342+00', '2026-09-30 01:07:16.672341+00'),
	('LIC-381D755C', 'EMP-00000019', 'PROD-JIR-01', 'active', '2026-09-30 01:07:16.672347+00', NULL, '2026-09-30 01:07:16.672349+00', '2026-09-30 01:07:16.672348+00'),
	('LIC-8FF41101', 'EMP-00000019', 'PROD-SLK-01', 'active', '2026-09-30 01:07:16.672352+00', NULL, '2026-09-30 01:07:16.672354+00', '2026-09-30 01:07:16.672353+00'),
	('LIC-AA5EF941', 'EMP-00000019', 'PROD-GWS-01', 'active', '2026-09-30 01:07:16.672356+00', NULL, '2026-09-30 01:07:16.672358+00', '2026-09-30 01:07:16.672357+00'),
	('LIC-C67A9D5E', 'EMP-00000019', 'PROD-NOT-01', 'active', '2026-09-30 01:07:16.67236+00', NULL, '2026-09-30 01:07:16.672362+00', '2026-09-30 01:07:16.672361+00');


--
-- Data for Name: onboarding_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."onboarding_requests" ("request_id", "created_at", "employee_id", "first_name", "last_name", "department", "role", "start_date", "employment_type", "location", "work_location", "hr_manager_id", "notes", "status", "manager_id", "shipping_address", "contact_phone", "medical_clearance_status", "national_id", "medical_clearance_date", "extraction_time_seconds", "total_lead_time_seconds", "finalized_at") VALUES
	('ONB-65FCAEE9', '2026-09-29 22:03:58.031946+00', 'EMP-00000019', 'Diana', 'Radu', 'Data Analytics, AI & Business Intelligence', 'Machine Learning Engineer', '2026-10-25', 'full-time', 'Romania, Timisoara', 'hybrid', 'EMP-0042', NULL, 'completed', 'MGR-897', '202 King''s Road, Suite 30, Timisoara', '+40 743 698 610', true, '6010616189766', '2026-09-28', 0.00, 198.66, '2026-09-29 22:07:16.650699+00');


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
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."users" ("user_id", "email", "role", "employee_id", "is_active", "created_at", "updated_at") VALUES
	('1c2632b0-cb5a-41e0-b9a5-040a99396e85', 'jack.doe@atossoftware.com', 'admin', 'EMP-00000002', true, '2026-09-30 14:18:06.645554+00', '2026-09-30 14:20:27.961035+00');


--
-- Data for Name: workflow_runs; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."workflow_runs" ("run_id", "request_id", "suggested_licenses", "suggested_hardware", "policy_citations", "it_notes", "reviewed_by", "created_at", "updated_at", "discretionary_licenses", "execution_time_seconds", "tokens_prompt", "tokens_completion", "tokens_total", "attempt_number", "review_action", "reviewed_at") VALUES
	(60, 'ONB-65FCAEE9', '[{"rule_id": "R-GLB-001", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Google Workspace", "vendor": "Google", "product_id": "PROD-GWS-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Slack Enterprise Grid", "vendor": "Slack", "product_id": "PROD-SLK-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-003", "access_level": "user", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Jira", "vendor": "Atlassian", "product_id": "PROD-JIR-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-004", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Zoom One Pro", "vendor": "Zoom", "product_id": "PROD-ZOO-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-005", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Notion Enterprise", "vendor": "Notion", "product_id": "PROD-NOT-01", "license_type": "seat-based"}}]', '{"laptop": "High-Performance Developer Workstation", "peripherals": ["external monitor", "USB docking station"], "shipping_required": false}', '[{"tags": ["POL-HDW-302", "POL-HDW-201", "POL-HDW-202"], "raw_citations": [{"code": "Policy_HDW", "section": "3. Work Location Logistics"}, {"code": "Policy_HDW", "section": "2. Hardware Allocation Protocol"}, {"code": "Policy_NET", "section": "2. Network Segmentation & Enclave Access"}, {"code": "Policy_NET", "section": "1. Purpose & Scope"}], "flagged_exceptions": []}]', NULL, 'EMP-IT-01', '2026-09-29 22:04:39.704291+00', '2026-09-30 01:07:16.687445+00', '[]', 41.69, 892, 3881, 4773, 1, 'regenerate', '2026-09-29 22:05:33.096721+00'),
	(61, 'ONB-65FCAEE9', '[{"rule_id": "R-GLB-001", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Google Workspace", "vendor": "Google", "product_id": "PROD-GWS-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Slack Enterprise Grid", "vendor": "Slack", "product_id": "PROD-SLK-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-003", "access_level": "user", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Jira", "vendor": "Atlassian", "product_id": "PROD-JIR-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-004", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Zoom One Pro", "vendor": "Zoom", "product_id": "PROD-ZOO-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-005", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Notion Enterprise", "vendor": "Notion", "product_id": "PROD-NOT-01", "license_type": "seat-based"}}]', '{"laptop": "High-Performance Developer Laptop", "peripherals": ["External Monitor", "Docking Station", "Mechanical Keyboard", "Mouse"], "shipping_required": false}', '[{"tags": ["POL-HDW-302", "POL-NET-201", "POL-NET-202"], "raw_citations": [{"code": "Policy_HDW", "section": "3. Work Location Logistics"}, {"code": "Policy_HDW", "section": "2. Hardware Allocation Protocol"}, {"code": "Policy_NET", "section": "2. Network Segmentation & Enclave Access"}, {"code": "Policy_NET", "section": "1. Purpose & Scope"}], "flagged_exceptions": []}]', NULL, 'EMP-IT-01', '2026-09-29 22:05:59.305416+00', '2026-09-30 01:07:16.687445+00', '[{"name": "Figma Professional", "product_id": "PROD-FIG-01", "justification": "IT reviewer requested assigning a Figma Professional license to the employee."}]', 26.29, 2238, 6438, 8676, 2, 'approve', '2026-09-29 22:07:16.650699+00');


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 3, true);


--
-- Name: workflow_runs_run_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."workflow_runs_run_id_seq"', 61, true);


--
-- PostgreSQL database dump complete
--

-- \unrestrict gquNArdCePZV1i8gqDyBmv614sHDM1CCt0swDKPhDTY8s4fqJf0YZufMBg4CEkl

RESET ALL;
