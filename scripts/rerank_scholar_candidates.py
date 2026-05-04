#!/usr/bin/env python3
"""Deterministically rerank Scholar Labs candidates from structured JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "report",
    "reports",
    "study",
    "the",
    "to",
    "what",
    "when",
    "with",
}

CJK_RE = re.compile(r"[\u3400-\u9fff]")
TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rerank Scholar Labs candidates with explicit topic-fit scoring."
    )
    parser.add_argument("input_json", type=Path, help="Path to the input JSON file.")
    parser.add_argument("--top", type=int, default=5, help="Number of ranked papers to emit.")
    return parser.parse_args()


def normalize_text(value: str) -> str:
    return " ".join(value.lower().split())


def tokenize(value: str) -> set[str]:
    return {
        token
        for token in TOKEN_RE.findall(value.lower())
        if token not in STOPWORDS and len(token) > 1
    }


def estimate_language(candidate: dict) -> str:
    declared = str(candidate.get("language") or "").strip().lower()
    if declared:
        return declared

    joined = f"{candidate.get('title', '')} {candidate.get('abstract', '')}"
    if not joined.strip():
        return "unknown"
    if CJK_RE.search(joined):
        cjk_count = len(CJK_RE.findall(joined))
        ratio = cjk_count / max(len(joined), 1)
        if ratio > 0.03:
            return "zh"
    ascii_letters = sum(ch.isascii() and ch.isalpha() for ch in joined)
    if ascii_letters / max(len(joined), 1) > 0.45:
        return "en"
    return "unknown"


def normalize_term_spec(value: object) -> list[list[str]]:
    if value is None:
        return []
    normalized: list[list[str]] = []
    if not isinstance(value, list):
        raise ValueError("Term lists must be arrays.")
    for item in value:
        if isinstance(item, str):
            normalized.append([item])
        elif isinstance(item, list) and item and all(isinstance(x, str) for x in item):
            normalized.append(list(item))
        else:
            raise ValueError("Each term must be a string or a non-empty string array.")
    return normalized


def group_match_terms(group: Iterable[str], text: str) -> list[str]:
    matches = []
    for term in group:
        if normalize_text(term) in text:
            matches.append(term)
    return matches


def overlap_score(query_tokens: set[str], title_tokens: set[str], abstract_tokens: set[str]) -> tuple[int, list[str]]:
    title_hits = sorted(query_tokens & title_tokens)
    abstract_hits = sorted((query_tokens & abstract_tokens) - set(title_hits))
    score = len(title_hits) * 3 + len(abstract_hits)
    reasons = []
    if title_hits:
        reasons.append(f"title overlaps query tokens: {', '.join(title_hits[:6])}")
    if abstract_hits:
        reasons.append(f"abstract overlaps query tokens: {', '.join(abstract_hits[:6])}")
    return score, reasons


def score_candidate(candidate: dict, payload: dict) -> dict:
    title = str(candidate.get("title") or "")
    abstract = str(candidate.get("abstract") or "")
    normalized_title = str(candidate.get("normalized_title") or title)
    normalized_abstract = str(candidate.get("normalized_abstract") or abstract)
    title_text = normalize_text(normalized_title)
    abstract_text = normalize_text(normalized_abstract)
    title_tokens = tokenize(normalized_title)
    abstract_tokens = tokenize(normalized_abstract)
    query_tokens = tokenize(str(payload.get("query") or ""))

    must_have = normalize_term_spec(payload.get("must_have", []))
    should_have = normalize_term_spec(payload.get("should_have", []))
    exclude = normalize_term_spec(payload.get("exclude", []))
    prefer_english = bool(payload.get("prefer_english", True))

    score = 0
    reasons: list[str] = []
    breakdown = {
        "must_have": 0,
        "should_have": 0,
        "exclude": 0,
        "query_overlap": 0,
        "language": 0,
    }

    missing_must = []
    for group in must_have:
        title_hits = group_match_terms(group, title_text)
        abstract_hits = group_match_terms(group, abstract_text)
        if title_hits:
            score += 24
            breakdown["must_have"] += 24
            reasons.append(f"must-have in title: {title_hits[0]}")
        elif abstract_hits:
            score += 12
            breakdown["must_have"] += 12
            reasons.append(f"must-have in abstract: {abstract_hits[0]}")
        else:
            score -= 28
            breakdown["must_have"] -= 28
            missing_must.append(group[0])

    if missing_must:
        reasons.append(f"missing must-have concepts: {', '.join(missing_must)}")

    for group in should_have:
        title_hits = group_match_terms(group, title_text)
        abstract_hits = group_match_terms(group, abstract_text)
        if title_hits:
            score += 10
            breakdown["should_have"] += 10
            reasons.append(f"should-have in title: {title_hits[0]}")
        elif abstract_hits:
            score += 4
            breakdown["should_have"] += 4
            reasons.append(f"should-have in abstract: {abstract_hits[0]}")

    for group in exclude:
        title_hits = group_match_terms(group, title_text)
        abstract_hits = group_match_terms(group, abstract_text)
        if title_hits:
            score -= 22
            breakdown["exclude"] -= 22
            reasons.append(f"exclude term in title: {title_hits[0]}")
        elif abstract_hits:
            score -= 10
            breakdown["exclude"] -= 10
            reasons.append(f"exclude term in abstract: {abstract_hits[0]}")

    overlap_points, overlap_reasons = overlap_score(query_tokens, title_tokens, abstract_tokens)
    score += overlap_points
    breakdown["query_overlap"] += overlap_points
    reasons.extend(overlap_reasons)

    language = estimate_language(candidate)
    if prefer_english:
        if language.startswith("en"):
            score += 8
            breakdown["language"] += 8
            reasons.append("preferred English candidate")
        elif language.startswith("zh"):
            score -= 8
            breakdown["language"] -= 8
            reasons.append("penalized non-English candidate")

    return {
        "id": candidate.get("id"),
        "title": title,
        "year": candidate.get("year"),
        "venue": candidate.get("venue"),
        "language": language,
        "score": score,
        "score_breakdown": breakdown,
        "reasons": reasons,
        "missing_must_have": missing_must,
        "candidate": candidate,
    }


def validate_payload(payload: dict) -> None:
    if not isinstance(payload, dict):
        raise ValueError("Input JSON must be an object.")
    if "candidates" not in payload or not isinstance(payload["candidates"], list):
        raise ValueError("Input JSON must contain a candidates array.")


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.input_json.read_text(encoding="utf-8-sig"))
        validate_payload(payload)
        ranked = [score_candidate(candidate, payload) for candidate in payload["candidates"]]
    except Exception as exc:  # pragma: no cover - CLI entry path
        print(f"error: {exc}", file=sys.stderr)
        return 1

    ranked.sort(
        key=lambda item: (
            item["score"],
            -len(item["missing_must_have"]),
            int(item.get("year") or 0),
        ),
        reverse=True,
    )

    output = {
        "query": payload.get("query"),
        "top_n": args.top,
        "ranked_candidates": ranked[: args.top],
    }
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
