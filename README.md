# Project Setup

## Requirements

1. **uv Python Package Manager:** [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1)
2. **FastAPI:** [Requirements & Setup](https://fastapi.tiangolo.com/#requirements)
3. **Supabase:** [JavaScript Client Installation](https://supabase.com/docs/reference/javascript/installing)

---

## Installation & Setup

After installing the prerequisites, run the following commands:

```bash
uv add supabase python-dotenv
npm install supabase --save-dev
npx supabase init # (daca nu merge adaugati --force)
npx supabase start
uv run fastapi dev
```

---

## Environment Variables

Create a `.env` file in the project root and add:

```env
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_KEY=<Publishable Authentication Key>     # npx supabase status -> Authentication Keys
SUPABASE_SECRET_KEY=<Secret Authentication Key>
API_URL="..."
OLLAMA_MODEL="granite4.2:3b"
OLLAMA_VISION_MODEL="glm-ocr:latest"
OLLAMA_JUDGE_MODEL="qwen2.5:3b"
```

---

## Service Endpoints & Interfaces

* **Supabase Web Interface:** [http://127.0.0.1:54323/project/default](http://127.0.0.1:54323/project/default)
* **FastAPI SwaggerUI (pentru testare endpoints):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Streamlit Frontend:** [http://localhost:8501/hr](http://localhost:8501/hr)

---

## Jira Cloud Ticketing Integration

The onboarding workflow synchronizes with a Jira Cloud project (default key `IT`).
Each onboarding request creates **one parent ticket**; regenerations update that same
ticket instead of creating duplicates. IT can approve/reject either from the portal
or directly in Jira, and hardware shipments spawn a linked sub-task.

### 1. Jira configuration

1. Create a project with key `IT` (issues: `Task`, `Subtask`; both names are configurable
   via `JIRA_ISSUE_TYPE` / `JIRA_SUBTASK_ISSUE_TYPE`).
2. Add workflow statuses/transitions: `Pending Approval`, `Approved`, `Needs Revision`,
   `In Progress`, `Done` (names are matched case-insensitively).
3. Create a dedicated service account and an **API token**
   (Atlassian account settings → Security → API tokens).
4. Fill in `.env`:

```env
JIRA_BASE_URL="https://your-site.atlassian.net"
JIRA_EMAIL="jira-service-account@your-company.com"
JIRA_API_TOKEN="<Atlassian API token>"
JIRA_PROJECT_KEY="IT"
JIRA_ISSUE_TYPE="Task"
JIRA_SUBTASK_ISSUE_TYPE="Subtask"
JIRA_WEBHOOK_SECRET="<shared secret>"
JIRA_LOGISTICS_ASSIGNEE_ACCOUNT_ID="<optional accountId>"
JIRA_SERVICE_ACCOUNT_ID="<optional accountId>"
```

Jira sync is automatically disabled when the first four variables are missing, so
local development works without a Jira instance. Check the credentials with
`GET /health/jira` (read-only). Apply the schema migration after pulling:

```bash
npx supabase db reset   # or: npx supabase migration up
```

### 2. Jira webhook

In Jira: **Settings → System → Webhooks → Create a webhook**

* **URL:** `https://<your-host>/webhooks/jira` (expose the local API with your tunnel)
* **Events:** Issue → Updated (enable comments too if desired)
* **Secret:** set the same value as `JIRA_WEBHOOK_SECRET`

Jira Cloud signs deliveries with HMAC-SHA256 in the `X-Hub-Signature` header
(`sha256=<hex>`); the endpoint verifies that signature. If you trigger the endpoint
from Jira Automation or a proxy instead, you can send the secret directly in the
`X-Jira-Webhook-Secret` header. Events written by the integration account (identified
by `JIRA_EMAIL` / `JIRA_SERVICE_ACCOUNT_ID`) are ignored to prevent feedback loops
when the portal itself transitions a ticket.

### 3. API notes

* Issue create/update/comments use REST **v2** (`/rest/api/2/...`) so the description
  and comment bodies accept plain-text/Jira Wiki Markup. REST v3 requires ADF JSON.
* Status transitions use REST **v3** and require a transition **id**. The client first
  fetches `GET /rest/api/3/issue/{key}/transitions` and matches the requested status
  name case-insensitively before posting `{"transition": {"id": "..."}}`.
* `POST /webhooks/jira` maps `Approved → action=approve` and `Needs Revision →
  action=regenerate`, then resumes the paused LangGraph approval gate.

---

## Mock Document Generation

To create mock documents, run the following command from the project root:

```bash
python scripts/generate_mock_docs.py --count x
```

This will create a `mock_documents` directory where all mock candidate docs will be stored.

---

## Maintenance

After pulling changes from the repository, remember to sync your dependencies:

```bash
uv sync
```

and update the database structure by applying the latest db migration and seeding:

```bash
npx supabase db reset
```
