from dotenv import load_dotenv

from helper import extract_video_id
from vectorstore_utils import load_or_create_vectorstore
from rag_chain import build_rag_chain


def main():
    load_dotenv()

    video_input = input("Enter YouTube URL or video ID: ").strip()
    video_id = extract_video_id(video_input)

    if not video_id:
        print("Invalid YouTube URL or video ID.")
        return

    print(f"\nUsing video ID: {video_id}")
    vector_store = load_or_create_vectorstore(video_id)
    chain = build_rag_chain(vector_store)

    while True:
        query = input("\nAsk a question about the video (or type 'exit'): ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            print("Please enter a question.")
            continue

        try:
            result = chain.invoke(query)
            print("\nAnswer:")
            print(result)
        except Exception as e:
            print(f"\nError while generating answer: {e}")


if __name__ == "__main__":
    main()