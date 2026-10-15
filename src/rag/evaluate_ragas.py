import os
import sys
import types
import warnings
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")

from retriever import PolicyRetriever

try:
    from langchain_ollama import ChatOllama
except ImportError:
    from langchain_community.chat_models import ChatOllama

# ---------------------------------------------------------------------------
# 1. Benchmark Test Cases with Explicit Clause Targets
# ---------------------------------------------------------------------------
BENCHMARK_TEST_CASES = [
    {
        "id": "TC-01-HDW-REMOTE",
        "question": "What laptop hardware profile and logistics are required for a remote Software Engineer?",
        "ground_truth": (
            "Software engineers receive the Technical & Engineering Workstation Laptop tier "
            "(minimum 32 GB RAM, 1 TB encrypted SSD) per [POL-HDW-203]. Remote personnel require an automated "
            "courier dispatch ticket with trackable delivery dispatched at least 5 business days before the start "
            "date per [POL-HDW-501] and [POL-HDW-502]."
        ),
        "expected_clauses": ["POL-HDW-203", "POL-HDW-501", "POL-HDW-502"],
    },
    {
        "id": "TC-02-SAAS-EXHAUSTION",
        "question": "How should the orchestration engine handle an onboarding request when a required software license has zero available seats?",
        "ground_truth": (
            "Under [POL-SAAS-203] and [POL-EXC-204], if an assigned software product has zero available seats, "
            "the system must flag a license deficit exception, suspend license execution, halt automated assignment, "
            "and alert the IT administrator without failing the entire workflow."
        ),
        "expected_clauses": ["POL-SAAS-203", "POL-EXC-204"],
    },
    {
        "id": "TC-03-IAM-AUTH-TAP",
        "question": "What authentication protocol replaces plain-text passwords for new hires, and how long is it valid?",
        "ground_truth": (
            "Per [POL-IAM-202], the system issues a single-use Temporary Access Pass (TAP) token expiring "
            "within 24 hours of the official start date. Initial login requires immediate mandatory MFA enrollment "
            "per [POL-IAM-204]."
        ),
        "expected_clauses": ["POL-IAM-202", "POL-IAM-204"],
    },
    {
        "id": "TC-04-NET-VPN-TAP",
        "question": "Can an employee establish a corporate network tunnel (VPN) using their initial Temporary Access Pass (TAP)?",
        "ground_truth": (
            "No. Under [POL-NET-303], network tunnel access cannot be established via a Temporary Access Pass (TAP). "
            "Full MFA enrollment and cryptographic client certificates on managed devices are required."
        ),
        "expected_clauses": ["POL-NET-303", "POL-NET-302"],
    },
    {
        "id": "TC-05-OFF-ASSET-RETURN",
        "question": "What is the mandatory protocol for digital work assets and physical hardware when an employee is offboarded?",
        "ground_truth": (
            "Under [POL-OFF-301], ownership of repositories, storage drives, and workflow tickets must be transferred "
            "to the designated replacement manager. Physical hardware must have prepaid return waybills dispatched per "
            "[POL-OFF-401], devices locked remotely per [POL-OFF-402], and be returned within 5 business days per [POL-OFF-403]."
        ),
        "expected_clauses": ["POL-OFF-301", "POL-OFF-401", "POL-OFF-402", "POL-OFF-403"],
    },
    {
        "id": "TC-06-EXC-PRIVILEGED",
        "question": "What are the approval and justification requirements when a request includes privileged or administrative access?",
        "ground_truth": (
            "Under [POL-EXC-301] and [POL-EXC-302], privileged access requires a non-empty business justification string. "
            "Under [POL-EXC-304] and [POL-EXC-401], it routes to the Human-in-the-Loop gateway and requires two-party sign-off "
            "from the department manager and an Information Security Administrator."
        ),
        "expected_clauses": ["POL-EXC-301", "POL-EXC-302", "POL-EXC-304", "POL-EXC-401"],
    },
]


def run_benchmark(ollama_model: str = "qwen3.5:9b"):
    print("--> Initializing Policy Retriever...", flush=True)
    retriever = PolicyRetriever()

    print(f"--> Connecting to Ollama Model: '{ollama_model}'...", flush=True)
    llm = ChatOllama(model=ollama_model, temperature=0.0, num_ctx=4096)

    records = []

    print(f"\n--> Running Evaluation over {len(BENCHMARK_TEST_CASES)} Policy Cases...\n", flush=True)

    for case in BENCHMARK_TEST_CASES:
        q = case["question"]
        expected = set(case["expected_clauses"])

        # 1. Retrieve citations
        citations = retriever.retrieve(query=q, top_k_candidates=10, final_top_k=3)

        # Extract all retrieved clause codes from metadata
        retrieved_clauses = set()
        for c in citations:
            retrieved_clauses.update(c.get("clause_tags", []))

        # 2. Deterministic Retrieval Metrics
        matched_clauses = expected.intersection(retrieved_clauses)
        clause_recall = len(matched_clauses) / len(expected) if expected else 1.0
        hit = 1.0 if len(matched_clauses) > 0 else 0.0

        # Check MRR (Rank of the first expected clause in top-k parent sections)
        mrr = 0.0
        for rank, c in enumerate(citations, start=1):
            if any(clause in expected for clause in c.get("clause_tags", [])):
                mrr = 1.0 / rank
                break

        # 3. Generate Local Compliance Answer
        context_block = "\n\n".join([f"[{c['policy_code']}]: {c['content']}" for c in citations])
        prompt = (
            f"You are an enterprise compliance auditor. Answer using ONLY the policy text provided below.\n"
            f"Cite policy clause IDs (e.g. [POL-HDW-203]) explicitly.\n\n"
            f"Policy Context:\n{context_block}\n\n"
            f"Question: {q}\n\nAnswer:"
        )

        res = llm.invoke(prompt)
        answer = res.content if hasattr(res, "content") else str(res)

        # Check if the LLM actually cited the required clauses in its answer
        cited_in_answer = [clause for clause in expected if clause.lower() in answer.lower()]
        answer_grounding = len(cited_in_answer) / len(expected) if expected else 1.0

        print(f"[{case['id']}]")
        print(f" • Expected Clauses : {list(expected)}")
        print(f" • Retrieved Clauses: {list(retrieved_clauses)}")
        print(f" • Clause Recall    : {clause_recall * 100:.1f}%")
        print(f" • MRR              : {mrr:.2f}")
        print(f" • Cited in Answer  : {cited_in_answer} ({answer_grounding * 100:.1f}%)\n")

        records.append({
            "test_id": case["id"],
            "question": q,
            "clause_hit": hit,
            "clause_recall": clause_recall,
            "mrr": mrr,
            "answer_grounding": answer_grounding,
            "answer": answer,
        })

    df = pd.DataFrame(records)
    output_path = Path("tests/reports")
    output_path.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path / "policy_retrieval_benchmark.csv", index=False)

    print("=" * 60)
    print("        POLICY RETRIEVAL & GROUNDING SCORECARD")
    print("=" * 60)
    print(f" • Hit Rate (Any Clause Found) : {df['clause_hit'].mean() * 100:.1f}%")
    print(f" • Average Clause Recall       : {df['clause_recall'].mean() * 100:.1f}%")
    print(f" • Mean Reciprocal Rank (MRR)  : {df['mrr'].mean():.4f}")
    print(f" • Answer Citation Grounding   : {df['answer_grounding'].mean() * 100:.1f}%")
    print(f"\nDetailed report saved to: tests/reports/policy_retrieval_benchmark.csv")
    print("=" * 60)


if __name__ == "__main__":
    MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")
    run_benchmark(ollama_model=MODEL)