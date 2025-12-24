from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document as LangChainDocument
from typing import List, Optional
import os
import pandas as pd
from ..config import settings
from ..schemas.chat import SourceCitation


class VectorService:
    """Vector store service for document embedding and retrieval"""

    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=settings.EMBEDDING_MODEL,
            base_url=settings.OLLAMA_BASE_URL
        )
        self.persist_directory = settings.CHROMA_PERSIST_DIR
        self.collection_name = settings.CHROMA_COLLECTION_NAME

        # Initialize vector store
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def add_documents(
        self,
        documents: List[LangChainDocument],
        ids: Optional[List[str]] = None
    ) -> None:
        """Add documents to the vector store"""
        self.vector_store.add_documents(documents=documents, ids=ids)

    def search(
        self,
        query: str,
        k: int = None,
        filter_dict: Optional[dict] = None
    ) -> List[LangChainDocument]:
        """Search for relevant documents"""
        k = k or settings.RETRIEVAL_K

        if filter_dict:
            results = self.vector_store.similarity_search(
                query,
                k=k,
                filter=filter_dict
            )
        else:
            results = self.vector_store.similarity_search(query, k=k)

        return results

    def search_with_scores(
        self,
        query: str,
        k: int = None
    ) -> List[tuple[LangChainDocument, float]]:
        """Search with relevance scores"""
        k = k or settings.RETRIEVAL_K
        return self.vector_store.similarity_search_with_score(query, k=k)

    def get_source_citations(
        self,
        query: str,
        k: int = None
    ) -> List[SourceCitation]:
        """Get formatted source citations for a query"""
        results = self.search_with_scores(query, k=k)

        citations = []
        for doc, score in results:
            citation = SourceCitation(
                source=doc.metadata.get("source", "Unknown"),
                content=doc.page_content,
                score=float(score),
                metadata=doc.metadata
            )
            citations.append(citation)

        return citations

    def delete_by_source(self, source: str) -> None:
        """Delete all documents from a specific source"""
        # Chroma doesn't have a direct delete by metadata, so we'd need to:
        # 1. Search for all docs with that source
        # 2. Delete by IDs
        # This is a placeholder for now
        pass

    def get_retriever(self, k: int = None):
        """Get a LangChain retriever"""
        k = k or settings.RETRIEVAL_K
        return self.vector_store.as_retriever(search_kwargs={"k": k})

    @staticmethod
    def load_legacy_csv_data(csv_path: str) -> List[LangChainDocument]:
        """Load data from legacy CSV format (for migration)"""
        df = pd.read_csv(csv_path)
        documents = []

        for i, row in df.iterrows():
            document = LangChainDocument(
                page_content=row["Category"] + " " + row["Fact"],
                metadata={
                    "source": "chopin_music_theory_facts.csv",
                    "source_type": "csv",
                    "category": row["Category"],
                    "row_index": i,
                    "user_uploaded": False
                }
            )
            documents.append(document)

        return documents


# Singleton instance
vector_service = VectorService()
