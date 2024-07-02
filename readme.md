main.py:
调用lc_rag (langchain rag), g_a (google api), llm_tool(chatbot), 的工具进入一个agent，并在chainlit端打开。

lc_rag.py:
基本的langchain rag 的工具。需要进一步做到vector database的persistence。并且需要更好结合调取的document信息。

g_a.py:
用google api调用网上的信息，并进行rag

llm_tool.py:
设置一个openai的client，并保存context来做到持续性的chatbot功能



rag.py:
调用了openai 的file search agent 用的 api的vector db(client.beta.vector_store module).
initialize_db.py:
vector db 的创建在initialize_db中完成，并具有persistence。rag.py调用了initiailze_db的vector db