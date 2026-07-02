# Security Policy

## Supported Versions

This is a demo/learning project showcasing a DevSecOps CI/CD pipeline. Security fixes are applied to the `main` branch only.

| Branch | Supported          |
| ------ | ------------------ |
| main   | :white_check_mark: |
| other  | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please **do not open a public GitHub issue**.

Instead, report it privately using one of the following options:

- **GitHub Security Advisories** (preferred): go to the [Security tab](../../security/advisories) of this repository and click **"Report a vulnerability"**.
- **Email**: roman.chernyshev2008@gmail.com

Please include as much detail as possible:
- Steps to reproduce
- Affected component (API, Dockerfile, CI/CD workflow, etc.)
- Potential impact

You can expect an initial response within **48–72 hours**. If the vulnerability is confirmed, a fix will be prioritized and a security advisory will be published once resolved.

## Security Measures in This Project

This pipeline demonstrates several DevSecOps practices already in place:

- **Container scanning**: [Trivy](https://github.com/aquasecurity/trivy) scans the Docker image for `CRITICAL` and `HIGH` severity vulnerabilities on every CI run, failing the build if issues are found.
- **Secrets management**: sensitive values (e.g. `RAILWAY_TOKEN`, `TELEGRAM_TOKEN`) are stored as **GitHub Actions Secrets**, never committed to the repository.
- **Environment isolation**: local secrets are kept in a `.env` file, excluded from version control via `.gitignore`.
- **Containerization**: the application runs in an isolated Docker container, reducing the host attack surface.
- **Automated CI/CD checks**: every push/PR triggers the pipeline, including security scanning, before deployment to Railway.

## Known Limitations / Scope

This repository is intended as a **learning/demo project** for practicing DevSecOps concepts (CI/CD, container scanning, automated deployment, notifications). It has **not** undergone a formal, professional security audit and should not be treated as production-hardened without further review — including dependency auditing, SAST/DAST integration, and infrastructure hardening.

## Dependency Updates

Dependencies are currently managed manually via `requirements.txt`. Contributions enabling automated dependency scanning (e.g. Dependabot or Renovate) are welcome.