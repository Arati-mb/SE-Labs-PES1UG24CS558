# Lab 5: Static Code Analysis — Issue Table

| Issue | Type | Line(s) Before Fix | Description | Fix Approach |
|---|---|---|---|---|
| Mutable default argument | Bug | 9 | Using `system_logs=[]` shares the same list across function calls. | Changed the default to `None` and initialized a new list inside the function. |
| Bare exception handling | Code quality | 21–22 | A bare `except` catches exceptions too broadly. | Changed it to `except ValueError:` and returned `False` when the seat was not booked. |
| Weak MD5 hash | Security | 29 | MD5 is a weak hash algorithm for security-sensitive uses. | Replaced MD5 with SHA-256 to generate the ticket code. |
| Permissive file permissions | Security | 61 (before cleanup) | Setting permissions to `0777` can allow excessive access. | Removed the unnecessary permission-changing operation. |
| Missing docstrings | Code quality | Multiple | Functions or the module lacked documentation. | Added descriptive docstrings. |
| Long lines and formatting issues | Style | Multiple | Some lines exceeded style limits and blank-line rules were violated. | Reformatted the code and corrected blank-line spacing. |

## Verification

- Ran Pylint after the fixes; final score: 10.00/10.
- Ran Bandit after the fixes; no issues identified.
- Ran Flake8 after the fixes; no issues reported.
