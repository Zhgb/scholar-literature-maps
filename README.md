# Scholar Literature Maps

Scholar Literature Maps is a Codex agent skill for academic literature discovery. It is designed for literature reviews, paper screening, seed-paper tracing, and researcher discovery in scientific research workflows.

Academic literature searches often fail in two ways: non-English prompts can pull the wrong language or weakly translated results, and broad academic search tools often return papers that share keywords but miss the real research object. This skill helps an agent turn a research question into an English-first, scope-aware literature map instead of a raw search list.

## What This Skill Does

- Converts Chinese or other non-English research questions into field-standard English academic search concepts.
- Builds grouped literature maps for a topic, with short explanations of why each paper is relevant.
- Searches narrowly first, then performs controlled adjacent-core expansion so important nearby papers are not missed.
- Traces related papers around a seed paper, including earlier foundations, same-author work, later citing papers, and close neighboring studies.
- Identifies high-impact and recently active scholars in a research area, with representative papers and relevance notes.
- Classifies candidate papers as core, adjacent-core, boundary, or excluded to avoid padding narrow topics with weakly related papers.

## Typical Uses

- Find the most relevant English papers for a research topic.
- Understand how one important paper fits into a broader literature.
- Discover authoritative and currently active researchers in a field.
- Improve noisy Scholar Labs or academic-search results through explicit scope locking and reranking.

## Main Files

- `SKILL.md`: Main workflow and usage instructions.
- `references/scoring-rubric.md`: Internal guidance for scope locking, reranking, and boundary classification.
- `scripts/rerank_scholar_candidates.py`: Optional helper script for structured candidate reranking.
- `agents/openai.yaml`: UI metadata for Codex skill display.
