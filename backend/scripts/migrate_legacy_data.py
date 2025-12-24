"""
Script to migrate legacy CSV data to the new vector store
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vector_service import vector_service


def migrate_csv_data():
    """Migrate data from legacy CSV to new vector store"""
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "legacy",
        "chopin_music_theory_facts.csv"
    )

    print(f"Loading data from {csv_path}")
    documents = vector_service.load_legacy_csv_data(csv_path)

    print(f"Found {len(documents)} documents")
    print("Adding documents to vector store...")

    # Generate IDs for the documents
    ids = [f"legacy_csv_{i}" for i in range(len(documents))]

    vector_service.add_documents(documents, ids=ids)

    print("Migration complete!")
    print(f"Added {len(documents)} documents to the vector store")


if __name__ == "__main__":
    migrate_csv_data()
