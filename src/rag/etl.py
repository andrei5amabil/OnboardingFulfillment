import os
import pickle
import re
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from rank_bm25 import BM25Okapi

POLICIES_DIR = Path("Policies")
CHROMA_PATH = Path("chroma_db")
BM25_INDEX_PATH = CHROMA_PATH / "bm25_index.pkl"
COLLECTION_NAME = "policies"


def tokenize_for_bm25(text: str) -> list[str]:
    """Tokenize text preserving hyphenated policy clause codes (e.g., 'pol-hdw-201')."""
    return re.findall(r"[a-zA-Z0-9_\-]+", text.lower())


def extract_clause_tags(text: str) -> str:
    """Extract policy clause codes like [POL-HDW-201] to store as comma-separated tags."""
    matches = re.findall(r"\[(POL-[A-Z]+-\d+)\]", text)
    return ",".join(matches)


def run_etl():
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)

    # 1. Initialize Persistent ChromaDB Client & Dense Embedder
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Reset collection to maintain idempotency
    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = chroma_client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
        metadata={"hnsw:space": "cosine"},
    )

    # 2. Stage 1 Splitter: Extract Parent Document Sections by Header
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "policy_name"),
            ("##", "section_title"),
        ],
        strip_headers=False,
    )

    # 3. Stage 2 Splitter: 25% Overlap on Child Chunks (chunk_size=500, chunk_overlap=125)
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=125,
        separators=["\n- **", "\n\n", "\n", " ", ""],
    )

    documents: list[str] = []
    metadatas: list[dict] = []
    ids: list[str] = []
    bm25_corpus: list[list[str]] = []
    parent_store: dict[str, str] = {}

    # 4. Ingest and Process Each Markdown Policy
    for file_path in sorted(POLICIES_DIR.glob("*.md")):
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        sections = header_splitter.split_text(raw_text)

        for sec_idx, section in enumerate(sections):
            parent_id = f"{file_path.stem}_SEC_{sec_idx:02d}"
            parent_content = section.page_content
            parent_store[parent_id] = parent_content

            policy_name = section.metadata.get("policy_name", file_path.stem)
            section_title = section.metadata.get("section_title", "General")

            # Split parent section into overlapping child chunks
            child_chunks = child_splitter.split_text(parent_content)

            for chk_idx, chunk in enumerate(child_chunks):
                child_id = f"{parent_id}_CHK_{chk_idx:02d}"
                clause_tags = extract_clause_tags(chunk)

                documents.append(chunk)
                ids.append(child_id)

                # ChromaDB metadata must use primitive types (str, int, float, bool)
                metadata_entry = {
                    "source_file": file_path.name,
                    "policy_code": file_path.stem,
                    "policy_name": policy_name,
                    "section_title": section_title,
                    "parent_id": parent_id,
                    "parent_content": parent_content,
                    "clause_tags": clause_tags,
                    "chunk_index": chk_idx,
                }
                metadatas.append(metadata_entry)

                # Tokenize child text for BM25
                bm25_corpus.append(tokenize_for_bm25(chunk))

    # 5. Populate ChromaDB Collection
    if documents:
        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        print(f"Indexed {len(documents)} child chunks into ChromaDB.")

    # 6. Fit & Serialize BM25 Index alongside Parent Document References
    bm25_model = BM25Okapi(bm25_corpus)
    bm25_payload = {
        "model": bm25_model,
        "ids": ids,
        "documents": documents,
        "metadatas": metadatas,
        "parent_store": parent_store,
    }

    with open(BM25_INDEX_PATH, "wb") as f:
        pickle.dump(bm25_payload, f)
    print(f"Persisted BM25 artifact and parent map to {BM25_INDEX_PATH}.")


if __name__ == "__main__":
    run_etl()