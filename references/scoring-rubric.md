# Scoring Rubric

Use this rubric to derive `must_have`, `should_have`, and `exclude` before reranking.

## Scope Lock

Before scoring candidates, define the scope lock:

- required outcome
- required sample matrix, organism, population, system, or dataset
- required method or evidence type
- explicit exclusions

For narrow tasks, score strict-core fit first. Then allow one controlled adjacent-core axis when it directly supports the user's real research task. A paper that misses the required outcome or matrix by more than one axis should be boundary or excluded even if it shares many keywords.

## Must-Have Concepts

Put a concept in `must_have` only if the paper is off-target without it.

Typical must-have categories:

- main object of study
- target organism, material, population, or disease
- main exposure, intervention, or phenomenon
- primary outcome if the request is narrow
- required sample matrix or dataset when the user explicitly restricts it
- required method or model type when the user asks for modelling or prediction papers

Good example:

- query: `environmental risks of veterinary antibiotic residues in manure`
- `must_have`: `veterinary antibiotic residues`, `manure` or `animal feces`

Bad example:

- putting `environmental` in `must_have` when many relevant papers say `ecological`, `soil`, `water`, or `fate` instead

## Should-Have Concepts

Use `should_have` for terms that improve ranking without becoming hard filters.

Examples:

- mechanistic terms
- common synonyms
- target outcomes
- common methods
- field-specific phrases such as `occurrence`, `fate`, `transport`, `ecotoxicity`

## Exclude Concepts

Use `exclude` for frequent distractors.

Examples:

- human clinical topics when the user asked for veterinary or environmental literature
- food safety residue testing when the user asked for environmental fate
- unrelated antibiotics or unrelated sample matrices

## Ranking Logic

Apply these principles when reading the script output:

1. Required outcome and matrix fit outrank title keyword overlap.
2. A title hit is useful, but abstract, dataset, methods, and sample source can reveal relevant papers with broad titles.
3. Missing a must-have concept is usually disqualifying.
4. A paper with many loose overlaps should still rank below a paper that matches the exact study object.
5. English is preferred by default, but do not discard a highly relevant non-English paper if the English pool is weak.
6. Use year and venue only as secondary tie-breakers unless the user explicitly asks for recent literature or a certain evidence type.

## Boundary Classification

Classify candidates before writing the final answer:

- `core`: matches the required outcome, matrix, and method or evidence role
- `adjacent-core`: misses the strict scope by one controlled axis but directly supports the research task, such as use-derived emissions/fate/risk for a use-estimation topic, statistical modelling for a machine-learning topic, or a parent system for a narrow matrix topic when not explicitly excluded
- `boundary`: useful but misses more than one requirement, is review-only, uses a distant matrix, or is mainly background
- `exclude`: misses a must-have concept or falls into an explicit exclusion

Do not pad a strict narrow-topic result with weak boundary papers. Return fewer core papers when needed, and list adjacent-core papers separately when they help explain methods, datasets, downstream pathways, or field context.

## Output Style

Use the script output internally. Final answers should be grouped by research role or lineage role, not presented as a raw ranked list unless the user asks for ranking.

Explain the final selection in plain language:

- `Early foundational study: Direct match on antibiotic residues + manure in both title and abstract; focuses on environmental fate rather than food testing.`
- `Adjacent methods paper: Good manure and risk match, but antibiotics are broader and the study is partly about wastewater, so it is useful mainly for comparison.`

Call out why near-misses were rejected when that helps the user trust the filtering.
