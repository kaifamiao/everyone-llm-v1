from types import NoneType
from typing import Dict

from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_json_agent

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.utilities import SQLDatabase
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

from kfm_core.kfm_chatllama.KfmChatLlama import kfm_llm
from kfm_framework.interface.kfm_chain.KfmChain import KfmChain

from kfm_core.kfm_sys.log_config import setup_logger

kfm_logger = setup_logger(__name__)

class China_Agent1(KfmChain):

    def __init__(self):
        kfm_logger.debug(f"China_Agent1 initialization")

    def execute(self, input: Dict) -> object:
        model = input.get('model')
        a = agent(model)
        return a.reponse()


class agent:
    import json
    from types import NoneType

    from langchain.agents import Agent, AgentExecutor, initialize_agent, AgentType, create_structured_chat_agent
    from langchain.chains.llm import LLMChain
    from langchain_community.chat_message_histories import SQLChatMessageHistory
    from langchain_community.utilities import SQLDatabase
    from langchain_core.chat_history import BaseChatMessageHistory
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.runnables import RunnableWithMessageHistory


    from langchain_core.messages import HumanMessage
    from langgraph.prebuilt import create_react_agent
    from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_json_agent

    from langchain_core.messages import SystemMessage, HumanMessage

    def mysql_db(self, username, password, host, port, database):
        print("mysql db ....")
        url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        return SQLDatabase.from_uri(url)

    def __init__(self,kfm_llm):
        kfm_logger.debug(f"agent initialization use model is {kfm_llm}")
        self.llm = kfm_llm
        self.db = self.mysql_db("root", "休闲鞋", "localhost", 3306,  "chatbot_db")
        print(self.db.run("select * from chat_messages"))

        SQL_PREFIX = """You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the below tools. Only use the information returned by the below tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        To start you should ALWAYS look at the tables in the database to see what you can query.
        Do NOT skip this step.
        Then you should query the schema of the most relevant tables."""

        system_message = SystemMessage(content=SQL_PREFIX)
        prompt = ChatPromptTemplate.from_messages([
            ("system", SQL_PREFIX),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        toolkit = SQLDatabaseToolkit(db=self.db, llm=kfm_llm)

        tools = toolkit.get_tools()

        agent_executor = create_json_agent(kfm_llm, toolkit, state_modifier=system_message)

        def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
            # if session_id not in store:
            #     store[session_id] = InMemoryHistory()
            # return store[session_id]
            return SQLChatMessageHistory(session_id, connection="sqlite:///db_v3.db")

        self.chain_with_history = RunnableWithMessageHistory(
            agent_executor,
            get_by_session_id,
            input_messages_key="input",
            history_messages_key="history",
        )


    def reponse(self):
        return self.chain_with_history

if __name__ == '__main__':
    a =agent(kfm_llm=kfm_llm)
    for chunk in a.reponse().stream(
        {"input": [HumanMessage(content="数据表多少几条记录?")]},
        config={'configurable': {'session_id': 'xxxxx'}}
    ):
        print(chunk, end='', flush=True)
        print(".")
    print("\n")
    # for chunk in a.chain_with_history().stream(
    #         {"input": [HumanMessage(content="数据表user_settings有多少几条记录?")]},
    #         config={'configurable': {'session_id': 'xxxxx'}}
    # ):
    #     if type(chunk.get("steps")) is not NoneType:
    #         # json_data =json.loads(chunk.get("steps"))
    #         print(type(chunk.get("steps")), end='', flush=True)
    #         print(chunk.get("steps"), end='', flush=True)
    #     # print(chunk.get("output"), end='', flush=True)
    #
    #     print("----")
