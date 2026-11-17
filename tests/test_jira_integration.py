import hashlib
import hmac
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.integrations.jira.client import JiraClient, JiraConfig
from src.integrations.jira.format import (
    build_logistics_subtask_description,
    build_onboarding_ticket_description,
)
from src.integrations.jira.workflow import map_status_to_action


class FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self.text = "" if payload is None else json.dumps(payload)
        self.content = self.text.encode("utf-8")
        self._payload = payload or {}

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append({"method": method, "url": url, **kwargs})
        return self.responses.pop(0)


def make_client(responses):
    config = JiraConfig(
        base_url="https://example.atlassian.net",
        email="bot@example.com",
        api_token="token",
        project_key="IT",
    )
    return JiraClient(config=config, session=FakeSession(responses))


class JiraClientTests(unittest.TestCase):
    def test_transition_resolves_name_to_id(self):
        client = make_client(
            [
                FakeResponse(payload={
                    "transitions": [
                        {"id": "31", "name": "Approved"},
                        {"id": "41", "name": "Needs Revision"},
                    ]
                }),
                FakeResponse(status_code=204),
            ]
        )

        moved = client.transition_issue("IT-402", "approved")

        self.assertTrue(moved)
        get_call, post_call = client.session.calls
        self.assertEqual(get_call["method"], "GET")
        self.assertEqual(
            get_call["url"],
            "https://example.atlassian.net/rest/api/3/issue/IT-402/transitions",
        )
        self.assertEqual(post_call["method"], "POST")
        self.assertEqual(post_call["json"], {"transition": {"id": "31"}})

    def test_transition_missing_name_returns_false(self):
        client = make_client([FakeResponse(payload={"transitions": []})])

        self.assertFalse(client.transition_issue("IT-402", "Approved"))
        self.assertEqual(len(client.session.calls), 1)

    def test_create_issue_uses_v2_plain_text(self):
        client = make_client([FakeResponse(payload={"id": "1", "key": "IT-402"})])

        issue = client.create_issue(
            summary="Onboarding - Ionut Popescu (Data Analyst)",
            description="h2. Onboarding Plan",
            labels=["onboarding", "Data Analytics"],
        )

        self.assertEqual(issue["key"], "IT-402")
        call = client.session.calls[0]
        self.assertEqual(call["url"], "https://example.atlassian.net/rest/api/2/issue")
        self.assertEqual(call["json"]["fields"]["description"], "h2. Onboarding Plan")
        self.assertEqual(call["json"]["fields"]["labels"], ["onboarding", "data-analytics"])


class JiraFormatTests(unittest.TestCase):
    def test_plan_description_contains_all_sections(self):
        state = {
            "request_id": "ONB-123",
            "employee_id": "EMP-1",
            "attempt_count": 2,
            "status": "pending_approval",
            "candidate_data": {
                "first_name": "Ionut",
                "last_name": "Popescu",
                "role": "Data Analyst",
                "department": "Data",
                "start_date": "2026-12-01",
                "work_location": "remote",
            },
            "suggested_licenses": [
                {
                    "access_level": "standard",
                    "is_mandatory": True,
                    "requires_approval": False,
                    "software_products": {
                        "name": "Jira",
                        "vendor": "Atlassian",
                        "license_type": "seat-based",
                    },
                }
            ],
            "discretionary_licenses": [
                {"product_id": "PROD-FIG-01", "name": "Figma", "justification": "Design work"}
            ],
            "suggested_hardware": {
                "laptop": "Dell XPS 15",
                "peripherals": ["Dock", "Monitor"],
                "shipping_required": True,
            },
            "policy_tags": ["POL-HDW-501"],
            "citations": [{"policy_code": "Policy_HDW", "section_title": "5. Logistics"}],
            "flagged_exceptions": ["LOGISTICS WARNING: missing address"],
        }

        description = build_onboarding_ticket_description(state)

        self.assertIn("Onboarding Plan - Ionut Popescu", description)
        self.assertIn("||Product||Vendor||", description)
        self.assertIn("Dell XPS 15", description)
        self.assertIn("LOGISTICS WARNING", description)
        self.assertIn("Needs Revision", description)

    def test_logistics_subtask_includes_shipping_address(self):
        state = {
            "request_id": "ONB-123",
            "employee_id": "EMP-1",
            "candidate_data": {
                "first_name": "Ionut",
                "last_name": "Popescu",
                "shipping_address": "1 Main Street",
                "contact_phone": "+40700000000",
            },
            "suggested_hardware": {"laptop": "Dell XPS 15", "peripherals": ["Dock"]},
        }

        description = build_logistics_subtask_description(state)

        self.assertIn("1 Main Street", description)
        self.assertIn("Dell XPS 15", description)
        self.assertIn("Hardware shipment", description)

    def test_status_mapping(self):
        self.assertEqual(map_status_to_action("Approved"), "approve")
        self.assertEqual(map_status_to_action("needs revision"), "regenerate")
        self.assertIsNone(map_status_to_action("In Progress"))
        self.assertIsNone(map_status_to_action("Done"))


class _FakeQuery:
    def __init__(self, data):
        self._data = data

    def select(self, *args, **kwargs):
        return self

    def eq(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    def execute(self):
        return SimpleNamespace(data=self._data)


class _FakeSupabase:
    def __init__(self, rows):
        self.rows = rows

    def table(self, name):
        return _FakeQuery(self.rows)


class JiraWebhookTests(unittest.TestCase):
    def setUp(self):
        import main

        self.main = main
        self.client = TestClient(main.app)
        self._original_secret = main.jira_client.config.webhook_secret
        main.jira_client.config.webhook_secret = "test-secret"

    def tearDown(self):
        self.main.jira_client.config.webhook_secret = self._original_secret

    def _payload(self, status, author_email="admin@company.com", event_id="evt-1"):
        return {
            "webhookEvent": "jira:issue_updated",
            "timestamp": 1700000000,
            "user": {"emailAddress": author_email, "displayName": "IT Admin"},
            "issue": {"key": "IT-402", "fields": {"status": {"name": status}}},
            "changelog": {
                "id": event_id,
                "items": [
                    {
                        "field": "status",
                        "fromString": "Pending Approval",
                        "toString": status,
                    }
                ],
            },
            "comment": {
                "body": {
                    "type": "doc",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "LGTM"}],
                        }
                    ],
                }
            },
        }

    def test_rejects_wrong_secret(self):
        response = self.client.post(
            "/webhooks/jira",
            json=self._payload("Approved"),
            headers={"X-Jira-Webhook-Secret": "wrong"},
        )
        self.assertEqual(response.status_code, 401)

    def test_accepts_hmac_signature(self):
        body = json.dumps(self._payload("In Progress")).encode("utf-8")
        signature = hmac.new(b"test-secret", body, hashlib.sha256).hexdigest()

        response = self.client.post(
            "/webhooks/jira",
            content=body,
            headers={
                "Content-Type": "application/json",
                "X-Hub-Signature": f"sha256={signature}",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ignored")

    def test_ignores_non_decision_status(self):
        response = self.client.post(
            "/webhooks/jira",
            json=self._payload("In Progress"),
            headers={"X-Jira-Webhook-Secret": "test-secret"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ignored")

    def test_ignores_service_account_events(self):
        import main

        response = self.client.post(
            "/webhooks/jira",
            json=self._payload("Approved", author_email=main.jira_client.config.email),
            headers={"X-Jira-Webhook-Secret": "test-secret"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ignored")

    def test_approved_transition_queues_resume(self):
        import main

        request_row = {"request_id": "ONB-123", "status": "pending_approval"}
        with (
            patch.object(main, "supabase", _FakeSupabase([request_row])),
            patch.object(
                main.onboarding_flow,
                "get_state",
                return_value=SimpleNamespace(tasks=[object()]),
            ),
            patch.object(main, "_resume_from_jira") as resume,
        ):
            response = self.client.post(
                "/webhooks/jira",
                json=self._payload("Approved", event_id="evt-approved"),
                headers={"X-Jira-Webhook-Secret": "test-secret"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "accepted")
        self.assertEqual(response.json()["action"], "approve")
        resume.assert_called_once_with(
            "ONB-123",
            "approve",
            "LGTM",
            "JIRA:admin@company.com",
        )


if __name__ == "__main__":
    unittest.main()
