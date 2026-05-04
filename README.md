# Scholar Literature Maps

Scholar Literature Maps is a Codex agent skill for academic literature discovery. It is designed for literature reviews, paper screening, seed-paper tracing, and researcher discovery in scientific research workflows.

Academic literature searches often fail in two ways: non-English prompts can pull the wrong language or weakly translated results, and broad academic search tools often return papers that share keywords but miss the real research object. This skill helps an agent turn a research question into an English-first, scope-aware literature map instead of a raw search list.

## What This Skill Does

- Converts Chinese or other non-English research questions into field-standard English academic search concepts.
- Builds grouped literature maps for a topic, with short explanations of why each paper is relevant.
- Traces related papers around a seed paper, including earlier foundations, same-author work, later citing papers, and close neighboring studies.
- Identifies high-impact and recently active scholars in a research area, with representative papers and relevance notes.


## Quick Install

This skill can be installed directly from GitHub with Codex's skill installer. The current repository is:

```text
https://github.com/Zhgb/scholar-literature-maps
```

Because this repository root is the skill folder itself, ask Codex:

```text
Use $skill-installer to install the Codex skill from https://github.com/Zhgb/scholar-literature-maps. The repository root is the skill folder; install path "." with name "scholar-literature-maps".
```

Or run the installer script manually:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Zhgb/scholar-literature-maps \
  --path . \
  --name scholar-literature-maps
```

After installation, restart Codex so it can pick up the new skill.

## Typical Uses

- Find the most relevant English papers for a research topic.
- Understand how one important paper fits into a broader literature.
- Discover authoritative and currently active researchers in a field.


## Main Files

- `SKILL.md`: Main workflow and usage instructions.
- `references/scoring-rubric.md`: Internal guidance for scope locking, reranking, and boundary classification.
- `scripts/rerank_scholar_candidates.py`: Optional helper script for structured candidate reranking.
- `agents/openai.yaml`: UI metadata for Codex skill display.
