# Contributing

Thanks for considering a contribution. This document sets expectations so maintainers and contributors can work effectively.

## Status

Pre-alpha: the design is recorded in [`spec/roadmap.md`](spec/roadmap.md) and most of the listed work is not yet built. Discussion and issue threads are more useful than code at this stage. If you want to pick up a delivery slice, say so in an issue first.

## Before You Start

Read [`agent-instructions.md`](agent-instructions.md) and [`spec/roadmap.md`](spec/roadmap.md) before anything else: most architectural questions (the adapter boundary, the constraint-object contract, what this repo deliberately is not) are already answered there, and a proposal that contradicts a recorded decision needs to engage the recorded reason.

Search existing issues and pull requests before opening a new one. For non-trivial changes, discuss the problem and approach before writing substantial code.

## Issues

Bug reports should include the expected and actual behaviour, exact reproduction steps, relevant environment details, and redacted logs or screenshots. Do not include licensed terminology terms or real patient data in a report - use synthetic values (see [`SECURITY.md`](SECURITY.md) for why).

Feature requests should describe the underlying problem before proposing a solution.

## Pull Requests

1. Create a descriptive branch from `main`.
2. Keep the pull request focused on one coherent change.
3. Run the repository's documented validation commands before pushing: `s/lint`, `s/test`, `reuse lint`.
4. Update documentation and roadmap entries when they apply. Terminology semantics belong in the backend adapter, never in this repo - see [`agent-instructions.md`](agent-instructions.md).
5. Explain the change and its rationale in the pull request description.

## Direction

The maintainer named in the README has final responsibility for scope and design decisions. Discussion and constructive disagreement are welcome.

## Licence

By contributing, you agree that your contribution is licensed under this repository's licence ([AGPL-3.0-or-later](LICENSE)).

## Code Of Conduct

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to follow it.