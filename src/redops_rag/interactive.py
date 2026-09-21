"""Small interactive shell for source-grounded RedOps queries."""

from __future__ import annotations

from .service import RagService
from .status import collect_status, render_status

HELP = """Commands:
  /help       show this help
  /status     show provider, index, and execution status
  /stats      show index counts
  /sources    toggle source details after each answer
  /generate   use the configured provider for answers
  /extractive use local retrieval-only answers
  /quit       exit the shell

Enter a normal sentence to query the knowledge base."""


def run_interactive(*, top_k: int | None = None, generate: bool = True) -> None:
    service = RagService()
    show_sources = True
    print("RedOps interactive · type /help for commands, /quit to exit")
    print(render_status(collect_status(service.settings)))
    while True:
        try:
            question = input("\nredops> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return
        if not question:
            continue
        command = question.lower()
        if command in {"/quit", "/exit", ":q"}:
            print("Bye.")
            return
        if command == "/help":
            print(HELP)
            continue
        if command == "/status":
            print(render_status(collect_status(service.settings)))
            continue
        if command == "/stats":
            print(service.store.stats())
            continue
        if command == "/sources":
            show_sources = not show_sources
            print(f"Source details: {'on' if show_sources else 'off'}")
            continue
        if command == "/generate":
            generate = True
            print("Answer mode: configured provider")
            continue
        if command == "/extractive":
            generate = False
            print("Answer mode: local retrieval-only")
            continue
        try:
            result = service.query(question, top_k=top_k, generate=generate)
        except Exception as exc:  # noqa: BLE001 - keep the REPL alive after provider errors
            print(f"Error: {exc}")
            continue
        print(f"\n{result['answer'] or 'No generated answer; review the sources below.'}")
        if show_sources:
            print(f"\nSources ({len(result['sources'])}):")
            for index, source in enumerate(result["sources"], 1):
                print(f"  [{index}] {source['title']} · {source['path']}")
                print(f"      {source['source_url']}")
