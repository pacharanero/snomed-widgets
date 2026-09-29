# Roadmap and design decisions

Status: pre-implementation. No code beyond the package scaffold. Origin: lessons from a private clinical dataset workbench built in September 2026, where terminology expressions had to be authored, expanded, and tested against 280k rows of episode data with no local ground truth.

This file records decisions with their reasons. Changing a decision means updating the reason, not just the text.

## Why this repo exists separately

The upstream spec at [`sct`'s `spec/marimo-snomed-notebook.md`](https://github.com/pacharanero/sct/blob/main/spec/marimo-snomed-notebook.md) sets two boundaries that this work cannot satisfy inside `sct`: no competition data, solver, or scoring logic belongs in `sct`, and `sct`'s planned GUI (`R38`) must not acquire a notebook dependency or publish a component library ahead of its own gate. A dataset-facing analysis surface with scoring and user-authored rules therefore needs its own home.

The separation is cheap because the coupling is a published artefact, not a source path: `pip install sct-py`, a versioned PyPI package with abi3 wheels. This is the opposite of `sct-lens`, which is correctly a sibling project inside `sct` because it links `sct-rs` by path and must move in lockstep.

What this buys: an independent dependency graph (npm, Monaco, marimo, and a dataframe engine touch nothing in `sct`'s Rust build), an independent release cadence, and a clean trust boundary for the user-authored-code question below.

## Naming

`clinical-widgets`, deliberately dull and descriptive.

Not named after marimo, because the widgets are `anywidget`-based and therefore host-portable across marimo, Jupyter, Shiny, and Panel. Naming the current host as if it were the product would contradict a documented future direction.

Not named after terminology, because the intended scope includes openEHR, which is an information model rather than a terminology. SNOMED CT is the first target because it is the hardest, not because it is the boundary. FHIR, LOINC, ICD, and dm+d are all in scope.

Accepted cost: "widgets" undersells the adapter, dataset, and scoring layers that sit behind the visual components.

## Licence

AGPL-3.0-or-later. Not a free choice: the first terminology backend links AGPL `sct-py`, so the combined work is AGPL. It absorbs Apache-2.0 and GPL-3.0 components inbound, which covers the adoptable prior art below.

## Architecture

```text
user / agent <-> notebook host (marimo first)
                       |
                 widgets (anywidget, shadow DOM)
                       |
              terminology adapter interface
                 /            |           \
          sct-py         FHIR R4        future
       (local, offline)  ($expand,      (WASM, other
                          $lookup)       code systems)

           dataset layer (dataframe, vectorised membership)
```

### The adapter boundary is the load-bearing decision

Terminology semantics live in the backend. If a query cannot be expressed through the backend's public API, the fix is a method added upstream, not SQL in this repo. Without this rule the project becomes a second, worse terminology engine, which is exactly the fragmentation `sct` was built to avoid.

The FHIR adapter is what makes the widgets useful to someone who never installs `sct`, and it confines the AGPL obligation to users who choose the `sct` path.

### Expansion is explicit; everything downstream is reactive

This is the correction that makes "live preview" honest. Expression expansion fully materialises a concept set and is expensive, so a keystroke must not trigger it: editing marks results stale and requires an explicit run. Once the set exists, testing membership over a dataframe column is a hash probe, so prevalence, diffs, and strata recompute automatically on every other control.

The staleness boundary is part of the interface, not a hidden cost. The result is marimo's spreadsheet feel without pretending expansion is free.

### Two-speed rule evaluation

| Operation | Order of magnitude, ~280k rows | Reactive? |
|---|---|---|
| Vectorised membership against a materialised set | milliseconds | yes |
| Dataframe expression over numeric columns | tens of milliseconds | yes |
| Arbitrary per-row Python | seconds | no |

The interface must show which mode it is in. A **preview** mode runs an arbitrary predicate over a stratified sample; a **full** mode runs the whole dataset on demand. A rule should be able to declare itself vectorisable, and promoting an arbitrary predicate to a vectorised one should be easy and visible.

### User-authored and AI-authored code

The upstream spec puts arbitrary predicates outside its first slice, and is right that "a notebook cell or run button is not isolation". This repo takes a different documented stance, because it is a single-user local analysis tool rather than a distributed product: arbitrary predicates are in scope, and the first implementation may run in-process.

The obligation that comes with that: design the rule interface so a least-privilege subprocess path (explicit argv, staged read-only inputs, scrubbed environment, no network, resource limits, aggregate-only output) is available from the start, even before it is implemented. The risk profile changes the moment anyone else runs this or real patient data is involved, and retrofitting isolation into a rule interface that assumed in-process execution is a rewrite.

## Open questions to resolve by spike, not by argument

Each is roughly an afternoon, and each can reshape the design. Do them before building any interface.

### Spike A - the performance premise

One notebook: open a terminology session in-process, scan a large dataset lazily, expand one expression, test membership as a vectorised column operation, report prevalence. No interface at all.

Measures whether the edit-to-number loop is fast enough to feel direct. Also gives a direct comparison against the existing row-at-a-time script, so the result is useful whatever happens next.

### Spike B - can a concept reference live inside a dataframe view?

Unknown and untested: whether the notebook host's table component will render a custom element in a cell or escape it to text.

This determines the information architecture. If it renders, inspectable codes are available everywhere data is displayed. If it does not, they only work in purpose-built views, and the codelist and adjudication surfaces become the place they live.

### Spike C - Monaco inside a widget bundle

`@aehrc/ecl-editor` is a Monaco-based web component, and Monaco is demanding about web workers and bundling. `anywidget` wants an ESM bundle.

Fallback if it fights: CodeMirror with a hand-written grammar, revisiting Monaco later. The diagnostics are the prize, not the editor chrome.

## Delivery slices

Identifiers are stable and must not be renumbered.

- **CW-1 - First vertical slice.** Expression in, concept set out, prevalence over a dataset, every code in the result rendered as an inspectable reference. One screen. Exercises all three spikes together. Explicitly excludes the codelist tree, adjudication, and any metric.
- **CW-2 - Concept reference component.** The keystone, built once as a shadow-DOM custom element over the adapter interface: fully specified name, preferred term, active status, immediate parents and children on expand. Inactive status and forwarding target must be unmistakable, since a plausible term shown for a retired code is the most likely way this tool misleads someone.
- **CW-3 - Codelist review.** Hierarchy tree with include/exclude at branch level, set exported back as a compact expression. Interaction model informed by OpenCodelists.
- **CW-4 - Adjudication and honest metrics.** Show disagreement between two rule versions, capture a per-row verdict, accumulate a local labelled slice, report a metric with an interval. This is the slice that closes the feedback loop, and the reason scoring cannot live in `sct`.
- **CW-5 - Cross-edition binding.** Make the terminology release a visible per-rule property rather than an ambient environment variable, and surface the routing that decides which release applies to a record.
- **CW-6 - Second adapter.** A FHIR R4 adapter, which is the proof that the boundary in CW-2 is real.

## Known upstream gaps in `sct`

Fix these in `sct`, not here.

- **No `parents` method.** The Python surface exposes `children`, `ancestors` (transitive), `descendants`, and `subsumes`, but not immediate parents, which CW-2 needs. Small addition.
- **Diagnostics across the Python boundary.** Parser and evaluator errors, and annotation warnings, need to arrive as structured values rather than process stderr, so a widget can show an actionable message.
- **Bulk lookup already exists** (`concepts(ids)`), which is what makes rendering thousands of references viable: resolve the distinct codes once, then every reference is a cache hit.

## Prior art

Read the original before borrowing ideas, code, or terminology content. Licences verified 2026-09-29.

- [`aehrc/ecl-lsp`](https://github.com/aehrc/ecl-lsp) - Apache-2.0, actively maintained. Publishes `@aehrc/ecl-editor` to npm: a Monaco web component for SNOMED CT ECL 2.2 with diagnostics, completion, hover, and formatting, backed by a language server. Adopt with attribution rather than rebuilding.
- [OpenCodelists](https://github.com/opensafely-core/opencodelists) - GPL, Bennett Institute. The most mature open codelist-building interaction model: search, hierarchy tree, include/exclude at branch level. Study the interaction; the Django stack is not the target here.
- [OHDSI ATLAS](https://github.com/OHDSI/Atlas) - Apache-2.0. Conceptually closest existing tool: build a concept set, get live counts against a real dataset. Counts, not metrics, and a Java/OMOP stack.
- [ECLed](https://link.springer.com/article/10.1186/s13326-025-00344-3) - 2026 paper on ECL authoring with live results and a parent/child viewer. Note its small usability sample and untested scalability; the Angular/Spring architecture is not a model to copy.
- [`wardle/hermes`](https://github.com/wardle/hermes) and [`wardle/codelists`](https://github.com/wardle/codelists) - Clojure, ECL 2.2 plus ICD-10 and ATC composition. Prior art for composing codelists across code systems.
- Ontoserver and Shrimp are not open source and are therefore out of scope as components, though useful as comparison points.

The relevant specification is always the semantic authority; editor and browser behaviour is not.
