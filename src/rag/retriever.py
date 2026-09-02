from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.schemas.agent_payload import PolicyCitation

CHROMA_PATH = "./data/chroma_db"

class PolicyRetriever:
    def __init__(self, persist_directory: str = CHROMA_PATH):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )

    def retrieve_citations(self, query: str, k: int = 3) -> list[PolicyCitation]:
        results = self.vectorstore.similarity_search(query, k=k)
        citations = []
        for doc in results:
            citations.append(
                PolicyCitation(
                    rule_id=doc.metadata.get("rule_id", "POL-UNKNOWN"),
                    document_name=doc.metadata.get("source", "Unknown"),
                    quote=doc.page_content.strip()
                )
            )
        return citations

if __name__ == "__main__":
    retriever = PolicyRetriever()
    test_query = "What happens if a software license has zero available seats?"
    citations = retriever.retrieve_citations(test_query, k=2)
    print(f"\n[*] Query: {test_query}\n")
    for c in citations:
        print(f"[{c.rule_id}] ({c.document_name}):")
        print(f"  \"{c.quote}\"\n")
