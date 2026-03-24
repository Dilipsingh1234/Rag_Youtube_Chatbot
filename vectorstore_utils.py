import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from transcript_utils import get_youtube_transcript


def build_and_save_vectorstore(video_id: str, db_path: str):
    print("Fetching transcript...")
    transcript = get_youtube_transcript(video_id)

    print("Splitting transcript into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.create_documents([transcript])

    print("Creating embeddings and FAISS index...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(chunks, embeddings)

    vector_store.save_local(db_path)
    print(f"Saved vector store to: {db_path}")

    return vector_store


def load_or_create_vectorstore(video_id: str):
    db_path = f"faiss_index_{video_id}"
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    if os.path.exists(db_path):
        print("Loading existing FAISS index...")
        vector_store = FAISS.load_local(
            db_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        print("No existing FAISS index found.")
        vector_store = build_and_save_vectorstore(video_id, db_path)

    return vector_store