# Security policy

## Status

`clinical-widgets` is a pre-alpha scaffold with no release and no users. There is nothing deployed to attack, but reports are still welcome and will be acted on.

## Supported versions

None yet. Once releases begin, the latest published version is supported.

## Reporting a vulnerability

Report privately via [GitHub Security Advisories](https://github.com/pacharanero/clinical-widgets/security/advisories/new). If that is unavailable, email marcus@bawmedical.co.uk.

Please do not open a public issue for a vulnerability until it has been addressed.

Include what you can: affected version or commit, reproduction steps, impact, and whether any data was exposed. Expect an acknowledgement within a week.

## Scope

In scope: code in this repository, its dependency declarations, and its CI configuration.

Out of scope: vulnerabilities in terminology backends (report to [`sct`](https://github.com/pacharanero/sct/security) or the relevant server project), in marimo or other upstream dependencies (report upstream), and anything requiring an attacker who already has local access to the user's machine and data.

## Handling sensitive data in reports

This project is used alongside licensed terminology content and potentially identifiable clinical datasets. **Do not include licensed terminology terms, real patient data, or database paths in a report.** Use synthetic values that demonstrate the issue. A report that needs real data to explain it should say so and wait for a private channel to be arranged.
