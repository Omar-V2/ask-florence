from operator import itemgetter

from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.vectorstores import FAISS


PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}

Question: {question}
"""


class ChatSession:

    def __init__(self, patient_id: int):
        ehr_entries = fetch_and_parse_ehr(patient_id)
        vector_store = FAISS.from_texts(ehr_entries, embedding=OpenAIEmbeddings())
        self._chain = self._create_chain(vector_store)

    def query(self, user_query: str) -> str:
        return self._chain.invoke(user_query)

    def _create_vector_store(self, ehr_entries: list[str]):
        return FAISS.from_texts(ehr_entries)

    def _create_chain(self, vector_store):
        model = ChatOpenAI()
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        retriever = vector_store.as_retriever()
        return (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )


def fetch_and_parse_ehr(patient_id) -> list[str]:
    return ["Jannic is in the hospital."]


session = ChatSession("1234")
print(session.query("Where is Jannic right now?"))
