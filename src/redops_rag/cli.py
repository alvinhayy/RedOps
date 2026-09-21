from __future__ import annotations

import argparse
import json

from .execution import CommandRunner, ExecutionError
from .providers import PROVIDERS
from .service import RagService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="redops", description="RedOps pentest RAG")
    subparsers = parser.add_subparsers(dest="command", required=True)

    providers_parser = subparsers.add_parser("providers", help="list supported model providers")
    providers_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    status_parser = subparsers.add_parser("status", help="show safe provider/index/runtime status")
    status_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    install_parser = subparsers.add_parser("install-cli", help="install RedOps adapters for agent CLIs")
    install_parser.add_argument("target", choices=("codex", "claude", "opencode", "all"))
    install_parser.add_argument("--dry-run", action="store_true", help="show paths without writing")
    install_parser.add_argument("--force", action="store_true", help="replace existing RedOps adapter files")

    ingest_parser = subparsers.add_parser("ingest", help="index Markdown knowledge")
    ingest_parser.add_argument("--force", action="store_true", help="rebuild changed embeddings")

    query_parser = subparsers.add_parser("query", help="retrieve or answer a question")
    query_parser.add_argument("question")
    query_parser.add_argument("--top-k", type=int)
    query_parser.add_argument("--no-generate", action="store_true")

    interactive_parser = subparsers.add_parser(
        "interactive", aliases=["shell"], help="open an interactive RAG query shell"
    )
    interactive_parser.add_argument("--top-k", type=int)
    interactive_parser.add_argument("--no-generate", action="store_true")

    subparsers.add_parser("stats", help="show index statistics")
    serve_parser = subparsers.add_parser("serve", help="run the HTTP API")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", default=8000, type=int)

    exegol_parser = subparsers.add_parser("exegol", help="run authorized tools via Exegol")
    exegol_subparsers = exegol_parser.add_subparsers(dest="exegol_command", required=True)
    exegol_subparsers.add_parser("status", help="show Exegol container status (read-only)")
    exec_parser = exegol_subparsers.add_parser("exec", help="execute an argv command")
    exec_parser.add_argument("exec_args", nargs=argparse.REMAINDER)
    subparsers.add_parser("exegol-mcp", help="run the optional Exegol MCP stdio adapter")
    waf_parser = subparsers.add_parser("waf", help="bounded WAF timing benchmark")
    waf_sub = waf_parser.add_subparsers(dest="waf_command", required=True)
    bench = waf_sub.add_parser("benchmark", help="measure baseline/test timing")
    bench.add_argument("--baseline-url", required=True)
    bench.add_argument("--test-url", required=True)
    bench.add_argument("--amplifier-url")
    bench.add_argument("--samples", type=int, default=10)
    bench.add_argument("--delay", type=float, default=1.0)
    bench.add_argument("--lab-mode", action="store_true", help="allow approved staging/local amplifier")
    bench.add_argument("--allowlist", action="append", default=[])
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "providers":
        rows = [
            {
                "id": item.id,
                "name": item.display_name,
                "kind": item.kind,
                "default_base_url": item.default_base_url,
                "api_key_env": item.api_key_env,
                "default_chat_model": item.default_chat_model,
                "default_embedding_model": item.default_embedding_model,
                "cli_model": item.cli_model,
                "notes": item.notes,
            }
            for item in PROVIDERS
        ]
        if args.json:
            print(json.dumps(rows, indent=2, ensure_ascii=False))
        else:
            for row in rows:
                print(f"{row['id']}: {row['name']} ({row['kind']}) — {row['notes']}")
        return
    if args.command == "status":
        from .status import collect_status, render_status

        result = collect_status()
        print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else render_status(result))
        return
    if args.command == "install-cli":
        from .integrations import install_integrations

        print(json.dumps(install_integrations(args.target, dry_run=args.dry_run, force=args.force), indent=2))
        return
    if args.command == "exegol-mcp":
        from .exegol_mcp import serve_stdio

        serve_stdio()
        return
    if args.command == "exegol":
        try:
            runner = CommandRunner()
            if args.exegol_command == "status":
                result = runner.status()
            else:
                result = runner.run(args.exec_args)
            print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False))
        except ExecutionError as exc:
            print(json.dumps(exc.as_dict(), indent=2, ensure_ascii=False))
            raise SystemExit(1) from exc
        return
    if args.command == "waf":
        from .waf import WafBenchmarkError, WafTimingBenchmark

        try:
            result = WafTimingBenchmark(lab_mode=args.lab_mode, allowlist=tuple(args.allowlist)).run(
                baseline_url=args.baseline_url, test_url=args.test_url, amplifier_url=args.amplifier_url,
                samples=args.samples, delay=args.delay,
            )
        except (WafBenchmarkError, ValueError) as exc:
            print(json.dumps({"error": "invalid_benchmark", "message": str(exc)}, indent=2))
            raise SystemExit(2) from exc
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.command in {"interactive", "shell"}:
        from .interactive import run_interactive

        run_interactive(top_k=args.top_k, generate=not args.no_generate)
        return

    service = RagService()
    if args.command == "ingest":
        result = service.ingest(force=args.force)
    elif args.command == "query":
        result = service.query(args.question, args.top_k, not args.no_generate)
    elif args.command == "stats":
        result = service.store.stats()
    else:
        import uvicorn

        uvicorn.run("redops_rag.api:app", host=args.host, port=args.port)
        return
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
