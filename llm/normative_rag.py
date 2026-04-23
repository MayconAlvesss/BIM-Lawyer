from typing import Dict, Any
import os
import logging

try:
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    from langchain.vectorstores import Chroma
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.chat_models import ChatOpenAI
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

logger = logging.getLogger(__name__)

class NormativeRAG:
    """
    Enterprise RAG architecture integrating FAISS/ChromaDB with LangChain
    to map normative rules against building codes dynamically.
    """
    def __init__(self, db_path: str = "database/chroma_sim"):
        self.db_path = db_path
        self.vector_store = None
        self.qa_chain = None

        # In a real environment, this initializes the connection to the Vector DB
        if LANGCHAIN_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self._initialize_chain()
        else:
            logger.warning("LangChain or API keys missing. RAG running in local mock mode.")

    def _initialize_chain(self):
        try:
            embeddings = OpenAIEmbeddings()
            if os.path.exists(self.db_path):
                self.vector_store = Chroma(persist_directory=self.db_path, embedding_function=embeddings)
            else:
                # Fallback to in-memory for initialization if path doesn't exist yet
                self.vector_store = Chroma(embedding_function=embeddings)

            llm = ChatOpenAI(temperature=0.0, model_name="gpt-4-turbo")

            prompt_template = """
            You are a senior AEC compliance officer. Use the following pieces of retrieved building code to assist.
            If you don't know the answer based on the context, say you can't verify compliance.

            Context: {context}
            Question: {question}
            Answer:
            """
            PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )
            logger.info("LangChain RAG Chain Initialized Successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize LangChain: {e}")

    async def query_norm(self, query: str, jurisdiction: str = "ADA") -> Dict[str, str]:
        """ Queries the vector database for a specific normative code reference. """

        if self.qa_chain:
            try:
                res = self.qa_chain({"query": f"Under {jurisdiction}: {query}"})
                sources = "\n".join([doc.metadata.get("source", "Unknown") for doc in res.get("source_documents", [])])
                return {
                    "answer": res["result"],
                    "source": sources if sources else "No specific source retrieved."
                }
            except Exception as e:
                logger.error(f"RAG Error: {e}")

        # Mocking the RAG response for demonstration when Langchain/Keys aren't active
        if "door" in query.lower() and "ADA" in jurisdiction:
            return {
                "answer": "ADA Section 404.2.3 requires clear opening width of 32 inches (815 mm) minimum.",
                "source": "ADA Standards for Accessible Design (2010), §404.2.3"
            }
        elif "ramp" in query.lower() and "NBR" in jurisdiction:
            return {
                "answer": "NBR 9050:2015 §6.6.2.1 estabelece que a inclinação máxima de rampas deve ser de 8,33%.",
                "source": "ABNT NBR 9050:2015, Cláusula 6.6.2.1"
            }

        return {
            "answer": "Generic rule mapping provided. Please verify against technical document in context.",
            "source": f"Vector Index: {jurisdiction} Baseline"
        }

    async def generate_audit_suggestion(self, audit_result: Dict[str, Any]) -> str:
        """ Generates a natural language remediation step based on a violation. """
        element_id = audit_result.get("element_id")
        rule = audit_result.get("rule_violated")
        curr = audit_result.get("current_value")
        req = audit_result.get("required_value")

        if self.qa_chain:
            # Here it would use an LLM specifically to write the recommendation
            pass

        return (
            f"Action Required for {element_id}: The detected {rule} of {curr} fails to meet the "
            f"mandatory requirement of {req}. Recommendation: Review the geometry and ensure proper "
            f"clearances are maintained."
        )
