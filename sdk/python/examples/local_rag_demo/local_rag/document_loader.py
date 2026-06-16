from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    doc_id: str
    path: str
    text: str


def load_markdown_documents(docs_dir: Path) -> list[Document]:
    """
    Load all markdown documents from a local directory.

    doc_id is derived from the filename:
    refund_policy.md -> refund_policy
    """
    if not docs_dir.exists():
        raise FileNotFoundError(f"Docs directory does not exist: {docs_dir}")

    documents: list[Document] = []

    for path in sorted(docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        documents.append(
            Document(
                doc_id=path.stem,
                path=str(path),
                text=text,
            )
        )

    return documents