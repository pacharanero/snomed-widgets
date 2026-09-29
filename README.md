# clinical-widgets

Interactive widgets and data adapters for clinical informatics work in reactive Python notebooks.

> **Status: pre-alpha scaffold.** Nothing here works yet. The design is recorded in [`spec/roadmap.md`](spec/roadmap.md); the code is three spikes away from a first useful slice. Do not use this for anything that touches patient care.

## What is this?

A toolkit for building and reviewing clinical concept sets, codelists, and row-level rules against a dataset, inside a [marimo](https://marimo.io) notebook. The intended loop is: write a terminology expression, see the concept set it produces, see what it does to your data, inspect the rows where it changed its mind.

The pieces are meant to be small and composable:

- **Concept widgets** - render any clinical code as an inspectable reference rather than a bare number. Hover or focus gives the fully specified name, preferred term, active status, and immediate hierarchy neighbours.
- **Expression editing** - a real editor for terminology query languages, with diagnostics, rather than a plain text box.
- **Codelist review** - hierarchy tree with include/exclude at branch level, and the resulting set exported back as an expression.
- **Dataset adapters** - vectorised set-membership over a dataframe, so the effect of a change to a concept set is visible immediately.
- **Adjudication** - label a slice of rows by hand and get an honest local metric with an interval, instead of guessing.

Terminology backends are pluggable. The first is [`sct`](https://github.com/pacharanero/sct) via its `sct-py` bindings, which makes lookups a local SQLite read with no network. A FHIR terminology adapter is planned so the widgets work against Ontoserver, Snowstorm, or any conformant server without installing `sct`.

SNOMED CT is the first terminology because it is the hardest. The design is deliberately not SNOMED-specific: openEHR, FHIR, LOINC, ICD, and dm+d are all in intended scope.

## What is it not?

- **Not clinical decision support**, and not diagnostic advice. It helps you design and inspect concept sets. It does not tell you what they mean clinically.
- **Not a terminology server**, and not a terminology authoring environment. It queries releases; it does not edit them.
- **Not a patient data store.** It reads a dataset you already have and holds nothing.
- **Not a replacement for `sct`'s own interfaces.** `sct` owns terminology semantics. This repo owns presentation. If a query cannot be expressed through the SDK, the fix belongs upstream in `sct`, not in a local SQL string here.
- **Not a distribution channel for licensed terminology content.** You supply your own release.

## Who is it for?

Clinical informaticians, terminologists, researchers, and analysts who already have a licensed terminology release locally and a dataset to test against, and who want a human-reviewable loop rather than a pile of one-off scripts. It assumes comfort with Python and a working knowledge of the terminology you are querying.

## Install

Not yet installable. When it is:

```sh
pip install clinical-widgets
```

Development setup:

```sh
git clone https://github.com/pacharanero/clinical-widgets
cd clinical-widgets
pip install -e '.[dev]'
```

A terminology backend is a separate install and a separate licence. For the local `sct` path you need `pip install sct-py` and a database you built yourself from a release you are licensed to use.

## Test

```sh
s/test          # pytest
s/lint          # ruff check and format --check
```

## Contribute

Early days, and the design is still moving. Read [`spec/roadmap.md`](spec/roadmap.md) and [`agent-instructions.md`](agent-instructions.md) first. Issues and discussion are more useful than pull requests at this stage.

## Licence

Code is **AGPL-3.0-or-later** (see [`LICENSE`](LICENSE)). This is not a free choice: the first terminology backend links `sct-py`, which is AGPL, so the combined work is too.

Written content and documentation are **CC-BY-SA-4.0**.

Third-party provenance: terminology content is not distributed with this repo and remains the property of its publishers under their own licences. SNOMED CT is copyright SNOMED International and requires an affiliate licence in most territories. Any adopted upstream component keeps its own licence and attribution, recorded in-file.
