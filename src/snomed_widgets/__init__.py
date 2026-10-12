# SPDX-FileCopyrightText: 2026 Marcus Baw and Baw Medical Ltd
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Interactive widgets and data adapters for clinical informatics notebooks.

Nothing is implemented yet. The design, and the three spikes that must resolve
before implementation starts, are recorded in ``spec/roadmap.md``.

The intended public surface is deliberately small:

- a terminology *adapter* interface, so widgets work against a local database or
  a remote FHIR server without changing;
- *widgets* that render clinical codes as inspectable references, edit
  expressions, and review codelists;
- *dataset* helpers that turn a materialised concept set into a vectorised
  membership test over a dataframe.

No module outside the adapter layer should import a terminology backend
directly. See ``agent-instructions.md`` for the invariants this package holds.
"""

__all__ = ["__version__"]

__version__ = "0.0.0"
