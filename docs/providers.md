# Model providers and CLI tools

RedOps supports the providers configured in OpenCode through one stable interface. Hosted
providers use the OpenAI-compatible `/chat/completions` contract; the local `extractive`
provider requires no network or credentials.

Install the CLI adapters for all supported agent providers with:

```bash
redops install-cli all --dry-run
redops install-cli all
# Copilot/Windsurf commands are workspace files:
redops install-cli all --workspace /path/to/project
```

The installer writes only RedOps command/skill text. It does not write API keys, MCP
tokens, or provider configuration.

## Agent provider formats

The adapter follows each provider's native layout. Claude and OpenCode use Markdown
commands, ZCode and Cursor use the shared `.agents`/`.cursor` command directories,
Gemini receives TOML commands (`$ARGUMENTS` is translated to `{{args}}`), and Copilot
and Windsurf receive workspace prompt/workflow files. Codex, Amp, and Crush use the
model-invoked `redops-rag` skill because they do not expose a user-defined slash-command
directory. Skill command files are discovered automatically from `commands/` and
`.agents/commands/`; use `--skill-path` for an external skill repository.

List the registry without exposing credentials:

```bash
redops providers
redops providers --json
```

## Provider matrix

| Provider | Environment | Default model | OpenCode model selector | CLI/tool path |
|---|---|---|---|---|
| Local extractive | none | n/a | n/a | `redops query --no-generate` |
| OpenAI | `OPENAI_API_KEY` | `gpt-4.1-mini` | `openai/gpt-4.1-mini` | `opencode --model openai/gpt-4.1-mini` |
| Z.ai | `ZAI_API_KEY` | `glm-5.3` | `zai/glm-5.3` | `opencode --model zai/glm-5.3` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-v4-pro` | `deepseek/deepseek-v4-pro` | `opencode --model deepseek/deepseek-v4-pro` |
| OrcaRouter | `ORCAROUTER_API_KEY` plus `REDOPS_ORCAROUTER_BASE_URL` | `orcarouter/free` | `orcarouter/free` | `opencode --model orcarouter/free` |

Select a provider in RedOps:

```bash
export REDOPS_LLM_PROVIDER=zai
export ZAI_API_KEY='...'
redops query "ringkas indikator CSRF" 
```

`REDOPS_API_KEY`, `REDOPS_API_BASE_URL`, and `REDOPS_LLM_MODEL` override the provider
defaults. Embeddings remain local hashing by default. To use a compatible embedding API,
set `REDOPS_EMBEDDING_PROVIDER`, `REDOPS_EMBEDDING_MODEL`, and optionally the separate
embedding key/base URL, then rebuild with `redops ingest --force`.

The CLI tool rows are launch recipes only; RedOps does not shell out to OpenCode or store
provider credentials. Never commit `.env` or API keys.
