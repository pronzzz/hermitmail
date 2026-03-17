# Contributing to HermitMail

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Pull Requests

1. Fork the repo and create your branch from `main`.
2. Ensure you have tested your code by running the `unittest` suites natively: `python -m unittest discover tests/`.
3. If you've added code that should be tested, add tests.
4. If you've changed APIs, update the documentation.
5. Ensure your PR description clearly describes the problem and solution.

## Code Standards

- HermitMail actively avoids SaaS logic. Any PR that adds API keys, analytics, external databases, cloud-backed LLMs, or tracking pixels **will be rejected immediately**.
- Python modules should be purely functional where feasible. Try not to maintain complex class state unless representing a Database connection.
