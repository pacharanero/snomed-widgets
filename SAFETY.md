# Clinical safety

Status: **pre-alpha scaffold, not in use.** No release, no users, no deployment. This file exists because the medical-device applicability record is required at project inception, and because recording the safety posture before there is code is cheaper than retrofitting it.

This is not a completed safety case and does not replace a Clinical Safety Officer or a DCB0129 process. See [house-style/clinical-safety.md](https://github.com/pacharanero/house-style/blob/main/clinical-safety.md) for the shape this file grows into.

## What the product does

Renders clinical codes as inspectable references, edits and validates terminology query expressions, reviews codelists as hierarchies with include/exclude decisions, shows the aggregate effect of a concept set on a dataset supplied by the user, and supports hand adjudication of a sample of rows.

## What the product does not do

- It does not provide clinical decision support, diagnosis, treatment advice, triage, or any patient-specific output.
- It does not define clinical truth. A concept set it produces is a proposal for human review.
- It does not store, transmit, or receive patient data. It reads a dataset the user already holds and persists nothing without an explicit user action.
- It does not distribute terminology content, and does not determine whether a user's terminology licence permits their use.
- It does not reconstruct historical terminology editions. Where a lookup reflects the current release rather than the release in force at a record's date, that must be stated, not implied.

## Intended users and setting

Clinical informaticians, terminologists, researchers, and analysts working on their own machine with a terminology release they are licensed to use, and with a dataset they are already authorised to access. Not intended for use by clinicians at the point of care, and not intended to be deployed as a shared or hosted service in its current form.

## Clinical safety owner

Marcus Baw. No separate Clinical Safety Officer appointed, appropriate to a pre-release tool with no users. Revisit if the tool is deployed beyond individual local use.

## Known hazard themes

No formal hazard log yet; these are the failure modes the design already guards against, recorded so they are not rediscovered later. Each maps to an invariant in [agent-instructions.md](agent-instructions.md).

- **A retired code rendered with a plausible current term**, leading a user to believe a concept set covers records it does not. Mitigation: active status and forwarding target are shown wherever a code is rendered.
- **A truncated result presented as complete**, causing a codelist to be accepted as exhaustive when it is not. Mitigation: total, returned count, and truncation are always disclosed.
- **An unsupported expression construct silently broadened or narrowed** instead of refused, changing set membership without the user knowing. Mitigation: unsupported constructs are visible errors inherited from the backend, never quietly reinterpreted.
- **A current-release lookup mistaken for a point-in-time historical one**, misattributing coverage for records from an earlier edition. Mitigation: release identity is shown with every result and historical reconstruction is not claimed.
- **An expansion-count change read as a measured change in patients affected.** Mitigation: terminology counts and data effects are presented as separate quantities.
- **Licensed terminology terms or real patient rows leaking into notebook source, exports, logs, or an AI agent's context.** Mitigation: synthetic fixtures only in the repo; export and agent-session constraints are a design requirement of the first slice.

## Medical-device applicability

- **Intended purpose**: A software tool for designing, inspecting, and testing clinical concept sets and codelists against a user-supplied dataset, used by informatics and research professionals for data curation and analysis. It makes no diagnostic, prognostic, screening, monitoring, or treatment claim about any individual patient, and produces no patient-specific output.
- **Decision-maker and role**: Marcus Baw, project owner. **Provisional: drafted at scaffold time and awaiting the decision-maker's explicit confirmation.**
- **Decision date**: 2026-09-29 (draft).
- **Next review date**: 2027-03-29, or earlier on any reassessment trigger below.
- **Evidence considered**: The intended purpose and non-claims recorded above, and the product scope in [README.md](README.md) and [spec/roadmap.md](spec/roadmap.md). The primary UK guidance identified for review is MHRA's [borderline products](https://www.gov.uk/guidance/borderline-products-how-to-tell-if-your-product-is-a-medical-device) and [regulating medical devices in the UK](https://www.gov.uk/guidance/regulating-medical-devices-in-the-uk), plus NHS England's [DCB0129/DCB0160 applicability guidance](https://digital.nhs.uk/services/clinical-safety/applicability-of-dcb-0129-and-dcb-0160/step-by-step-guidance). **Outstanding action: these sources have not yet been read against this product; the conclusion below is provisional until they have been, with the access date recorded.** No professional or legal advice obtained.
- **Conclusion**: Medical-device obligations are considered **provisionally not applicable**, on the basis that the product is a data-curation and analysis tool for professional users with no patient-specific output and no clinical claim. This is a governance record, not a self-classification or regulatory advice.
- **Actions and owner**: Marcus Baw to read the guidance above against this record and confirm or revise the conclusion before any public release; preserve this record and the roadmap as technical documentation; reassess before any change that introduces patient-specific output.
- **Reassessment triggers**: any patient-specific or individual-level output; any diagnostic, prognostic, screening, or treatment claim; use by clinicians at the point of care; integration with an EHR, medical device, or clinical decision support system; deployment as a shared or hosted service; a change of intended users or population; a change in UK medical-device or NHS clinical-safety guidance; or placing the product on the market.

A conclusion that this is not a medical device does not remove the need to manage the clinical hazards listed above.
