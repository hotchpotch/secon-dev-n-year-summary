from operator import itemgetter

from langchain_core.runnables import (
    ConfigurableField,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.runnables import chain as chain_decorator

from .diary_retriever import Diary, diary_retriever


@chain_decorator
def _filter_none(x):
    # None なら削除
    return list(filter(lambda y: y is not None, x))


@chain_decorator
def _combine_diaries(x):
    return [x["diary"]] + x["n_diaries"]


@chain_decorator
def _do_nothing(x):
    return None


def build_chain():
    retriever = RunnableLambda(diary_retriever)

    def _assine_n_diaries(x):
        return RunnablePassthrough.assign(
            diary=RunnablePassthrough(),
            n_diaries=itemgetter("n_diary_urls")
            | retriever.with_fallbacks([_do_nothing]).map(),
        )

    chain = retriever | _assine_n_diaries | _combine_diaries | _filter_none
    return chain
