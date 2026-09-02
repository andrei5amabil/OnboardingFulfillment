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
                "Your job is to strictly enforce access policies, evaluate entitlements, and output structured fulfillment plans.\n\n"
                "CRITICAL SECURITY RULES:\n"
                "1. PRIVILEGED ACCESS: Any request for root, infrastructure admin, or privileged consoles "
                "(e.g., elevated admin on 'AWS IAM Console', production database credentials) is a Privilege Escalation. "
                "It MUST be set to requires_approval=True, action_type='flag_exception', and trigger hitl_required=True.\n"
                "2. STOCK DEFICITS: If an item has available_seats <= 0, you MUST NOT auto-approve it. "
                "Flag requires_approval=True, action_type='flag_exception', and hitl_required=True.\n"
                "3. CATALOG MAPPING: In ProposedAction, set 'target_id' to the specific product_id (e.g., 'PROD-AWS-01', 'PROD-GWS-01') "
                "or the specific role-based asset identifier.\n"
                "4. ACTION TYPES: Use 'assign_license' for standard software provisioning. Use 'flag_exception' for denied, out-of-band, or approval-blocked requests.\n"
                "5. OUT-OF-BAND REQUESTS: Any software requested in notes that is not granted by Baseline Entitlements requires approval.\n"
                "6. CITATIONS: Populate the 'citations' array with the exact rule_id, document_name, and quote from the retrieved policies."
            )),
            ("user", (
                "### Incoming HR Payload:\n{hr_payload}\n\n"
                "### Baseline Entitlement Rules (Allowed by Default):\n{baseline_rules}\n\n"
                "### Current Software & Asset Inventory:\n{inventory_status}\n\n"
                "### Mandatory Applicable Policies:\n{retrieved_policies}\n\n"
                "Evaluate the request and generate the structured OnboardingPlan JSON adhering strictly to the above rules."
            ))
        ])

    def evaluate_request(
        self,
        hr_payload: Dict[str, Any],
        baseline_rules: list,
        inventory_status: list
    ) -> OnboardingPlan:
        # Guard against None values coming from the database
        notes = hr_payload.get("notes") or ""
        role = hr_payload.get("role") or ""

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
    
    # Realistic test payload matchingDB_Request schema
    sample_payload = {
        "request_id": "ONB-47E6F6D5",
        "employee_id": "EMP-0006",
        "first_name": "Son",
        "last_name": "Sonion",
        "department": "Software Engineering & Application Modernization",
        "role": "Junior Frontend Developer",
        "start_date": "2026-08-18",
        "employment_type": "full-time",
        "location": "Romania, Timisoara",
        "work_location": "remote",
        "hr_manager_id": "EMP-0042",
        "notes": "Employee requested elevated admin access to AWS IAM Console and a DataGrip license."
    }
    
    # Exact rules matching product_assignment_rules table
    sample_rules = [
        {
            "rule_id": "R-SE-GWS-01",
            "department": "Software Engineering & Application Modernization",
            "role": "Junior Frontend Developer",
            "product_id": "PROD-GWS-01",
            "product_name": "Google Workspace",
            "access_level": "standard",
            "is_mandatory": True,
            "requires_approval": False
        },
        {
            "rule_id": "R-SE-JIR-01",
            "department": "Software Engineering & Application Modernization",
            "role": "Junior Frontend Developer",
            "product_id": "PROD-JIR-01",
            "product_name": "Jira",
            "access_level": "user",
            "is_mandatory": True,
            "requires_approval": False
        }
    ]
    
    # Exact inventory matching software_products table
    sample_inventory = [
        {"product_id": "PROD-GWS-01", "name": "Google Workspace", "available_seats": 980, "requires_approval": False},
        {"product_id": "PROD-JIR-01", "name": "Jira", "available_seats": 450, "requires_approval": False},
        {"product_id": "PROD-GH-01", "name": "GitHub Enterprise", "available_seats": 920, "requires_approval": False},
        {"product_id": "PROD-AWS-01", "name": "AWS IAM Console", "available_seats": 50, "requires_approval": True},
        {"product_id": "PROD-DGR-01", "name": "DataGrip", "available_seats": 0, "requires_approval": True}
    ]

    print("[*] Running agent reasoning with real catalog IDs...")
    decision = agent.evaluate_request(sample_payload, sample_rules, sample_inventory)
    print("\n[+] Structured Decision Plan:")
    print(decision.model_dump_json(indent=2))
