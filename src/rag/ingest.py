import re
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

POLICY_DIR = Path("./Policies")
CHROMA_PATH = "./data/chroma_db"

def parse_markdown_policy(file_path: Path):
    """
    Parses policy files by extracting the Document ID and linking
    sub-clauses (e.g. 2.1, 3.2) directly to rule_id metadata.
    """
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Extract Document ID from header (e.g., # POL-SAAS-001: ...)
    doc_id_match = re.search(r"#\s*(POL-[A-Z]+(?:-\d+)?)", lines[0])
    doc_prefix = doc_id_match.group(1).rsplit("-", 1)[0] if doc_id_match else "POL-GEN"
    
    docs = []
    current_section = "General"
    current_clause_text = []
    current_rule_id = f"{doc_prefix}-0.0"

    for line in lines[1:]:
        line_clean = line.strip()
        if not line_clean:
            continue

        # Detect Section headings (e.g., ## Section 2: ...)
        if line_clean.startswith("## "):
            current_section = line_clean.replace("## ", "").strip()
            continue

        # Detect sub-clauses (e.g., 2.1. Rule Name: ...)
        clause_match = re.match(r"^(\d+\.\d+)\.\s*(.*)", line_clean)
        if clause_match:
            # Save previous clause if present
            if current_clause_text:
                docs.append(Document(
                    page_content=" ".join(current_clause_text),
                    metadata={
                        "source": file_path.name,
                        "rule_id": current_rule_id,
                        "section": current_section
                    }
                ))
                current_clause_text = []
            
            clause_num = clause_match.group(1)
            current_rule_id = f"{doc_prefix}-{clause_num}"
            current_clause_text.append(line_clean)
        else:
            current_clause_text.append(line_clean)

    # Append remaining clause
    if current_clause_text:
        docs.append(Document(
            page_content=" ".join(current_clause_text),
            metadata={
                "source": file_path.name,
                "rule_id": current_rule_id,
                "section": current_section
            }
        ))

    return docs

def build_vector_store():
    print(f"[*] Parsing policies from {POLICY_DIR}...")
    all_docs = []
    for policy_file in sorted(POLICY_DIR.glob("*.md")):
        parsed = parse_markdown_policy(policy_file)
        all_docs.extend(parsed)
        print(f"    - {policy_file.name}: Extracted {len(parsed)} structured rule blocks")

    print(f"[*] Total indexed policy rules: {len(all_docs)}")

    print("[*] Generating embeddings via sentence-transformers/all-MiniLM-L6-v2...")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = Chroma.from_documents(
        documents=all_docs,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH
    )
    print(f"[+] Vector database persisted successfully at {CHROMA_PATH}")

if __name__ == "__main__":
    build_vector_store()
