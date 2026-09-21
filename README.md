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
