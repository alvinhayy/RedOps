import json

from redops_rag.rag_mcp import RagMcpServer


class FakeStore:
    def stats(self):
        return {"documents": 2, "chunks": 4, "documents_by_corpus": {"knowledge": 1, "writeups": 1}}


class FakeService:
    def __init__(self):
        self.store = FakeStore()
        self.calls = []

    def query(self, question, *, top_k, generate, corpus):
        self.calls.append((question, top_k, generate, corpus))
        return {"question": question, "answer": None, "sources": [{"corpus": corpus}]}


def test_rag_mcp_searches_each_corpus():
    service = FakeService()
    server = RagMcpServer(service)

    listed = server.dispatch({"method": "tools/list", "id": 1})
    assert {tool["name"] for tool in listed["result"]["tools"]} == {
        "search_knowledge",
        "search_writeups",
        "knowledge_stats",
    }
    result = server.call_tool("search_writeups", {"query": "case", "n_results": 3})
    assert json.loads(result["content"][0]["text"])["sources"][0]["corpus"] == "writeups"
    assert service.calls == [("case", 3, False, "writeups")]


def test_rag_mcp_rejects_invalid_queries():
    result = RagMcpServer(FakeService()).call_tool("search_knowledge", {"query": "", "n_results": 2})
    assert result["isError"] is True
