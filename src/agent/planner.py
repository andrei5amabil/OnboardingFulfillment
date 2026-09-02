import json
from typing import Dict, Any, List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.schemas.agent_payload import OnboardingPlan, PolicyCitation
from src.rag.retriever import PolicyRetriever

# --- OBSERVABILITY SETUP ---
from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry import trace as trace_api
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

tracer_provider = trace_sdk.TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter("http://127.0.0.1:6006/v1/traces")))
trace_api.set_tracer_provider(tracer_provider)
LangChainInstrumentor().instrument()
# ---------------------------

class OnboardingAgent:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.llm = ChatOllama(
            base_url=base_url,
            model=model,
            temperature=0.0
        )
        self.structured_llm = self.llm.with_structured_output(OnboardingPlan)
        self.retriever = PolicyRetriever()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an enterprise IT Security & Onboarding Orchestrator.\n"
                "Your job is to strictly enforce access policies and protect enterprise assets.\n\n"
                "CRITICAL SECURITY RULES:\n"
                "1. PRIVILEGED ACCESS: Any request for root, production database, or admin consoles (e.g., 'AWS Production Root') "
                "is a Privilege Escalation. It MUST be marked with requires_approval=True, risk_level='high', and hitl_required=True.\n"
                "2. STOCK DEFICITS: If an item has available_seats <= 0 (e.g., DataGrip with 0 seats), you MUST NOT auto-approve it. "
                "Flag requires_approval=True, action_type='flag_exception', and hitl_required=True.\n"
                "3. OUT-OF-BAND REQUESTS: Any software requested in notes that is NOT in Baseline Entitlements requires HITL approval.\n"
                "4. CITATIONS: You MUST populate the 'citations' array with the exact rule_id, document_name, and quote from the retrieved policies."
            )),
            ("user", (
                "### Incoming HR Payload:\n{hr_payload}\n\n"
                "### Baseline Entitlement Rules (Allowed by Default):\n{baseline_rules}\n\n"
                "### Current Software & Asset Inventory:\n{inventory_status}\n\n"
                "### Mandatory Applicable Policies:\n{retrieved_policies}\n\n"
                "Evaluate the request and output the structured OnboardingPlan JSON adhering strictly to the above rules."
            ))
        ])

    def evaluate_request(
        self,
        hr_payload: Dict[str, Any],
        baseline_rules: list,
        inventory_status: list
    ) -> OnboardingPlan:
        notes = hr_payload.get("notes", "")
        role = hr_payload.get("role", "")
        work_location = hr_payload.get("work_location", "")

        retrieved_docs: List[PolicyCitation] = []
        retrieved_docs.extend(self.retriever.retrieve_citations(f"{role} baseline hardware and access", k=2))
        retrieved_docs.extend(self.retriever.retrieve_citations("Privilege escalation admin root database access justification", k=2))
        retrieved_docs.extend(self.retriever.retrieve_citations("License stock deficit zero available seats", k=2))

        unique_citations = {c.rule_id: c for c in retrieved_docs}.values()

        chain = self.prompt | self.structured_llm

        plan: OnboardingPlan = chain.invoke({
            "hr_payload": json.dumps(hr_payload, indent=2),
            "baseline_rules": json.dumps(baseline_rules, indent=2),
            "inventory_status": json.dumps(inventory_status, indent=2),
            "retrieved_policies": json.dumps([c.model_dump() for c in unique_citations], indent=2)
        })
        return plan

if __name__ == "__main__":
    agent = OnboardingAgent()
    
    # Run the same test payload as before
    sample_payload = {
        "request_id": "ONB-47E6F6D5",
        "employee_id": "EMP-0006",
        "first_name": "Son",
        "last_name": "Sonion",
        "department": "Software Engineering",
        "role": "Junior Frontend Developer",
        "work_location": "remote",
        "notes": "Employee requested access to AWS Production Root and DataGrip."
    }
    sample_rules = [
        {"role": "Junior Frontend Developer", "product_name": "GitHub Enterprise", "requires_approval": False},
        {"role": "Junior Frontend Developer", "product_name": "VS Code", "requires_approval": False}
    ]
    sample_inventory = [
        {"product_name": "GitHub Enterprise", "available_seats": 12},
        {"product_name": "DataGrip", "available_seats": 0},
        {"product_name": "AWS Production Root", "available_seats": 1}
    ]

    print("[*] Running agent reasoning with Observability Tracing...")
    decision = agent.evaluate_request(sample_payload, sample_rules, sample_inventory)
    print("\n[+] Structured Decision Plan:")
    print(decision.model_dump_json(indent=2))
