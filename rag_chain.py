from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser


def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)


def build_rag_chain(vector_store):
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    prompt = PromptTemplate(
        template="""
You are a helpful assistant.
Answer ONLY from the provided transcript context.
If the context is insufficient, say: "I don't know based on the transcript."
Keep the answer concise and to the point.

Context:
{context}

Question:
{question}
""",
        input_variables=["context", "question"]
    )

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    parser = StrOutputParser()
    main_chain = parallel_chain | prompt | llm | parser

    return main_chain