# Contributing

Thanks for improving Network Diagnostic Kit.

1. Use Python 3.10+ and create a virtual environment.
2. Install development requirements with `python -m pip install -e . pytest`.
3. Keep diagnostics bounded to an explicit user-supplied target; do not add broad scanning behavior.
4. Add or update tests for behavioral changes. External network operations in tests should be mocked whenever practical.
5. Run `python -m compileall -q src` and `python -m pytest` before opening a pull request.
6. Keep user-facing documentation accurate in both English and Arabic when behavior changes.

Please keep commits focused and never commit credentials, captures containing private traffic, or generated environments/build output.

## المؤلف

Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — @rad03i2
