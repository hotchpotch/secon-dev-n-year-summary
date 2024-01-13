from langchain_core.runnables import (
    ConfigurableField,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

from .diary_retriever import Diary, diary_retriever


def build_chain():
    retriever = RunnableLambda(diary_retriever)
    chain = retriever | {
        "main_diary": RunnablePassthrough(),
    }
    return chain
