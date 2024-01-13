from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    ConfigurableField,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.runnables import chain as chain_decorator
from langchain_openai import ChatOpenAI

from secon_d_summary.fake import FakeChatModel

from .diary_retriever import Diary, diary_retriever
from .prompts import load_prompt


@chain_decorator
def _filter_none(x):
    # None なら削除
    return list(filter(lambda y: y is not None, x))


@chain_decorator
def _combine_diaries(x):
    return [x["diary"]] + x["n_diaries"]


@chain_decorator
def _do_nothing(_):
    return None


@chain_decorator
def _diaries_formatter(diaries: list[Diary]) -> dict[str, str]:
    results = []
    for diary in diaries:
        title = diary["title"][0:200]
        text = diary["text"][0:2000]
        results.append(f"## {title}\n{text}\n")
    return {"diary": " \n".join(results)}


def build_chain():
    retriever = RunnableLambda(diary_retriever)
    model = ChatOpenAI(model="gpt-4-1106-preview")
    # model = FakeChatModel()
    prompt = load_prompt("summary.txt")

    def _assine_n_diaries(x):
        return RunnablePassthrough.assign(
            diary=RunnablePassthrough(),
            n_diaries=itemgetter("n_diary_urls")
            | retriever.with_fallbacks([_do_nothing]).map(),
        )

    chain = (
        retriever
        | _assine_n_diaries
        | _combine_diaries
        | _filter_none
        | {
            "diaries": RunnablePassthrough(),
            "summary": _diaries_formatter | prompt | model | StrOutputParser(),
        }
    )
    return chain
