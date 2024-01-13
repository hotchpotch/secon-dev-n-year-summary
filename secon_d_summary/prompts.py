from pathlib import Path

from langchain.prompts import ChatPromptTemplate

PROMPT_TEMPLATE_PATH = Path(__file__).parent / "prompt_templates"


def load_prompt(filaname: str):
    source = (PROMPT_TEMPLATE_PATH / filaname).read_text()
    return ChatPromptTemplate.from_template(source)
