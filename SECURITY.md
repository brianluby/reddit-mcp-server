# Security Policy

## Supported Versions

Currently, only the latest release of the Reddit MCP Server is supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please do not disclose it publicly. 

Instead, please send an email to the repository owner or use the GitHub Security Advisories feature to privately report the issue. We will strive to respond within 48 hours and release a patch as quickly as possible.

## Secret Scanning

This repository utilizes GitHub's native Secret Scanning. Please ensure you do not commit any personal API keys, Reddit app credentials, or tokens. If a secret is accidentally pushed, GitHub will notify you. However, you should consider any pushed secret compromised and revoke it immediately.
