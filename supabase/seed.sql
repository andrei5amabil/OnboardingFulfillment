SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- \restrict SvUmNRh9TvAcon3R4IguJzCD2amtNJFyHeYYmKAHlSYCsyMbo0WP6cKE57M3o5G

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
	('00000000-0000-0000-0000-000000000000', 'e1a4335b-fdd2-4966-8cc8-ee4efd908bad', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-09-30 15:33:08.138788+00', ''),
	('00000000-0000-0000-0000-000000000000', 'dd256c07-d6ec-43cd-a850-728718fc42ef', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 16:10:17.220705+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b6ac0422-688a-4a55-874b-62f3d3948e79', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 16:10:17.221887+00', ''),
	('00000000-0000-0000-0000-000000000000', '23e9a7ea-fe34-4273-ab8e-f33cf3a7353a', '{"action":"logout","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"account"}', '2026-10-01 16:11:10.576126+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b6cf4b69-97a0-4c92-b662-310b5c5b6c0d', '{"action":"login","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2026-10-01 16:11:27.34489+00', ''),
	('00000000-0000-0000-0000-000000000000', '945e53e1-d000-4952-9d33-4d19a139a107', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 17:09:56.697383+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b4b83f10-15bb-4565-b5b5-fc9ad5d36dba', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 17:09:56.697991+00', ''),
	('00000000-0000-0000-0000-000000000000', '47443b71-163c-457c-8277-f07669da56e6', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 18:07:56.713175+00', ''),
	('00000000-0000-0000-0000-000000000000', '2622bfc6-99d6-456d-9360-0f738aa5f39f', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 18:07:56.713692+00', ''),
	('00000000-0000-0000-0000-000000000000', 'd80705f3-b8f0-4b47-98ec-eed3ba6f13fd', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 19:06:14.787432+00', ''),
	('00000000-0000-0000-0000-000000000000', '5615ceda-5cd4-4da1-b6df-b9293a34e000', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 19:06:14.787973+00', ''),
	('00000000-0000-0000-0000-000000000000', '5e2677de-1e50-48a9-bda6-5cd21e7f2ec0', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 20:06:50.577806+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a9d2bc18-eb5c-4e14-9449-2cad345d64ae', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 20:06:50.578047+00', ''),
	('00000000-0000-0000-0000-000000000000', '1a4a6a1b-fc9b-471e-94a0-45927704f786', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 21:19:00.22912+00', ''),
	('00000000-0000-0000-0000-000000000000', 'fa364bb0-e535-46a7-b06e-614ad9557f65', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-01 21:19:00.229356+00', ''),
	('00000000-0000-0000-0000-000000000000', '241b9b19-a1b5-4be6-b844-aa7bbedff63d', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-07 12:24:40.277464+00', ''),
	('00000000-0000-0000-0000-000000000000', '79a81b9b-5d79-4dce-8dd6-b2770d4b9f76', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-07 12:24:40.279953+00', ''),
	('00000000-0000-0000-0000-000000000000', '1ec756ca-6ecd-4001-835d-7cf4cb57a138', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-07 13:27:19.352798+00', ''),
	('00000000-0000-0000-0000-000000000000', '4a1d62dd-a422-430e-9e0c-e8b8130b8278', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-07 13:27:19.353192+00', ''),
	('00000000-0000-0000-0000-000000000000', '09a4fb04-e1d1-4fda-aef7-f0d1fbb2a586', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-07 15:09:37.47941+00', ''),
	('00000000-0000-0000-0000-000000000000', '09f4e2ac-5c68-4d24-93da-6927b90eddef', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-07 15:09:37.479641+00', ''),
	('00000000-0000-0000-0000-000000000000', '765e4b49-300e-4701-9a73-01a739b8b01e', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 10:00:49.196774+00', ''),
	('00000000-0000-0000-0000-000000000000', '14a7de09-eee4-4edf-8876-332b18ff55e7', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 10:00:49.197755+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a503e54e-05cc-4232-a6df-ba1d1b5015bd', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 11:03:04.817735+00', ''),
	('00000000-0000-0000-0000-000000000000', '4cfcc960-e696-4017-a4b5-86b10cc5f834', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 11:03:04.81798+00', ''),
	('00000000-0000-0000-0000-000000000000', 'ab2c9987-3546-4ac7-bc46-5783ab375d89', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 13:26:45.208237+00', ''),
	('00000000-0000-0000-0000-000000000000', '88dfb89a-f5f6-4860-897c-901f1f9f0d16', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 13:26:45.208801+00', ''),
	('00000000-0000-0000-0000-000000000000', '5a66fb9d-8d01-4f96-ba2b-931c2ab60794', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 14:24:45.292985+00', ''),
	('00000000-0000-0000-0000-000000000000', '61205760-11cd-449a-8a11-b98ebe22b942', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 14:24:45.293546+00', ''),
	('00000000-0000-0000-0000-000000000000', 'a0482d72-00ee-4d14-bb43-ad0584f85aec', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 15:37:28.83751+00', ''),
	('00000000-0000-0000-0000-000000000000', '67b5311d-5dd6-4900-9ab9-980cc113fad1', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 15:37:28.83806+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b0173941-86e0-492b-aeed-6ea1807e7c2d', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 16:36:03.047338+00', ''),
	('00000000-0000-0000-0000-000000000000', 'febf15d9-e806-46d6-8c34-524c967f81b2', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 16:36:03.047629+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b7110169-bd8e-4d6d-bcea-9aae71e0a2eb', '{"action":"token_refreshed","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 20:29:00.490791+00', ''),
	('00000000-0000-0000-0000-000000000000', '35c7f039-dedc-4b72-80f3-0a80ac3a1ded', '{"action":"token_revoked","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 20:29:00.492179+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e6845960-458d-40db-9406-c53bc118ba87', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"admin@atossoftware.com","user_id":"bc8e759e-9bc3-48f4-b422-224ffb55aa87","user_phone":""}}', '2026-10-14 20:33:36.513085+00', ''),
	('00000000-0000-0000-0000-000000000000', '8b5b4b03-9509-4cde-a3c9-8332fdb3fa93', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"hr@atossoftware.com","user_id":"130ca666-9628-413d-ab1b-a1d5e68ddb78","user_phone":""}}', '2026-10-14 20:33:36.605131+00', ''),
	('00000000-0000-0000-0000-000000000000', '2925957d-686e-46e4-b56b-d8859662752a', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"it@atossoftware.com","user_id":"3b8dccef-b084-49e0-81e3-c2a0962d1061","user_phone":""}}', '2026-10-14 20:33:36.695842+00', ''),
	('00000000-0000-0000-0000-000000000000', 'bfd2e258-29fc-46cc-b17e-2bb15dc363f4', '{"action":"logout","actor_id":"1c2632b0-cb5a-41e0-b9a5-040a99396e85","actor_username":"jack.doe@atossoftware.com","actor_via_sso":false,"log_type":"account"}', '2026-10-14 20:39:08.420814+00', ''),
	('00000000-0000-0000-0000-000000000000', '45e5e3b6-ed21-4962-9b59-60df77633f49', '{"action":"login","actor_id":"130ca666-9628-413d-ab1b-a1d5e68ddb78","actor_username":"hr@atossoftware.com","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2026-10-14 20:39:32.075678+00', ''),
	('00000000-0000-0000-0000-000000000000', '1bca58a6-eb8b-40b8-8c39-931120c3206e', '{"action":"logout","actor_id":"130ca666-9628-413d-ab1b-a1d5e68ddb78","actor_username":"hr@atossoftware.com","actor_via_sso":false,"log_type":"account"}', '2026-10-14 20:41:54.197061+00', ''),
	('00000000-0000-0000-0000-000000000000', 'e54dc581-0a0f-4298-96ec-55d1ff3e7fd4', '{"action":"login","actor_id":"3b8dccef-b084-49e0-81e3-c2a0962d1061","actor_username":"it@atossoftware.com","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2026-10-14 20:42:17.769157+00', ''),
	('00000000-0000-0000-0000-000000000000', '7db6daa4-0fb7-40d1-ae49-edf3fd2c57c4', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"mihai.stan@atossoftware.com","user_id":"3dd6e3e3-d467-4d0d-86c8-a9a7ab292f01","user_phone":""}}', '2026-10-14 20:42:58.914629+00', ''),
	('00000000-0000-0000-0000-000000000000', '7324de91-2dd9-4ecb-83ec-43dce25d57e5', '{"action":"logout","actor_id":"3b8dccef-b084-49e0-81e3-c2a0962d1061","actor_username":"it@atossoftware.com","actor_via_sso":false,"log_type":"account"}', '2026-10-14 20:43:25.730363+00', ''),
	('00000000-0000-0000-0000-000000000000', '84790085-9960-40f3-bd4b-fe584696e23f', '{"action":"login","actor_id":"3dd6e3e3-d467-4d0d-86c8-a9a7ab292f01","actor_username":"mihai.stan@atossoftware.com","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2026-10-14 20:43:54.463124+00', ''),
	('00000000-0000-0000-0000-000000000000', '52e032c6-34bb-4d8d-9835-962e302a1261', '{"action":"token_refreshed","actor_id":"3dd6e3e3-d467-4d0d-86c8-a9a7ab292f01","actor_username":"mihai.stan@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 21:42:36.006377+00', ''),
	('00000000-0000-0000-0000-000000000000', '88f8bc6e-b4c3-489a-b771-a9021add945e', '{"action":"token_revoked","actor_id":"3dd6e3e3-d467-4d0d-86c8-a9a7ab292f01","actor_username":"mihai.stan@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-14 21:42:36.006617+00', ''),
	('00000000-0000-0000-0000-000000000000', 'b3ada1de-c266-41d1-a62f-9fc018949537', '{"action":"token_refreshed","actor_id":"3dd6e3e3-d467-4d0d-86c8-a9a7ab292f01","actor_username":"mihai.stan@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-18 22:12:47.09218+00', ''),
	('00000000-0000-0000-0000-000000000000', '0aa1c452-6df7-4b3f-a9f5-17ba4c92aa6a', '{"action":"token_revoked","actor_id":"3dd6e3e3-d467-4d0d-86c8-a9a7ab292f01","actor_username":"mihai.stan@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-18 22:12:47.094315+00', ''),
	('00000000-0000-0000-0000-000000000000', 'c34a5457-fcf3-47af-a85f-91d79b8d015a', '{"action":"logout","actor_id":"3dd6e3e3-d467-4d0d-86c8-a9a7ab292f01","actor_username":"mihai.stan@atossoftware.com","actor_via_sso":false,"log_type":"account"}', '2026-10-18 22:12:53.669581+00', ''),
	('00000000-0000-0000-0000-000000000000', '464ce53a-95f1-438a-9414-d8dcfe075881', '{"action":"login","actor_id":"bc8e759e-9bc3-48f4-b422-224ffb55aa87","actor_username":"admin@atossoftware.com","actor_via_sso":false,"log_type":"account","traits":{"provider":"email"}}', '2026-10-18 22:14:43.155185+00', ''),
	('00000000-0000-0000-0000-000000000000', '34524968-d769-48c7-abc1-19c9dec4c2ef', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"laura.stoica@atossoftware.com","user_id":"1ce4f979-96e0-45ce-8770-54569df5698f","user_phone":""}}', '2026-10-18 22:16:13.652731+00', ''),
	('00000000-0000-0000-0000-000000000000', '3c4bfa6a-cbb5-47fe-9ffd-b3dc88d386d3', '{"action":"token_refreshed","actor_id":"bc8e759e-9bc3-48f4-b422-224ffb55aa87","actor_username":"admin@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-19 21:27:34.479959+00', ''),
	('00000000-0000-0000-0000-000000000000', '54099a28-ff3a-4779-a72f-a84e36e2bd5d', '{"action":"token_revoked","actor_id":"bc8e759e-9bc3-48f4-b422-224ffb55aa87","actor_username":"admin@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-19 21:27:34.483533+00', ''),
	('00000000-0000-0000-0000-000000000000', '096393d7-e471-4315-b24e-b6b37fbeb205', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"laura.dumitrescu@atossoftware.com","user_id":"b8a6f75b-bffa-4c7f-bd0d-18eace0847b8","user_phone":""}}', '2026-10-19 21:30:51.639807+00', ''),
	('00000000-0000-0000-0000-000000000000', '9d60ebc1-9b00-48eb-b16a-a8f99a5206cc', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"stefan.radu@atossoftware.com","user_id":"64268d01-ff9c-48b9-b344-46aeaef3ecbe","user_phone":""}}', '2026-10-19 21:33:45.099075+00', ''),
	('00000000-0000-0000-0000-000000000000', '1ba5797b-2043-4acc-9d25-4710cabe79bf', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"radu.ionescu@atossoftware.com","user_id":"aa04e19a-8ade-4f27-ab84-91200fd7770f","user_phone":""}}', '2026-10-19 21:45:54.880169+00', ''),
	('00000000-0000-0000-0000-000000000000', '5de696a1-f358-4176-8447-a8923fb61ca3', '{"action":"token_refreshed","actor_id":"bc8e759e-9bc3-48f4-b422-224ffb55aa87","actor_username":"admin@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-20 09:31:30.616248+00', ''),
	('00000000-0000-0000-0000-000000000000', 'c463fe64-dd4e-4ae4-bfd4-d2cb647356b9', '{"action":"token_revoked","actor_id":"bc8e759e-9bc3-48f4-b422-224ffb55aa87","actor_username":"admin@atossoftware.com","actor_via_sso":false,"log_type":"token"}', '2026-10-20 09:31:30.617659+00', ''),
	('00000000-0000-0000-0000-000000000000', '3bde7180-dccd-4a00-b2f3-428c1847c59d', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"roxana.dumitrescu@atossoftware.com","user_id":"31531e2e-6618-4183-91d7-3f510092fb42","user_phone":""}}', '2026-10-20 09:33:47.356373+00', ''),
	('00000000-0000-0000-0000-000000000000', '9f86f9ff-8683-40fc-8285-249b435d0ef8', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"maria.dumitrescu@atossoftware.com","user_id":"fe032f51-f06c-48ae-b961-74b4e586e488","user_phone":""}}', '2026-10-20 09:40:46.797418+00', ''),
	('00000000-0000-0000-0000-000000000000', 'ebd8414b-1f4b-4f55-8271-ed1c770c796a', '{"action":"user_signedup","actor_id":"00000000-0000-0000-0000-000000000000","actor_username":"service_role","actor_via_sso":false,"log_type":"team","traits":{"provider":"email","user_email":"roxana.gheorghe@atossoftware.com","user_id":"030b9a08-e309-4b98-8df0-68cd76b5faa1","user_phone":""}}', '2026-10-20 10:10:13.552397+00', '');


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
	('00000000-0000-0000-0000-000000000000', '1c2632b0-cb5a-41e0-b9a5-040a99396e85', 'authenticated', 'authenticated', 'jack.doe@atossoftware.com', '$2a$10$u.CqJeSNFb9DD2Wbvmh7guCaPCShBJnYqFvDzHvt9x3EPPnbn6Ity', '2026-09-30 14:18:06.650902+00', NULL, '', NULL, '', NULL, '', '', NULL, '2026-10-01 16:11:27.345656+00', '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-09-30 14:18:06.645756+00', '2026-10-14 20:29:00.4942+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', '1ce4f979-96e0-45ce-8770-54569df5698f', 'authenticated', 'authenticated', 'laura.stoica@atossoftware.com', '$2a$10$/JN24iDJgRI.p/dIGiwvHeOqaE.JqtOlv0yeZ23kZedzKIyZgs7qu', '2026-10-18 22:16:13.653602+00', NULL, '', NULL, '', NULL, '', '', NULL, NULL, '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-10-18 22:16:13.647579+00', '2026-10-18 22:16:13.65408+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', '31531e2e-6618-4183-91d7-3f510092fb42', 'authenticated', 'authenticated', 'roxana.dumitrescu@atossoftware.com', '$2a$10$4bFFNPmy0RL.d6WNfOFwEOU8m14ZY6rJNvoo9MHOtlMh4fGHPIpo2', '2026-10-20 09:33:47.356791+00', NULL, '', NULL, '', NULL, '', '', NULL, NULL, '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-10-20 09:33:47.352035+00', '2026-10-20 09:33:47.35707+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', 'b8a6f75b-bffa-4c7f-bd0d-18eace0847b8', 'authenticated', 'authenticated', 'laura.dumitrescu@atossoftware.com', '$2a$10$RHptHAjmgBy9oFf2HdhSwuy0POCeyo.tov4lkuHFogixg9iQPK2su', '2026-10-19 21:30:51.640244+00', NULL, '', NULL, '', NULL, '', '', NULL, NULL, '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-10-19 21:30:51.637208+00', '2026-10-19 21:30:51.640519+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', '130ca666-9628-413d-ab1b-a1d5e68ddb78', 'authenticated', 'authenticated', 'hr@atossoftware.com', '$2a$10$gtxqW5KEjXlfSGlmADqHneqJiF5yUST5cwY5z9/xtZwEmMexp1RL.', '2026-10-14 20:33:36.605637+00', NULL, '', NULL, '', NULL, '', '', NULL, '2026-10-14 20:39:32.07653+00', '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-10-14 20:33:36.603087+00', '2026-10-14 20:39:32.07884+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', '3b8dccef-b084-49e0-81e3-c2a0962d1061', 'authenticated', 'authenticated', 'it@atossoftware.com', '$2a$10$T0RKtljBfPhYlHkdxN7Lt.mCxGqkDUcxN2z76q6Ty0HZQhEsxomhS', '2026-10-14 20:33:36.696635+00', NULL, '', NULL, '', NULL, '', '', NULL, '2026-10-14 20:42:17.769641+00', '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-10-14 20:33:36.692579+00', '2026-10-14 20:42:17.770953+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', 'fe032f51-f06c-48ae-b961-74b4e586e488', 'authenticated', 'authenticated', 'maria.dumitrescu@atossoftware.com', '$2a$10$QdAMwlLMoItXntpFj38qkOsY5OSja78ejP0MAi9m3qAgt8rbrL9By', '2026-10-20 09:40:46.798309+00', NULL, '', NULL, '', NULL, '', '', NULL, NULL, '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-10-20 09:40:46.79411+00', '2026-10-20 09:40:46.798782+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', '64268d01-ff9c-48b9-b344-46aeaef3ecbe', 'authenticated', 'authenticated', 'stefan.radu@atossoftware.com', '$2a$10$ngy3Nog6uQDPt827KV/Eme87eAp88Xwvg.8bKBDfhzKelgegw47Qi', '2026-10-19 21:33:45.100077+00', NULL, '', NULL, '', NULL, '', '', NULL, NULL, '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-10-19 21:33:45.09595+00', '2026-10-19 21:33:45.100596+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', '3dd6e3e3-d467-4d0d-86c8-a9a7ab292f01', 'authenticated', 'authenticated', 'mihai.stan@atossoftware.com', '$2a$10$EhpTylMJxXzu176s7R2M/.AHApfcEqET5xB6dxDN9zbubW9vJXdvi', '2026-10-14 20:42:58.914995+00', NULL, '', NULL, '', NULL, '', '', NULL, '2026-10-14 20:43:54.464024+00', '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-10-14 20:42:58.912741+00', '2026-10-18 22:12:47.096651+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', 'aa04e19a-8ade-4f27-ab84-91200fd7770f', 'authenticated', 'authenticated', 'radu.ionescu@atossoftware.com', '$2a$10$/D917SdZeMxmaNcAlT/xg.dw2ZgdvkKXuhGYFl42QE8h1WjyVdqN6', '2026-10-19 21:45:54.881168+00', NULL, '', NULL, '', NULL, '', '', NULL, NULL, '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-10-19 21:45:54.877857+00', '2026-10-19 21:45:54.881673+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', 'bc8e759e-9bc3-48f4-b422-224ffb55aa87', 'authenticated', 'authenticated', 'admin@atossoftware.com', '$2a$10$Yuf8st7bq4cT9qlJGVma2e2wL0awYgaILEAFd6h7cEFqFeygjzvyK', '2026-10-14 20:33:36.513999+00', NULL, '', NULL, '', NULL, '', '', NULL, '2026-10-18 22:14:43.156018+00', '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-10-14 20:33:36.510615+00', '2026-10-20 09:31:30.619332+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false),
	('00000000-0000-0000-0000-000000000000', '030b9a08-e309-4b98-8df0-68cd76b5faa1', 'authenticated', 'authenticated', 'roxana.gheorghe@atossoftware.com', '$2a$10$KFnLiFK6vN7IBdgeHHlhluD1iobhqxjmFLUNcAwjyEl.p2rEq0dv2', '2026-10-20 10:10:13.55285+00', NULL, '', NULL, '', NULL, '', '', NULL, NULL, '{"provider": "email", "providers": ["email"]}', '{"email_verified": true}', NULL, '2026-10-20 10:10:13.549734+00', '2026-10-20 10:10:13.553145+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL, false);


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."identities" ("provider_id", "user_id", "identity_data", "provider", "last_sign_in_at", "created_at", "updated_at", "id") VALUES
	('1c2632b0-cb5a-41e0-b9a5-040a99396e85', '1c2632b0-cb5a-41e0-b9a5-040a99396e85', '{"sub": "1c2632b0-cb5a-41e0-b9a5-040a99396e85", "email": "jack.doe@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-09-30 14:18:06.648849+00', '2026-09-30 14:18:06.648885+00', '2026-09-30 14:18:06.648885+00', 'd832770c-fe9f-4ad5-82a3-90e4a33a45cc'),
	('bc8e759e-9bc3-48f4-b422-224ffb55aa87', 'bc8e759e-9bc3-48f4-b422-224ffb55aa87', '{"sub": "bc8e759e-9bc3-48f4-b422-224ffb55aa87", "email": "admin@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-10-14 20:33:36.512704+00', '2026-10-14 20:33:36.512726+00', '2026-10-14 20:33:36.512726+00', '28071492-8654-460f-93e8-ae193d7504b6'),
	('130ca666-9628-413d-ab1b-a1d5e68ddb78', '130ca666-9628-413d-ab1b-a1d5e68ddb78', '{"sub": "130ca666-9628-413d-ab1b-a1d5e68ddb78", "email": "hr@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-10-14 20:33:36.604662+00', '2026-10-14 20:33:36.604683+00', '2026-10-14 20:33:36.604683+00', '0f06de15-fca6-4595-acf1-5e32d7f5261a'),
	('3b8dccef-b084-49e0-81e3-c2a0962d1061', '3b8dccef-b084-49e0-81e3-c2a0962d1061', '{"sub": "3b8dccef-b084-49e0-81e3-c2a0962d1061", "email": "it@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-10-14 20:33:36.695212+00', '2026-10-14 20:33:36.695241+00', '2026-10-14 20:33:36.695241+00', '84540457-cdc8-4640-8a16-1818f712a204'),
	('3dd6e3e3-d467-4d0d-86c8-a9a7ab292f01', '3dd6e3e3-d467-4d0d-86c8-a9a7ab292f01', '{"sub": "3dd6e3e3-d467-4d0d-86c8-a9a7ab292f01", "email": "mihai.stan@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-10-14 20:42:58.914291+00', '2026-10-14 20:42:58.914307+00', '2026-10-14 20:42:58.914307+00', '90efac02-f416-4b56-92e4-e2b112d44436'),
	('1ce4f979-96e0-45ce-8770-54569df5698f', '1ce4f979-96e0-45ce-8770-54569df5698f', '{"sub": "1ce4f979-96e0-45ce-8770-54569df5698f", "email": "laura.stoica@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-10-18 22:16:13.651578+00', '2026-10-18 22:16:13.651606+00', '2026-10-18 22:16:13.651606+00', '9c561a78-5a9d-41bf-8f3f-0d8596ed16a3'),
	('b8a6f75b-bffa-4c7f-bd0d-18eace0847b8', 'b8a6f75b-bffa-4c7f-bd0d-18eace0847b8', '{"sub": "b8a6f75b-bffa-4c7f-bd0d-18eace0847b8", "email": "laura.dumitrescu@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-10-19 21:30:51.639382+00', '2026-10-19 21:30:51.639405+00', '2026-10-19 21:30:51.639405+00', '9cd4e09f-03cd-40e6-8403-50f8afa14ab1'),
	('64268d01-ff9c-48b9-b344-46aeaef3ecbe', '64268d01-ff9c-48b9-b344-46aeaef3ecbe', '{"sub": "64268d01-ff9c-48b9-b344-46aeaef3ecbe", "email": "stefan.radu@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-10-19 21:33:45.098474+00', '2026-10-19 21:33:45.098507+00', '2026-10-19 21:33:45.098507+00', '8a8ad802-960f-4229-8c4c-3611ee6fbe47'),
	('aa04e19a-8ade-4f27-ab84-91200fd7770f', 'aa04e19a-8ade-4f27-ab84-91200fd7770f', '{"sub": "aa04e19a-8ade-4f27-ab84-91200fd7770f", "email": "radu.ionescu@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-10-19 21:45:54.879503+00', '2026-10-19 21:45:54.879526+00', '2026-10-19 21:45:54.879526+00', 'bd7c7436-9938-42f1-9d7e-354b96d3e95b'),
	('31531e2e-6618-4183-91d7-3f510092fb42', '31531e2e-6618-4183-91d7-3f510092fb42', '{"sub": "31531e2e-6618-4183-91d7-3f510092fb42", "email": "roxana.dumitrescu@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-10-20 09:33:47.355742+00', '2026-10-20 09:33:47.355766+00', '2026-10-20 09:33:47.355766+00', '372def9e-ab52-4656-baef-3dcf3e08ba7c'),
	('fe032f51-f06c-48ae-b961-74b4e586e488', 'fe032f51-f06c-48ae-b961-74b4e586e488', '{"sub": "fe032f51-f06c-48ae-b961-74b4e586e488", "email": "maria.dumitrescu@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-10-20 09:40:46.79679+00', '2026-10-20 09:40:46.796825+00', '2026-10-20 09:40:46.796825+00', '9930401e-2d6f-4efe-9b04-823e08eb8f18'),
	('030b9a08-e309-4b98-8df0-68cd76b5faa1', '030b9a08-e309-4b98-8df0-68cd76b5faa1', '{"sub": "030b9a08-e309-4b98-8df0-68cd76b5faa1", "email": "roxana.gheorghe@atossoftware.com", "email_verified": false, "phone_verified": false}', 'email', '2026-10-20 10:10:13.552039+00', '2026-10-20 10:10:13.552062+00', '2026-10-20 10:10:13.552062+00', '091ae7ab-6f4e-4c66-9604-e7b67c820ae4');


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
	('1aa9617a-bfb5-4c2b-af7b-2539b81b4b7e', 'bc8e759e-9bc3-48f4-b422-224ffb55aa87', '2026-10-18 22:14:43.156095+00', '2026-10-20 09:31:30.620646+00', NULL, 'aal1', NULL, '2026-10-20 09:31:30.620605', 'Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0', '172.19.0.1', NULL, NULL, NULL, NULL, NULL);


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO "auth"."mfa_amr_claims" ("session_id", "created_at", "updated_at", "authentication_method", "id") VALUES
	('1aa9617a-bfb5-4c2b-af7b-2539b81b4b7e', '2026-10-18 22:14:43.159268+00', '2026-10-18 22:14:43.159268+00', 'password', '874d7afe-727e-436a-9c44-a78442374248');


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
	('00000000-0000-0000-0000-000000000000', 26, 'edq6kmota7ss', 'bc8e759e-9bc3-48f4-b422-224ffb55aa87', true, '2026-10-18 22:14:43.158086+00', '2026-10-19 21:27:34.483682+00', NULL, '1aa9617a-bfb5-4c2b-af7b-2539b81b4b7e'),
	('00000000-0000-0000-0000-000000000000', 27, 'hodcphwtrsk3', 'bc8e759e-9bc3-48f4-b422-224ffb55aa87', true, '2026-10-19 21:27:34.484322+00', '2026-10-20 09:31:30.617829+00', 'edq6kmota7ss', '1aa9617a-bfb5-4c2b-af7b-2539b81b4b7e'),
	('00000000-0000-0000-0000-000000000000', 28, 'a6eopxmbhonx', 'bc8e759e-9bc3-48f4-b422-224ffb55aa87', false, '2026-10-20 09:31:30.618137+00', '2026-10-20 09:31:30.618137+00', 'hodcphwtrsk3', '1aa9617a-bfb5-4c2b-af7b-2539b81b4b7e');


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
	('EMP-IT-01', '2026-09-22 10:43:17+00', NULL, 'Torfals', 'Gentoo', 'torfals.gentoo@atossoftware.com', 'IT', 'Manager', '2026-09-30', 'full-time', 'Timisoara, Romania', 'onsite', 'EMP-IT-01', 'active', '2026-09-30 10:47:02.372285+00', '5050223450023', 'Cuca Macaii', '+40 756 678 223', true),
	('EMP-00000043', '2026-10-19 21:45:54.8007+00', 'ONB-8742A11D', 'Radu', 'Ionescu', 'radu.ionescu@atossoftware.com', 'Software Engineering & Application Modernization', 'Backend Engineer', '2026-11-14', 'full-time', 'Romania, Timisoara', 'remote', 'EMP-0042', 'active', '2026-10-19 21:45:54.8007+00', '5000321165441', '34 Innovation Way, Suite 31, London', '+40 748 878 133', true),
	('EMP-00000044', '2026-10-20 09:33:47.266312+00', 'ONB-42DD7B05', 'Roxana', 'Dumitrescu', 'roxana.dumitrescu@atossoftware.com', 'Software Engineering & Application Modernization', 'Backend Engineer', '2026-11-07', 'full-time', 'Romania, Timisoara', 'on-site', 'EMP-0042', 'active', '2026-10-20 09:33:47.266312+00', '6020212376968', '85 Innovation Way, Suite 18, Dublin', '+40 721 573 394', true),
	('EMP-00000045', '2026-10-20 09:40:46.719066+00', 'ONB-9F002F98', 'Maria', 'Dumitrescu', 'maria.dumitrescu@atossoftware.com', 'Software Engineering & Application Modernization', 'Backend Engineer', '2026-11-15', 'full-time', 'Romania, Timisoara', 'hybrid', 'EMP-0042', 'active', '2026-10-20 09:40:46.719066+00', '6000127058655', '78 Innovation Way, Suite 30, Timisoara', '+40 750 359 286', true),
	('EMP-00000002', '2026-09-30 14:15:10+00', NULL, 'Jack', 'Doe', 'jack.doe@atossoftware.com', 'IT', 'Admin', '2026-09-16', 'full-time', 'Timisoara, Romania', 'remote', NULL, 'active', '2026-09-30 14:16:35+00', '500234126745', NULL, '+40234887659', true),
	('EMP-00000003', '2026-10-01 21:20:53.916178+00', 'ONB-35132594', 'Cristian', 'Dumitrescu', 'cristian.dumitrescu@atossoftware.com', 'Cybersecurity & Digital Identity', 'Cybersecurity Engineer', '2026-10-15', 'full-time', 'Romania, Timisoara', 'on-site', 'EMP-0042', 'active', '2026-10-02 00:20:53.915644+00', '5021211244331', '244 King''s Road, Suite 16, Timisoara', '+40 739 480 912', true),
	('EMP-74E6BA', '2026-10-14 16:24:55.71469+00', 'TEST-ONB-DA3446', 'Radu-Ștefan', 'Mureșan', 'radustefan.muresan@atossoftware.com', 'Engineering', 'Backend Engineer', '2026-11-01', 'full-time', 'Romania', 'remote', NULL, 'active', '2026-10-14 16:24:55.71469+00', NULL, NULL, NULL, false),
	('EMP-AB989B', '2026-10-14 16:24:55.755216+00', 'TEST-ONB-D2A7B3', 'Radu-Ștefan', 'Mureșan', 'radustefan.muresan2@atossoftware.com', 'Engineering', 'Backend Engineer', '2026-11-01', 'full-time', 'Romania', 'remote', NULL, 'active', '2026-10-14 16:24:55.755216+00', NULL, NULL, NULL, false),
	('EMP-00000000', '2026-10-14 20:33:36.432691+00', NULL, 'System', 'Administrator', 'admin@atossoftware.com', 'IT', 'IT System Administrator', '2026-01-01', 'full_time', 'Timișoara', 'onsite', NULL, 'active', '2026-10-14 20:33:36.432691+00', NULL, NULL, NULL, false),
	('EMP-00000042', '2026-10-14 20:33:36.531652+00', NULL, 'Elena', 'Ionescu', 'hr@atossoftware.com', 'People & Culture', 'HR Lead', '2026-01-01', 'full_time', 'Timișoara', 'onsite', NULL, 'active', '2026-10-14 20:33:36.531652+00', NULL, NULL, NULL, false),
	('EMP-00000010', '2026-10-14 20:33:36.622136+00', NULL, 'Mihai', 'Radu', 'it@atossoftware.com', 'IT Operations', 'IT Provisioning Lead', '2026-01-01', 'full_time', 'Timișoara', 'onsite', NULL, 'active', '2026-10-14 20:33:36.622136+00', NULL, NULL, NULL, false),
	('EMP-00000046', '2026-10-20 10:10:13.47234+00', 'ONB-A467A770', 'Roxana', 'Gheorghe', 'roxana.gheorghe@atossoftware.com', 'Finance, Legal & Corporate Governance', 'Financial Analyst', '2026-11-06', 'full-time', 'Romania, Timisoara', 'hybrid', 'EMP-0042', 'active', '2026-10-20 10:10:13.47234+00', '6000328151868', '240 Main Street, Suite 21, Timisoara', '+40 748 104 753', true);


--
-- Data for Name: software_products; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."software_products" ("product_id", "vendor", "name", "license_type", "total_seats", "requires_approval", "created_at", "updated_at", "description", "access_url", "docs_url") VALUES
	('PROD-GWS-01', 'Google', 'Google Workspace', 'seat-based', 1000, false, '2026-08-20 16:32:30.89529+00', '2026-08-20 16:32:30.89529+00', 'Core enterprise collaboration suite including Gmail, Drive, Calendar, and Meet.', 'https://workspace.google.com/', 'https://support.google.com/a/users/'),
	('PROD-JIR-01', 'Atlassian', 'Jira', 'seat-based', 500, false, '2026-08-20 16:32:30.89529+00', '2026-08-20 16:32:30.89529+00', 'Issue tracking and project management platform for sprint planning and tickets.', 'https://www.atlassian.com/software/jira', 'https://support.atlassian.com/jira-software-cloud/'),
	('PROD-JET-01', 'JetBrains', 'JetBrains All Products Pack', 'subscription', 200, true, '2026-08-20 16:32:30.89529+00', '2026-08-20 16:32:30.89529+00', 'Full-featured enterprise IDE with intelligent code analysis, debugging, and testing.', 'https://account.jetbrains.com/', 'https://www.jetbrains.com/help/'),
	('PROD-AWS-01', 'Amazon', 'AWS IAM Console', 'usage-based', NULL, true, '2026-08-20 16:32:30.89529+00', '2026-08-20 16:32:30.89529+00', 'Cloud infrastructure platform, compute services, and IAM portal.', 'https://aws.amazon.com/console/', 'https://docs.aws.amazon.com/'),
	('PROD-GH-01', 'GitHub', 'GitHub Enterprise', 'seat-based', 1000, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00', 'Source code management, pull request reviews, and CI/CD automation pipelines.', 'https://github.com/login', 'https://docs.github.com/'),
	('PROD-SLK-01', 'Slack', 'Slack Enterprise Grid', 'seat-based', 2000, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00', 'Centralized workspace communication and team messaging channels.', 'https://slack.com/signin', 'https://slack.com/help'),
	('PROD-FIG-01', 'Figma', 'Figma Professional', 'seat-based', 100, true, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00', 'Enterprise software license provisioned and maintained by IT Operations.', 'https://www.figma.com/login', 'https://help.figma.com/'),
	('PROD-NOT-01', 'Notion', 'Notion Enterprise', 'seat-based', 1000, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00', 'Enterprise software license provisioned and maintained by IT Operations.', 'https://www.notion.so/login', 'https://www.notion.so/help'),
	('PROD-DD-01', 'Datadog', 'Datadog APM', 'usage-based', NULL, true, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00', 'Enterprise software license provisioned and maintained by IT Operations.', 'https://workspace.google.com/', 'https://support.google.com/'),
	('PROD-DOC-01', 'Docker', 'Docker Business', 'seat-based', 300, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00', 'Containerized local development runtime and image management.', 'https://hub.docker.com/', 'https://docs.docker.com/'),
	('PROD-ZOO-01', 'Zoom', 'Zoom One Pro', 'seat-based', 1500, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00', 'Enterprise software license provisioned and maintained by IT Operations.', 'https://zoom.us/signin', 'https://support.zoom.us/'),
	('PROD-M365-01', 'Microsoft', 'Microsoft 365 E3', 'seat-based', 1000, false, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00', 'Microsoft cloud productivity suite for documents, spreadsheets, and team collaboration.', 'https://www.office.com/', 'https://support.microsoft.com/office'),
	('PROD-PBI-01', 'Microsoft', 'PowerBI Pro', 'seat-based', 100, true, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00', 'Interactive business intelligence and dashboard reporting tool for data analysis.', 'https://app.powerbi.com/', 'https://learn.microsoft.com/en-us/power-bi/'),
	('PROD-DGR-01', 'JetBrains', 'DataGrip', 'subscription', 50, true, '2026-08-20 16:38:23.696654+00', '2026-08-20 16:38:23.696654+00', 'Cross-platform multi-engine IDE for querying, schema exploration, and database management.', 'https://www.jetbrains.com/datagrip/', 'https://www.jetbrains.com/help/datagrip/');


--
-- Data for Name: license_assignments; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."license_assignments" ("assignment_id", "employee_id", "product_id", "status", "assigned_at", "revoked_at", "updated_at", "created_at") VALUES
	('LIC-DBB1A206', 'EMP-00000003', 'PROD-AWS-01', 'active', '2026-10-02 00:20:53.923114+00', NULL, '2026-10-02 00:20:53.923119+00', '2026-10-02 00:20:53.923118+00'),
	('LIC-8B56EC7C', 'EMP-00000003', 'PROD-DOC-01', 'active', '2026-10-02 00:20:53.923123+00', NULL, '2026-10-02 00:20:53.923125+00', '2026-10-02 00:20:53.923124+00'),
	('LIC-9007F306', 'EMP-00000003', 'PROD-NOT-01', 'active', '2026-10-02 00:20:53.923128+00', NULL, '2026-10-02 00:20:53.92313+00', '2026-10-02 00:20:53.923129+00'),
	('LIC-31633F20', 'EMP-00000003', 'PROD-DD-01', 'active', '2026-10-02 00:20:53.923132+00', NULL, '2026-10-02 00:20:53.923134+00', '2026-10-02 00:20:53.923133+00'),
	('LIC-0B25CA12', 'EMP-00000003', 'PROD-JIR-01', 'active', '2026-10-02 00:20:53.923136+00', NULL, '2026-10-02 00:20:53.923138+00', '2026-10-02 00:20:53.923137+00'),
	('LIC-D4880664', 'EMP-00000003', 'PROD-ZOO-01', 'active', '2026-10-02 00:20:53.92314+00', NULL, '2026-10-02 00:20:53.923142+00', '2026-10-02 00:20:53.923141+00'),
	('LIC-7BE89EB7', 'EMP-00000003', 'PROD-GWS-01', 'active', '2026-10-02 00:20:53.923144+00', NULL, '2026-10-02 00:20:53.923146+00', '2026-10-02 00:20:53.923145+00'),
	('LIC-EB4EAD3A', 'EMP-00000003', 'PROD-SLK-01', 'active', '2026-10-02 00:20:53.923148+00', NULL, '2026-10-02 00:20:53.92315+00', '2026-10-02 00:20:53.923149+00'),
	('LIC-DA608771', 'EMP-74E6BA', 'PROD-GWS-01', 'active', '2026-10-14 16:24:55.71469+00', NULL, '2026-10-14 16:24:55.71469+00', '2026-10-14 16:24:55.71469+00'),
	('LIC-CF1436F2', 'EMP-00000043', 'PROD-SLK-01', 'active', '2026-10-19 21:45:54.8007+00', NULL, '2026-10-19 21:45:54.8007+00', '2026-10-19 21:45:54.8007+00'),
	('LIC-6029D3F3', 'EMP-00000043', 'PROD-JIR-01', 'active', '2026-10-19 21:45:54.8007+00', NULL, '2026-10-19 21:45:54.8007+00', '2026-10-19 21:45:54.8007+00'),
	('LIC-FAB07D83', 'EMP-00000043', 'PROD-GH-01', 'active', '2026-10-19 21:45:54.8007+00', NULL, '2026-10-19 21:45:54.8007+00', '2026-10-19 21:45:54.8007+00'),
	('LIC-18DA062D', 'EMP-00000043', 'PROD-NOT-01', 'active', '2026-10-19 21:45:54.8007+00', NULL, '2026-10-19 21:45:54.8007+00', '2026-10-19 21:45:54.8007+00'),
	('LIC-B836C480', 'EMP-00000043', 'PROD-DOC-01', 'active', '2026-10-19 21:45:54.8007+00', NULL, '2026-10-19 21:45:54.8007+00', '2026-10-19 21:45:54.8007+00'),
	('LIC-09BE09FC', 'EMP-00000043', 'PROD-GWS-01', 'active', '2026-10-19 21:45:54.8007+00', NULL, '2026-10-19 21:45:54.8007+00', '2026-10-19 21:45:54.8007+00'),
	('LIC-140CF523', 'EMP-00000043', 'PROD-JET-01', 'active', '2026-10-19 21:45:54.8007+00', NULL, '2026-10-19 21:45:54.8007+00', '2026-10-19 21:45:54.8007+00'),
	('LIC-A0E34BF2', 'EMP-00000043', 'PROD-ZOO-01', 'active', '2026-10-19 21:45:54.8007+00', NULL, '2026-10-19 21:45:54.8007+00', '2026-10-19 21:45:54.8007+00'),
	('LIC-0CD41CDA', 'EMP-00000044', 'PROD-ZOO-01', 'active', '2026-10-20 09:33:47.266312+00', NULL, '2026-10-20 09:33:47.266312+00', '2026-10-20 09:33:47.266312+00'),
	('LIC-85D0E053', 'EMP-00000044', 'PROD-SLK-01', 'active', '2026-10-20 09:33:47.266312+00', NULL, '2026-10-20 09:33:47.266312+00', '2026-10-20 09:33:47.266312+00'),
	('LIC-607B7295', 'EMP-00000044', 'PROD-GH-01', 'active', '2026-10-20 09:33:47.266312+00', NULL, '2026-10-20 09:33:47.266312+00', '2026-10-20 09:33:47.266312+00'),
	('LIC-CAAEE6D1', 'EMP-00000044', 'PROD-JET-01', 'active', '2026-10-20 09:33:47.266312+00', NULL, '2026-10-20 09:33:47.266312+00', '2026-10-20 09:33:47.266312+00'),
	('LIC-FBE4AF03', 'EMP-00000044', 'PROD-DOC-01', 'active', '2026-10-20 09:33:47.266312+00', NULL, '2026-10-20 09:33:47.266312+00', '2026-10-20 09:33:47.266312+00'),
	('LIC-9AE3DD66', 'EMP-00000044', 'PROD-NOT-01', 'active', '2026-10-20 09:33:47.266312+00', NULL, '2026-10-20 09:33:47.266312+00', '2026-10-20 09:33:47.266312+00'),
	('LIC-85877AEC', 'EMP-00000044', 'PROD-JIR-01', 'active', '2026-10-20 09:33:47.266312+00', NULL, '2026-10-20 09:33:47.266312+00', '2026-10-20 09:33:47.266312+00'),
	('LIC-03416664', 'EMP-00000044', 'PROD-GWS-01', 'active', '2026-10-20 09:33:47.266312+00', NULL, '2026-10-20 09:33:47.266312+00', '2026-10-20 09:33:47.266312+00'),
	('LIC-CEA10FAC', 'EMP-00000045', 'PROD-GH-01', 'active', '2026-10-20 09:40:46.719066+00', NULL, '2026-10-20 09:40:46.719066+00', '2026-10-20 09:40:46.719066+00'),
	('LIC-77304CD3', 'EMP-00000045', 'PROD-GWS-01', 'active', '2026-10-20 09:40:46.719066+00', NULL, '2026-10-20 09:40:46.719066+00', '2026-10-20 09:40:46.719066+00'),
	('LIC-95F01EDD', 'EMP-00000045', 'PROD-ZOO-01', 'active', '2026-10-20 09:40:46.719066+00', NULL, '2026-10-20 09:40:46.719066+00', '2026-10-20 09:40:46.719066+00'),
	('LIC-4BFEEB2A', 'EMP-00000045', 'PROD-SLK-01', 'active', '2026-10-20 09:40:46.719066+00', NULL, '2026-10-20 09:40:46.719066+00', '2026-10-20 09:40:46.719066+00'),
	('LIC-E73DB2F2', 'EMP-00000045', 'PROD-JIR-01', 'active', '2026-10-20 09:40:46.719066+00', NULL, '2026-10-20 09:40:46.719066+00', '2026-10-20 09:40:46.719066+00'),
	('LIC-60973C06', 'EMP-00000045', 'PROD-JET-01', 'active', '2026-10-20 09:40:46.719066+00', NULL, '2026-10-20 09:40:46.719066+00', '2026-10-20 09:40:46.719066+00'),
	('LIC-7DE5D850', 'EMP-00000045', 'PROD-DOC-01', 'active', '2026-10-20 09:40:46.719066+00', NULL, '2026-10-20 09:40:46.719066+00', '2026-10-20 09:40:46.719066+00'),
	('LIC-87D66DDB', 'EMP-00000045', 'PROD-NOT-01', 'active', '2026-10-20 09:40:46.719066+00', NULL, '2026-10-20 09:40:46.719066+00', '2026-10-20 09:40:46.719066+00'),
	('LIC-F5EBE3E2', 'EMP-00000046', 'PROD-JIR-01', 'active', '2026-10-20 10:10:13.47234+00', NULL, '2026-10-20 10:10:13.47234+00', '2026-10-20 10:10:13.47234+00'),
	('LIC-44A28116', 'EMP-00000046', 'PROD-SLK-01', 'active', '2026-10-20 10:10:13.47234+00', NULL, '2026-10-20 10:10:13.47234+00', '2026-10-20 10:10:13.47234+00'),
	('LIC-48064723', 'EMP-00000046', 'PROD-GWS-01', 'active', '2026-10-20 10:10:13.47234+00', NULL, '2026-10-20 10:10:13.47234+00', '2026-10-20 10:10:13.47234+00'),
	('LIC-3A2787C8', 'EMP-00000046', 'PROD-NOT-01', 'active', '2026-10-20 10:10:13.47234+00', NULL, '2026-10-20 10:10:13.47234+00', '2026-10-20 10:10:13.47234+00'),
	('LIC-9DF800DC', 'EMP-00000046', 'PROD-ZOO-01', 'active', '2026-10-20 10:10:13.47234+00', NULL, '2026-10-20 10:10:13.47234+00', '2026-10-20 10:10:13.47234+00');


--
-- Data for Name: onboarding_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."onboarding_requests" ("request_id", "created_at", "employee_id", "first_name", "last_name", "department", "role", "start_date", "employment_type", "location", "work_location", "hr_manager_id", "notes", "status", "manager_id", "shipping_address", "contact_phone", "medical_clearance_status", "national_id", "medical_clearance_date", "extraction_time_seconds", "total_lead_time_seconds", "finalized_at") VALUES
	('ONB-9F002F98', '2026-10-20 09:39:43.072852+00', 'EMP-00000045', 'Maria', 'Dumitrescu', 'Software Engineering & Application Modernization', 'Backend Engineer', '2026-11-15', 'full-time', 'Romania, Timisoara', 'hybrid', 'EMP-00000000', NULL, 'completed', 'EMP-0042', '78 Innovation Way, Suite 30, Timisoara', '+40 750 359 286', true, '6000127058655', '2026-10-12', 0.00, 63.76, '2026-10-20 09:40:46.704336+00'),
	('ONB-A467A770', '2026-10-20 10:09:44.3861+00', 'EMP-00000046', 'Roxana', 'Gheorghe', 'Finance, Legal & Corporate Governance', 'Financial Analyst', '2026-11-06', 'full-time', 'Romania, Timisoara', 'hybrid', 'EMP-00000000', NULL, 'completed', 'EMP-0042', '240 Main Street, Suite 21, Timisoara', '+40 748 104 753', true, '6000328151868', '2026-10-19', 0.00, 29.20, '2026-10-20 10:10:13.457557+00'),
	('ONB-35132594', '2026-10-01 21:20:05.40836+00', 'EMP-00000003', 'Cristian', 'Dumitrescu', 'Cybersecurity & Digital Identity', 'Cybersecurity Engineer', '2026-10-15', 'full-time', 'Romania, Timisoara', 'on-site', 'EMP-0042', NULL, 'completed', 'EMP-0042', '244 King''s Road, Suite 16, Timisoara', '+40 739 480 912', true, '5021211244331', '2026-09-27', 0.00, 48.54, '2026-10-01 21:20:53.903127+00'),
	('ONB-8742A11D', '2026-10-19 21:45:33.590293+00', 'EMP-00000043', 'Radu', 'Ionescu', 'Software Engineering & Application Modernization', 'Backend Engineer', '2026-11-14', 'full-time', 'Romania, Timisoara', 'remote', 'EMP-00000000', NULL, 'completed', 'EMP-0042', '34 Innovation Way, Suite 31, London', '+40 748 878 133', true, '5000321165441', '2026-10-14', 0.00, 21.32, '2026-10-19 21:45:54.789171+00'),
	('ONB-42DD7B05', '2026-10-20 09:32:43.62871+00', 'EMP-00000044', 'Roxana', 'Dumitrescu', 'Software Engineering & Application Modernization', 'Backend Engineer', '2026-11-07', 'full-time', 'Romania, Timisoara', 'on-site', 'EMP-00000000', NULL, 'completed', 'EMP-0042', '85 Innovation Way, Suite 18, Dublin', '+40 721 573 394', true, '6020212376968', '2026-10-14', 0.00, 63.77, '2026-10-20 09:33:47.250323+00');


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
	('1c2632b0-cb5a-41e0-b9a5-040a99396e85', 'jack.doe@atossoftware.com', 'admin', 'EMP-00000002', true, '2026-09-30 14:18:06.645554+00', '2026-09-30 14:20:27.961035+00'),
	('bc8e759e-9bc3-48f4-b422-224ffb55aa87', 'admin@atossoftware.com', 'admin', 'EMP-00000000', true, '2026-10-14 20:33:36.510469+00', '2026-10-14 20:33:36.523758+00'),
	('130ca666-9628-413d-ab1b-a1d5e68ddb78', 'hr@atossoftware.com', 'hr_manager', 'EMP-00000042', true, '2026-10-14 20:33:36.602954+00', '2026-10-14 20:33:36.614309+00'),
	('3b8dccef-b084-49e0-81e3-c2a0962d1061', 'it@atossoftware.com', 'it_manager', 'EMP-00000010', true, '2026-10-14 20:33:36.692363+00', '2026-10-14 20:33:36.704218+00'),
	('aa04e19a-8ade-4f27-ab84-91200fd7770f', 'radu.ionescu@atossoftware.com', 'new_hire', 'EMP-00000043', true, '2026-10-19 21:45:54.877726+00', '2026-10-19 21:45:54.889845+00'),
	('31531e2e-6618-4183-91d7-3f510092fb42', 'roxana.dumitrescu@atossoftware.com', 'new_hire', 'EMP-00000044', true, '2026-10-20 09:33:47.351905+00', '2026-10-20 09:33:47.365039+00'),
	('fe032f51-f06c-48ae-b961-74b4e586e488', 'maria.dumitrescu@atossoftware.com', 'new_hire', 'EMP-00000045', true, '2026-10-20 09:40:46.793892+00', '2026-10-20 09:40:46.806867+00'),
	('030b9a08-e309-4b98-8df0-68cd76b5faa1', 'roxana.gheorghe@atossoftware.com', 'new_hire', 'EMP-00000046', true, '2026-10-20 10:10:13.549503+00', '2026-10-20 10:10:13.561082+00');


--
-- Data for Name: workflow_runs; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO "public"."workflow_runs" ("run_id", "request_id", "suggested_licenses", "suggested_hardware", "policy_citations", "it_notes", "reviewed_by", "created_at", "updated_at", "discretionary_licenses", "execution_time_seconds", "tokens_prompt", "tokens_completion", "tokens_total", "attempt_number", "review_action", "reviewed_at") VALUES
	(66, 'ONB-35132594', '[{"rule_id": "R-CYB-161", "access_level": "auditor", "is_mandatory": true, "requires_approval": true, "software_products": {"name": "AWS IAM Console", "vendor": "Amazon", "product_id": "PROD-AWS-01", "license_type": "usage-based"}}, {"rule_id": "R-GLB-001", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Google Workspace", "vendor": "Google", "product_id": "PROD-GWS-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Slack Enterprise Grid", "vendor": "Slack", "product_id": "PROD-SLK-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-003", "access_level": "user", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Jira", "vendor": "Atlassian", "product_id": "PROD-JIR-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-004", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Zoom One Pro", "vendor": "Zoom", "product_id": "PROD-ZOO-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-005", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Notion Enterprise", "vendor": "Notion", "product_id": "PROD-NOT-01", "license_type": "seat-based"}}, {"rule_id": "R-CYB-ALL-001", "access_level": "viewer", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Datadog APM", "vendor": "Datadog", "product_id": "PROD-DD-01", "license_type": "usage-based"}}, {"rule_id": "R-CYB-ALL-002", "access_level": "standard", "is_mandatory": false, "requires_approval": true, "software_products": {"name": "Docker Business", "vendor": "Docker", "product_id": "PROD-DOC-01", "license_type": "seat-based"}}]', '{"laptop": "High-Performance Developer Workstation", "peripherals": ["Keyboard (standard)", "Mouse (standard)", "Docking Station (dock)", "External Monitor (monitor)"], "shipping_required": false}', '[{"tags": ["POL-HDW-302: On-Site Dispatch", "POL-NET-201: Default Tier-1 SaaS", "POL-NET-202: Restricted Enclave Entitlement", "POL-NET-203: Zero Day-1 Blockers"], "raw_citations": [{"code": "Policy_HDW", "section": "3. Work Location Logistics"}, {"code": "Policy_HDW", "section": "2. Hardware Allocation Protocol"}, {"code": "Policy_NET", "section": "2. Network Segmentation & Enclave Access"}, {"code": "Policy_NET", "section": "1. Purpose & Scope"}], "flagged_exceptions": []}]', NULL, 'EMP-IT-01', '2026-10-01 21:20:45.8376+00', '2026-10-02 00:20:53.937076+00', '[]', 40.44, 905, 2601, 3506, 1, 'approve', '2026-10-01 21:20:53.903127+00'),
	(73, 'ONB-8742A11D', '[{"rule_id": "R-GLB-001", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Google Workspace", "vendor": "Google", "product_id": "PROD-GWS-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Slack Enterprise Grid", "vendor": "Slack", "product_id": "PROD-SLK-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-003", "access_level": "user", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Jira", "vendor": "Atlassian", "product_id": "PROD-JIR-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-004", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Zoom One Pro", "vendor": "Zoom", "product_id": "PROD-ZOO-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-005", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Notion Enterprise", "vendor": "Notion", "product_id": "PROD-NOT-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-001", "access_level": "developer", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "GitHub Enterprise", "vendor": "GitHub", "product_id": "PROD-GH-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Docker Business", "vendor": "Docker", "product_id": "PROD-DOC-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-003", "access_level": "standard", "is_mandatory": true, "requires_approval": true, "software_products": {"name": "JetBrains All Products Pack", "vendor": "JetBrains", "product_id": "PROD-JET-01", "license_type": "subscription"}}]', '{"laptop": "Developer Workstation", "peripherals": ["External Monitor", "Dock (USB-C/Thunderbolt)", "Keyboard & Mouse"], "shipping_required": false}', '[{"tags": ["POL-HDW-501", "POL-HDW-502", "POL-HDW-504"], "raw_citations": [{"code": "Policy_HDW", "section": "5. Work Location Logistics & Delivery Protocols"}, {"code": "Policy_OFF", "section": "4. Hardware Recovery & Physical Asset Sanitization"}, {"code": "Policy_NET", "section": "1. Purpose & Scope"}, {"code": "Policy_NET", "section": "2. Network Segmentation & Enclave Entitlements"}], "flagged_exceptions": []}]', '', 'EMP-00000000', '2026-10-19 21:45:40.798995+00', '2026-10-20 00:45:54.903245+00', '[]', 7.22, 1428, 785, 2213, 1, 'approve', '2026-10-19 21:45:54.789171+00'),
	(75, 'ONB-9F002F98', '[{"rule_id": "R-GLB-001", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Google Workspace", "vendor": "Google", "product_id": "PROD-GWS-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Slack Enterprise Grid", "vendor": "Slack", "product_id": "PROD-SLK-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-003", "access_level": "user", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Jira", "vendor": "Atlassian", "product_id": "PROD-JIR-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-004", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Zoom One Pro", "vendor": "Zoom", "product_id": "PROD-ZOO-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-005", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Notion Enterprise", "vendor": "Notion", "product_id": "PROD-NOT-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-001", "access_level": "developer", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "GitHub Enterprise", "vendor": "GitHub", "product_id": "PROD-GH-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Docker Business", "vendor": "Docker", "product_id": "PROD-DOC-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-003", "access_level": "standard", "is_mandatory": true, "requires_approval": true, "software_products": {"name": "JetBrains All Products Pack", "vendor": "JetBrains", "product_id": "PROD-JET-01", "license_type": "subscription"}}]', '{"laptop": "High-Performance Developer Workstation", "peripherals": ["Docking Station", "External Monitor", "USB Keyboard", "Optical Mouse"], "shipping_required": false}', '[{"tags": ["POL-HDW-503: On-site and hybrid work location staged via campus IT Helpdesk repository for physical desk delivery day one.", "POL-HDW-502: Dispatch lead time requirement (5 business days prior to start date) is satisfied."], "raw_citations": [{"code": "Policy_OFF", "section": "4. Hardware Recovery & Physical Asset Sanitization"}, {"code": "Policy_HDW", "section": "5. Work Location Logistics & Delivery Protocols"}, {"code": "Policy_NET", "section": "2. Network Segmentation & Enclave Entitlements"}, {"code": "Policy_NET", "section": "1. Purpose & Scope"}], "flagged_exceptions": []}]', '', 'EMP-00000000', '2026-10-20 09:40:26.661135+00', '2026-10-20 12:40:46.82164+00', '[]', 43.60, 1428, 3729, 5157, 1, 'approve', '2026-10-20 09:40:46.704336+00'),
	(74, 'ONB-42DD7B05', '[{"rule_id": "R-GLB-001", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Google Workspace", "vendor": "Google", "product_id": "PROD-GWS-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Slack Enterprise Grid", "vendor": "Slack", "product_id": "PROD-SLK-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-003", "access_level": "user", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Jira", "vendor": "Atlassian", "product_id": "PROD-JIR-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-004", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Zoom One Pro", "vendor": "Zoom", "product_id": "PROD-ZOO-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-005", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Notion Enterprise", "vendor": "Notion", "product_id": "PROD-NOT-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-001", "access_level": "developer", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "GitHub Enterprise", "vendor": "GitHub", "product_id": "PROD-GH-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Docker Business", "vendor": "Docker", "product_id": "PROD-DOC-01", "license_type": "seat-based"}}, {"rule_id": "R-SE-ALL-003", "access_level": "standard", "is_mandatory": true, "requires_approval": true, "software_products": {"name": "JetBrains All Products Pack", "vendor": "JetBrains", "product_id": "PROD-JET-01", "license_type": "subscription"}}]', '{"laptop": "Developer Workstation", "peripherals": ["Keyboard", "Mouse"], "shipping_required": false}', '[{"tags": ["POL-HDW-503", "POL-NET-204"], "raw_citations": [{"code": "Policy_OFF", "section": "4. Hardware Recovery & Physical Asset Sanitization"}, {"code": "Policy_HDW", "section": "5. Work Location Logistics & Delivery Protocols"}, {"code": "Policy_NET", "section": "2. Network Segmentation & Enclave Entitlements"}, {"code": "Policy_NET", "section": "1. Purpose & Scope"}], "flagged_exceptions": []}]', '', 'EMP-00000000', '2026-10-20 09:33:39.938373+00', '2026-10-20 12:33:47.383203+00', '[]', 56.32, 1430, 3845, 5275, 1, 'approve', '2026-10-20 09:33:47.250323+00'),
	(76, 'ONB-A467A770', '[{"rule_id": "R-GLB-001", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Google Workspace", "vendor": "Google", "product_id": "PROD-GWS-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-002", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Slack Enterprise Grid", "vendor": "Slack", "product_id": "PROD-SLK-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-003", "access_level": "user", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Jira", "vendor": "Atlassian", "product_id": "PROD-JIR-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-004", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Zoom One Pro", "vendor": "Zoom", "product_id": "PROD-ZOO-01", "license_type": "seat-based"}}, {"rule_id": "R-GLB-005", "access_level": "standard", "is_mandatory": true, "requires_approval": false, "software_products": {"name": "Notion Enterprise", "vendor": "Notion", "product_id": "PROD-NOT-01", "license_type": "seat-based"}}]', '{"laptop": "Standard Enterprise Laptop", "peripherals": ["USB Keyboard", "USB Mouse", "Docking Station"], "shipping_required": false}', '[{"tags": ["POL-HDW-501", "POL-HDW-503", "POL-NET-202", "POL-NET-204"], "raw_citations": [{"code": "Policy_OFF", "section": "4. Hardware Recovery & Physical Asset Sanitization"}, {"code": "Policy_HDW", "section": "5. Work Location Logistics & Delivery Protocols"}, {"code": "Policy_NET", "section": "2. Network Segmentation & Enclave Entitlements"}, {"code": "Policy_NET", "section": "4. Cross-Enclave Routing & Exception Governance"}], "flagged_exceptions": []}]', '', 'EMP-00000000', '2026-10-20 10:10:06.182818+00', '2026-10-20 13:10:13.577396+00', '[]', 21.81, 1578, 1169, 2747, 1, 'approve', '2026-10-20 10:10:13.457557+00');


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 28, true);


--
-- Name: workflow_runs_run_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."workflow_runs_run_id_seq"', 76, true);


--
-- PostgreSQL database dump complete
--

-- \unrestrict SvUmNRh9TvAcon3R4IguJzCD2amtNJFyHeYYmKAHlSYCsyMbo0WP6cKE57M3o5G

RESET ALL;
