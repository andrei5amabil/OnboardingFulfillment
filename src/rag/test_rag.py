# test_rag.py
from retriever import PolicyRetriever

retriever = PolicyRetriever()
results = retriever.retrieve("remote employee laptop equipment dispatch courier")

for res in results:
    print(f"[{res['policy_code']}] {res['section_title']} (Score: {res['rerank_score']:.4f})")
    print(f"Clauses: {res['clause_tags']}")
    print(res['content'][:200] + "...\n")