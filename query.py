import docx
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.vectorstores import FAISS

from constants import BUCKET_NAME
from utils import get_uk_timestamp_utc_format
import time


from constants import EHR_BASE_PATH
from query_constants import (
    PROMPT_TEMPLATE,
    CONDITION_DENY_CATEGORIES,
    USER_DENY_MESSAGE,
    MEDICAL_DICTIONARY
)
from chat_history import upload_chat_history_to_s3


class ChatSession:
    def __init__(self, patient_number: str):
        self._patient_number = patient_number
        self._model = ChatOpenAI()
        self._prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        self._chat_key = patient_number + "_" + str(time.time())
        self._chat_history = []
        self._chat_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{self._chat_key}"
        upload_chat_history_to_s3(self._chat_key, [])

    def query(self, user_query: str) -> str:
        ehr_entries = _fetch_and_parse_ehr(self._patient_number)
        vector_store = FAISS.from_texts(ehr_entries, embedding=OpenAIEmbeddings())
        chain = (
            {
                "condition_deny_categories": lambda _: "\n,".join(
                    CONDITION_DENY_CATEGORIES
                ),
                "context": vector_store.as_retriever(),
                "user_deny_message": lambda _: USER_DENY_MESSAGE,
                "question": RunnablePassthrough(),
                "medical_dictionary": (
                    lambda _: "\n".join(
                        f"{k}: {v}" for k, v in MEDICAL_DICTIONARY.items()
                    )
                ),
            }
            | self._prompt
            | self._model
            | StrOutputParser()
        )
        response = chain.invoke(user_query)
        self._update_chat_history(user_query, response)
        return response

    def _update_chat_history(self, user_query: str, response: str) -> None:
        # Add user query
        self._chat_history.append((
            get_uk_timestamp_utc_format(),
            "Next of Kin",
            user_query
        ))

        # Add response
        self._chat_history.append((
            get_uk_timestamp_utc_format(),
            "Florence",
            response
        ))

        upload_chat_history_to_s3(self._chat_key, self._chat_history)
        _add_chat_to_ehr(self._patient_number, self._chat_url)


def _fetch_and_parse_ehr(patient_number: str) -> list[str]:
    doc = docx.Document(str(EHR_BASE_PATH / (patient_number + ".docx")))

    fullText = []
    for paragraph in doc.paragraphs:
        fullText.append(paragraph.text)

    return '\n'.join(fullText).split("---")


def _add_chat_to_ehr(patient_number: str, chat_url: str) -> None:
    doc = docx.Document(str(EHR_BASE_PATH / (patient_number + ".docx")))
    timestamp = get_uk_timestamp_utc_format()

    # Add a new paragraph with '---'
    doc.add_paragraph(
        f"---\n[{timestamp}]\n\nNext of kin initiated a conversation with Florence."
        f" View chat at:\n{chat_url}"
    )

    # Save the modified document
    doc.save(str(EHR_BASE_PATH / (patient_number + ".docx")))
