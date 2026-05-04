---
name: scholar-literature-maps
description: Build scope-locked, English-first academic literature maps, seed-paper lineage traces, and researcher discovery outputs from Scholar Labs or similar academic-search tools. Use when Codex needs to turn Chinese or any non-English research topic into field-standard English natural-language search prompts, find and group highly relevant English papers with relevance explanations, search narrow core papers first then controlled adjacent-core papers, avoid padding narrow topics with weak boundary papers, trace earlier/later papers around a seed paper, or identify high-impact and recently active scholars in a research area.
---

# Scholar Literature Maps

Use this skill to turn a research question into a readable literature map or research lineage. Default to English-first retrieval unless the user explicitly asks for Chinese or another language's literature.

Prioritize Scholar Labs or similar natural-language academic search as the discovery entry point. Use other sources as methodology, not as a separate user-facing feature: Semantic Scholar, OpenAlex, Crossref, PubMed, arXiv, publishers, and author pages can supplement references, citations, DOI metadata, author trajectories, recency, and publication evidence.

## User-Facing Modes

Choose the mode from the user's request. If multiple modes fit, combine them without exposing internal search mechanics.

### Topic literature map

Use when the user gives a topic, question, mechanism, population, method, disease, material, organism, or field and wants papers.

Return about 20-30 highly relevant English papers unless the user requests a different number. Group papers by research role, not by search source.

Common groups:

- field entry points or core reviews
- early foundational studies
- key empirical studies
- methods, datasets, models, or measurement papers
- recent representative advances
- debates, limitations, negative findings, or alternative explanations

For each paper, include title, year, venue when available, and one or two sentences explaining why it is relevant. Mention caveats such as review-only, different population, adjacent method, broader object, or partial topic overlap.

Do not show explicit search prompts, query strings, numerical scores, or score breakdowns unless the user asks for them.

### Seed paper lineage trace

Use when the user names, links, uploads, or describes a specific paper and wants related, earlier, or follow-up work.

First identify the seed paper's title, year, DOI if available, authors, venue, abstract, references, citing papers, and author publication history. Then trace the paper's position in the field.

Useful groups:

- the seed paper and its immediate contribution
- earlier papers cited by the seed paper
- field precursors that predate the seed paper
- earlier related work by the same author or author group
- later papers that cite, test, extend, criticize, or apply the seed paper
- close neighboring papers with similar object, method, or conclusion

Prefer papers that explain the seed paper's intellectual ancestry or later influence over papers that merely share keywords. For each selected paper, explain the connection to the seed paper.

### Researcher discovery

Use when the user asks who works on a topic, who is influential, or who is recently active in a field.

Return high-impact scholars and recently active research experts. Consider impact and activity separately:

- high-impact: recurring author on foundational papers, widely cited reviews, influential datasets/methods, or central studies
- recently active: relevant papers in the last three to five years, continuing grants/projects, preprints, conference activity, or recent collaborations

For each scholar, include name, affiliation when available, relevant subtopic, representative papers, and a short reason they matter for the user's topic. Avoid ranking people only by citation count or h-index; topic fit and recent relevance matter.

## Workflow

### 1. Lock the scope before searching

Extract a compact internal scope lock before searching:

- `outcome`: abundance, concentration, occurrence, risk, source, host, mechanism, or another target
- `matrix`: population, organism, material, disease, dataset, environment, sample type, or system
- `method`: machine learning, statistical modelling, experimental design, review, dataset, or other evidence type
- `exclusions`: paper types, matrices, methods, outcomes, languages, years, or adjacent topics the user does not want
- `mode`: topic literature map, seed-paper lineage trace, researcher discovery, or a combination

For narrow tasks, prioritize precision first, then run a controlled adjacent expansion. Do not force 20-30 papers when the scope lock and adjacent-core pass leave only a few genuinely relevant studies. State the inclusion boundary in the final answer when it affects what is included or excluded.

### 2. Normalize and expand English concepts

Translate Chinese or any non-English user wording into field-standard English terminology. Use canonical English research terms before searching, and keep the user's original language only as a fallback aid or for final explanation.

Build internal term sets:

- `must_have`: concepts that must appear in a relevant paper
- `should_have`: concepts that strengthen relevance but are not required
- `exclude`: adjacent topics that often cause false positives

Expand concepts by meaning, not only literal title words. For example:

- `ARGs`: `antibiotic resistance genes`, `antimicrobial resistance genes`, `AMR genes`, `resistome`
- `prediction`: `predict`, `prediction`, `modelling`, `modeling`, `modelling study`, `statistical model`, `machine learning`, `random forest`, `LASSO`, `XGBoost`, `deep learning`
- `wastewater`: `wastewater`, `sewage`, `urban sewage`, `hospital wastewater`, `influent`, `effluent`

Do not reject a paper because the title lacks the user's exact words. Screen title, abstract, dataset, sample source, model target, and methods.

### 3. Search narrow first, then controlled adjacent-core

Prepare three to five English natural-language prompts for Scholar Labs or similar tools:

- one direct high-precision prompt matching the strict scope lock
- one synonym-expanded prompt using alternate names for the outcome and matrix
- one method-expanded prompt using terms such as `modelling study`, `random forest`, or other method variants
- one controlled adjacent-core prompt that shifts one axis outward while preserving the user's real research intent
- one prompt aimed at reviews, foundations, datasets, early literature, recent advances, or active researchers when needed

Use short research-style prompts rather than literal translation. The prompts are internal working material; do not include them in the final answer unless requested.

Start with high-precision retrieval and identify strict-core papers first. Then broaden exactly one axis at a time to find adjacent-core papers that a researcher would expect in the literature map.

Common adjacent-core moves:

- broaden outcome from `use` to `use-derived emissions`, `fate`, `exposure`, or `risk inventory`
- broaden method from `machine learning` to `statistical modelling`, `mechanistic modelling`, or `multimedia modelling`
- broaden matrix from a specific sample type to a parent system only if the user did not explicitly exclude it
- broaden object from one drug class or organism to the parent class only if it supplies methods, datasets, or early context

Do not broaden along an axis the user explicitly excluded. If an adjacent-core pass only returns weak boundary papers, stop broadening.

### 4. Pool, verify, and classify candidates

Combine candidates across prompts and supplementary sources before judging relevance.

- deduplicate by DOI, exact title, or near-identical title
- keep title, authors, year, venue, DOI, abstract, language, source, and source role when available
- keep reference and citation links when tracing a seed paper
- keep author identifiers when discovering scholars
- discard records with no usable title and no abstract or metadata evidence

Classify each candidate as `core`, `adjacent-core`, `boundary`, or `exclude` against the scope lock:

- `core`: matches the required outcome, matrix, and method or evidence role
- `adjacent-core`: misses the strict scope by one controlled axis but directly supports the research task, such as use-derived emissions/fate/risk for a use-estimation topic
- `boundary`: useful but misses more than one requirement, is review-only, uses a distant matrix, or is mainly background
- `exclude`: misses a must-have concept or falls into an explicit exclusion

Use supplementary sources to verify metadata and relationships:

- Semantic Scholar or OpenAlex for citations, references, related papers, and author publication trails
- Crossref for DOI and publication metadata
- PubMed, arXiv, publishers, or institutional pages for domain-specific records and abstracts
- author profiles or lab pages only as supporting evidence for activity and affiliation

Do not invent citation relationships, author trajectories, or publication details when sources are incomplete. Mark uncertain links as tentative.

### 5. Run a limited seed-based recall pass

After initial screening, choose two to four strong seed papers. For each seed, check only the highest-value neighborhood:

- key references that supply data, methods, or early concepts
- citing papers that reuse the dataset, model target, or modelling frame
- same-author papers that predate or extend the seed
- related papers identified by Scholar Labs, Semantic Scholar, OpenAlex, or publisher pages

Keep at most five to eight new candidates per seed before screening them against the scope lock. This pass is for recall repair, not unlimited citation chasing.

### 6. Run a final boundary-check query

Before finalizing a narrow or technical literature map, run one short recall check for papers that may not contain the obvious title keywords.

Use alternate wording for the weak axis. Examples:

- replace `machine learning` with `modelling study`, `statistical modelling`, or the specific model family
- replace `ARGs` with `AMR genes`, `antimicrobial resistance`, or `resistome`
- replace `wastewater treatment plant` with `sewage`, `urban sewage`, `influent`, `effluent`, or the requested sample matrix
- combine a seed-paper title with `cited by`, `associated with`, `predictors`, or a known dataset name

Include one controlled adjacent-core wording in this check when the topic has obvious downstream or upstream papers, such as `use-derived emissions`, `environmental fate`, `risk assessment`, `exposure inventory`, `source inventory`, `policy scenario`, or `dataset reuse`.

Do not use this step to expand beyond the user's exclusions.

### 7. Rerank explicitly, then hide the machinery

Judge each candidate against this order of importance:

1. match to the required outcome
2. match to the target matrix, population, material, organism, disease, dataset, or system
3. match to the required method, study design, mechanism, or claim
4. title and abstract evidence for `must_have`
5. fit to the requested mode: foundational, recent, empirical, methodological, lineage, or scholar-related
6. absence of `exclude` concepts
7. language preference, with English favored by default

Treat a paper as weak even if it has many overlapping words when it misses the actual study object, outcome, mechanism, or method.

When the result set is long or noisy, use `scripts/rerank_scholar_candidates.py` with a structured candidate list. Read [references/scoring-rubric.md](references/scoring-rubric.md) before tuning the term sets. Use score output internally to support selection, grouping, and caveat writing; do not expose numerical scores in the final answer unless requested.

### 8. Stop and return grouped results

Stop broadening when two or three consecutive searches add only duplicates, weak boundary papers, or excluded papers.

Report grouped results after reranking and verification, not raw search order. For topic maps, return 20-30 papers only when enough strong candidates exist. For strict narrow topics, return fewer core papers and include adjacent-core papers as a separate group when they help explain methods, datasets, downstream emissions/fate/risk, or field context. Do not mix adjacent-core papers into the strict-core group.

For seed-paper traces, prioritize intellectual lineage and later influence over volume. Include enough papers to clarify the research path, usually 10-25 depending on evidence.

For scholar discovery, separate high-impact scholars from recently active experts when useful. Include representative papers and reasons, not just names.

Always explain why each paper or scholar matters to the user's topic. Include caveats where relevance is partial, and call out excluded near-misses when that helps clarify the boundary.

## Script Input Contract

Use `scripts/rerank_scholar_candidates.py` when you have structured candidates. Provide a JSON file with this shape:

```json
{
  "query": "English-normalized research question",
  "must_have": ["antibiotic residues", ["animal feces", "manure"]],
  "should_have": ["environmental risk", "ecotoxicity"],
  "exclude": ["human clinical trial"],
  "prefer_english": true,
  "candidates": [
    {
      "id": "paper-1",
      "title": "Paper title",
      "abstract": "Abstract text",
      "normalized_title": "Optional English-normalized title for non-English papers",
      "normalized_abstract": "Optional English-normalized abstract for non-English papers",
      "year": 2024,
      "venue": "Journal name",
      "language": "en"
    }
  ]
}
```

A term can be:

- a string: one concept with one surface form
- a string array: one concept with interchangeable synonyms; any match satisfies that concept

If a candidate is not in English but you still want a fair comparison, add `normalized_title` and `normalized_abstract` in English. The script matches against those normalized fields first and still applies the language preference separately.

Run:

```powershell
python scripts/rerank_scholar_candidates.py input.json --top 30
```

The script prints ranked JSON with score breakdowns and reasons. Convert those reasons into plain-language relevance explanations and grouped output.
