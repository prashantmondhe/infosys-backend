from dataclasses import dataclass
from pathlib import Path
from .embedding_jobs.vector_indexer import EnterprisePDFIndexer


# ---------------------------------------------------------
# Synthetic/demo document metadata
# ---------------------------------------------------------

@dataclass
class EnterpriseDocument:
    id: str
    title: str
    department: str
    owner_id: str
    access_scope: str
    confidentiality: str


CATEGORY_CONFIG = {
    "engineering_guides": {
        "department": "Engineering",
        "confidentiality": "internal",
    },
    "hr_policies": {
        "department": "HR",
        "confidentiality": "internal",
    },
    "project_manuals": {
        "department": "Project Management",
        "confidentiality": "internal",
    },
    "sales_assets": {
        "department": "Sales",
        "confidentiality": "internal",
    },
    "sops": {
        "department": "Operations",
        "confidentiality": "internal",
    },
}


def build_document(
    pdf_path: Path,
    category: str,
) -> EnterpriseDocument:

    config = CATEGORY_CONFIG[category]

    return EnterpriseDocument(
        id=(
            f"demo_{category}_"
            f"{pdf_path.stem.lower().replace(' ', '_')}"
        ),
        title=pdf_path.stem,
        department=config["department"],
        owner_id="demo_admin",
        access_scope="enterprise",
        confidentiality=config["confidentiality"],
    )


def ingest_category(
    indexer: EnterprisePDFIndexer,
    data_root: Path,
    category: str,
) -> None:

    category_path = data_root / category

    if not category_path.exists():
        raise FileNotFoundError(
            f"Category folder not found: {category_path}"
        )

    pdf_files = sorted(
        category_path.glob("*.pdf")
    )

    if not pdf_files:
        print(
            f"No PDFs found in '{category_path}'."
        )
        return

    for pdf_path in pdf_files:

        print(
            f"\nIndexing: {pdf_path.name}"
        )

        document = build_document(
            pdf_path=pdf_path,
            category=category,
        )

        file_bytes = pdf_path.read_bytes()

        indexer.process_and_index(
            document=document,
            file_bytes=file_bytes,
        )


def main():

    # -----------------------------------------------------
    # Project root
    # -----------------------------------------------------

    project_root = Path(__file__).resolve().parents[3]

    data_root = project_root / "data"
    vector_db_path = project_root / "vector_db"

    print("=" * 60)
    print("ENTERPRISE DOCUMENT INGESTION")
    print("=" * 60)

    print(f"Data root: {data_root}")
    print(f"Vector DB: {vector_db_path}")

    if not data_root.exists():
        raise FileNotFoundError(
            f"Data directory not found: {data_root}"
        )

    # -----------------------------------------------------
    # Existing indexer
    # -----------------------------------------------------

    indexer = EnterprisePDFIndexer(
        data_root_path=str(data_root),
        vector_db_path=str(vector_db_path),
    )

    # -----------------------------------------------------
    # Ingest ALL five categories
    # -----------------------------------------------------

    categories = [
        "engineering_guides",
        "hr_policies",
        "project_manuals",
        "sales_assets",
        "sops",
    ]

    for category in categories:

        print("\n" + "=" * 60)
        print(
            f"PROCESSING CATEGORY: {category}"
        )
        print("=" * 60)

        ingest_category(
            indexer=indexer,
            data_root=data_root,
            category=category,
        )

    print("\n" + "=" * 60)
    print("ALL DOCUMENTS INGESTED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()