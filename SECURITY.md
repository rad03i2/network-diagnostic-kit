# Security Policy

## Supported version

The latest version on the `main` branch is supported.

## Scope and safe use

Network Diagnostic Kit is a defensive troubleshooting utility. It performs bounded DNS, TCP, HTTP(S), and ping checks only against targets explicitly supplied by the user. It is not intended for unauthorized scanning, exploitation, packet interception, or credential collection.

Do not include secrets, private packet captures, access tokens, credentials, or sensitive infrastructure details in public vulnerability reports.

## Reporting

If you find a security problem, use GitHub's private security reporting feature when available. Otherwise, open a minimal public issue that describes the affected component without publishing exploit details or sensitive data, so a private follow-up can be arranged.

Dependencies should remain minimal; runtime currently uses only the Python standard library.
