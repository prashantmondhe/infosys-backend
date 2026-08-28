import os
import tempfile
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config.env_config import envConfig
from config.llm_config import (
    GEMINI_EMBEDDING_MODEL,
    EMBEDDING_DIMENSION,
)


class EnterprisePDFIndexer:

    def __init__(
        self,
        data_root_path: str | None = None,
        vector_db_path: str | None = None,
        google_api_key: str | None = None,
    ):
        # -------------------------------------------------
        # Project paths
        # -------------------------------------------------

        script_dir = os.path.dirname(os.path.abspath(__file__))

        # vector_indexer.py:
        # backend/GenAI/ingestion_pipeline/embedding_jobs/
        #
        # Go up:
        # embedding_jobs -> ingestion_pipeline
        # -> GenAI -> backend -> project root
        project_root = os.path.abspath(
            os.path.join(
                script_dir,
                "..",
                "..",
                "..",
                "..",
            )
        )

        self.data_root = data_root_path or os.path.join(
            project_root,
            "data",
        )

        self.vector_db_path = vector_db_path or os.path.join(
            project_root,
            "vector_db",
        )

        # -------------------------------------------------
        # Gemini API key
        # -------------------------------------------------

        api_key = (
            google_api_key
            or envConfig.GEMINI_API_KEY
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Please configure it in the environment."
            )

        # -------------------------------------------------
        # Gemini Embedding 2
        # -------------------------------------------------

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=GEMINI_EMBEDDING_MODEL,
            google_api_key=api_key,
            output_dimensionality=EMBEDDING_DIMENSION,
        )

        # -------------------------------------------------
        # Document chunking
        # -------------------------------------------------

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

        # -------------------------------------------------
        # ChromaDB
        # -------------------------------------------------

        self.vector_store = Chroma(
            persist_directory=self.vector_db_path,
            embedding_function=self.embeddings,
            collection_name="documents",
        )

    # -----------------------------------------------------
    # Index document
    # -----------------------------------------------------

    def process_and_index(
        self,
        document,
        file_bytes: bytes,
    ):

        temp_pdf_path = None

        try:

            # ---------------------------------------------
            # Save PDF temporarily
            # ---------------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as temp_file:

                temp_file.write(file_bytes)
                temp_pdf_path = temp_file.name

            # ---------------------------------------------
            # Load PDF
            # ---------------------------------------------

            loader = PyMuPDFLoader(
                temp_pdf_path
            )

            pages = loader.load()

            all_chunks = []

            # ---------------------------------------------
            # Chunk pages
            # ---------------------------------------------

            for page in pages:

                page_number = (
                    page.metadata.get("page", 0) + 1
                )

                chunks = self.text_splitter.split_text(
                    page.page_content
                )

                for chunk_index, chunk_text in enumerate(
                    chunks
                ):

                    chunk_id = (
                        f"{document.id}_"
                        f"{page_number}_"
                        f"{chunk_index}"
                    )

                    metadata = {
                        "document_id": str(
                            document.id
                        ),
                        "title": document.title,
                        "department": document.department,
                        "owner_id": str(
                            document.owner_id
                        ),
                        "access_scope": (
                            document.access_scope
                        ),
                        "confidentiality": (
                            document.confidentiality
                        ),
                        "page_number": page_number,
                        "chunk_id": chunk_id,
                    }

                    all_chunks.append(
                        {
                            "text": chunk_text,
                            "metadata": metadata,
                        }
                    )

            if not all_chunks:

                raise ValueError(
                    f"No text chunks extracted from "
                    f"'{document.title}'."
                )

            # ---------------------------------------------
            # Prepare Chroma data
            # ---------------------------------------------

            texts = [
                chunk["text"]
                for chunk in all_chunks
            ]

            metadatas = [
                chunk["metadata"]
                for chunk in all_chunks
            ]

            ids = [
                chunk["metadata"]["chunk_id"]
                for chunk in all_chunks
            ]

            # ---------------------------------------------
            # Store in ChromaDB
            # ---------------------------------------------

            self.vector_store.add_texts(
                texts=texts,
                metadatas=metadatas,
                ids=ids,
            )

            print(
                f"Indexed '{document.title}' "
                f"with {len(all_chunks)} chunks."
            )

        finally:

            if (
                temp_pdf_path
                and os.path.exists(temp_pdf_path)
            ):
                os.remove(temp_pdf_path)