from typing import Any, List
import ollama
from src.rag.service import get_retriever

CHAT_SYSTEM_PROMPT = """You are the internal Onboarding Assistant for AutoOnboard.
Your role is to answer questions for newly hired employees about their specific role, hardware, software tools, and company policies.

STRICT OPERATIONAL BOUNDARIES:
1. ONLY answer using the provided Employee Profile and Policy Excerpts.
2. If the user asks a question unrelated to their onboarding, workplace policies, assigned hardware, or company software tools (e.g., general world facts, coding help, casual chatting, personal advice), POLITELY REFUSE with:
   "I am only authorized to assist with questions regarding your onboarding, assigned equipment, software access, and company policies."
3. Do not invent policies or software licenses not listed in the context.
4. Keep answers concise, professional, and directly actionable.
"""

def generate_portal_chat_response(
    employee_context: dict[str, Any],
    query: str,
    chat_history: list[dict[str, str]]
) -> str:
    retriever = get_retriever()
    # Retrieve top 3 most relevant policy chunks
    citations = retriever.retrieve(query=query, top_k_candidates=10, final_top_k=3) #[cite: 18]

    # Format candidate tool & equipment context
    software_list = ", ".join([
        lic.get("software_products", {}).get("name", "") 
        for lic in employee_context.get("licenses", [])
    ]) or "Standard Corporate Suite"
    
    hardware_info = employee_context.get("hardware", {}).get("laptop", "Standard Laptop")

    context_str = f"""
### EMPLOYEE PROFILE
- Role: {employee_context.get('role')}
- Department: {employee_context.get('department')}
- Location: {employee_context.get('work_location')}
- Assigned Laptop: {hardware_info}
- Assigned Software: {software_list}

### POLICY EXCERPTS
""" + "\n\n".join([
        f"[{doc['policy_name']} - {doc['section_title']}]: {doc['content']}" #[cite: 18]
        for doc in citations
    ])

    messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
    
    # Append recent conversation turns for light multi-turn context
    for turn in chat_history[-4:]:
        messages.append(turn)

    user_prompt = f"Context:\n{context_str}\n\nQuestion: {query}"
    messages.append({"role": "user", "content": user_prompt})

    response = ollama.chat(
        model="granite4.2:3b", # or your configured local model
        messages=messages,
        options={"temperature": 0.1} # low temperature for strict factual adherence
    )

    return response["message"]["content"]