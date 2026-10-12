# Agent instructions

`snomed-widgets` provides interactive widgets and data adapters for clinical informatics work in reactive Python notebooks, starting with marimo. It is a presentation and analysis layer: it renders clinical codes as inspectable references, edits terminology expressions, reviews codelists, and shows the effect of a concept set on a dataset. It is **not** a terminology engine, not clinical decision support, and not a patient data store. Terminology semantics belong to the backend, never to this repo.

## Read first

- [README.md](README.md) - purpose, scope, and what this explicitly is not.
- [spec/roadmap.md](spec/roadmap.md) - the design decisions, the three de-risking spikes, and the planned slices. Read this before writing any code; most architectural questions are already answered there.
- [SAFETY.md](SAFETY.md) - clinical safety posture and the medical-device applicability record.
- [house-style/AGENTS.md](https://github.com/pacharanero/house-style/blob/main/AGENTS.md) - cross-repo standards for CI, licensing, commits, dependencies, and UI.
- [`sct`'s `spec/marimo-snomed-notebook.md`](https://github.com/pacharanero/sct/blob/main/spec/marimo-snomed-notebook.md) - the upstream spec this repo was split out of. It defines what `sct` will and will not do in support of this work, and its constraints on honesty, provenance, and isolation apply here too.

## Core invariants

- **Terminology semantics live in the backend, not here.** If a query cannot be expressed through the backend's public API, add a method upstream. Never write raw terminology SQL, and never reimplement expression parsing or expansion locally. This is the rule that stops the repo becoming a second, worse terminology engine.
- **Backends are pluggable and resolved at runtime.** No module outside the adapter layer imports `sct_py` or any other backend directly. A widget talks to an adapter interface, so the same component works against a local database or a remote FHIR server.
- **Expansion is explicit; everything downstream is reactive.** Editing an expression marks results stale and requires an explicit run, because expansion fully materialises a set and is expensive. Once materialised, set-membership tests over a dataframe are vectorised and recompute automatically. Never trigger expansion on a keystroke.
- **Never silently broaden or narrow a set.** An unsupported construct, a truncated result, or a missing capability is a visible error or an explicit disclosure. A limit is never presented as a complete result, and a count is never presented as a measured effect on patients.
- **Inactive concepts are unmistakable.** Rendering a plausible term for a retired code without saying it is retired is the most likely way this tool misleads someone. Show the status and the forwarding target.
- **Data crosses boundaries as data.** Widget values are escaped attribute data and event payloads, never values interpolated into JavaScript source, `innerHTML`, or inline handlers. Terminology terms are untrusted input and must render literally.
- **No licensed content in the repo.** No terminology releases, no real patient data, no derived databases, no sample outputs containing licensed terms. Fixtures are synthetic.
- **SPDX headers on every source file** (`# SPDX-FileCopyrightText: 2026 Marcus Baw and Baw Medical Ltd`, `# SPDX-License-Identifier: AGPL-3.0-or-later`). Files that cannot carry one are covered by `REUSE.toml`. `reuse lint` is enforced in CI.

## Validation

Run before every commit:

```sh
s/lint          # ruff check . && ruff format --check .
s/test          # pytest
reuse lint
```

CI runs the same three.

## Git workflow

Small repo, one contributor: commit and push each validated coherent parcel direct to `main`. Use a branch and PR for anything large, risky, or worth reviewing as a unit. Conventional commits (`feat(widgets):`, `fix(adapter):`, `docs:`, `chore(deps):`, `ci:`, `test:`).

## Approval required

Ask before publishing to PyPI, creating or changing the GitHub remote, force-pushing, deleting branches, changing secrets, or any other externally visible action.

## Do not touch casually

- `spec/roadmap.md` records decisions with reasons. Changing a decision means updating the reason, not just the text.
- `SAFETY.md`'s medical-device record has explicit reassessment triggers. If a change hits one of them, say so rather than quietly editing the conclusion.
