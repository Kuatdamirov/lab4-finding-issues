# Lab 4 — Finding an issues (Flask)

Demonstrates three common issues and their fixes:
1) **CWE-209**: Information disclosure through verbose errors (debug/stack trace)
2) **CWE-798/CWE-200**: Hardcoded/exposed secrets in repo
3) **CWE-502**: Unsafe deserialization (pickle on user input)

## How to run (fixed version)
1. Create `.env`:
SECRET_KEY=sk_live_rotated
DB_PASSWORD=P@ssw0rd!
API_TOKEN=ghp_rotated_example
2. Install deps: `python -m pip install -r requirements.txt`  
3. Run: `python app.py`
4. Check:
   - `GET /` → `OK`
   - `GET /cause_error` → `{"error":"Internal server error"}`
   - `POST /deser` with JSON `{"role":"admin"}` → `{"ok": true, "role": "admin"}`

## Reproducing original issues (vulnerable state)
- Verbose error: `GET /cause_error` shows stack trace
- Secrets in repo: `config.yml`, `SECRET_KEY` in `app.py` (old commit)
- Unsafe deserialization: `POST /deser` accepted base64-pickle payload

## Fix summary
- Disabled debug; added generic 500 handler
- Moved secrets to environment (`.env`), stopped tracking `config.yml`
- Replaced `pickle.loads` with JSON + validation

## Risk matrix
| Issue | CWE | Severity | Mitigation |
|---|---|---|---|
| Verbose errors | 209 | Medium | Generic 500 + server-side logging |
| Exposed secrets | 798/200 | High | Secrets in env; rotate tokens; `.gitignore` |
| Unsafe deserialization | 502 | Critical | JSON input + validation |

## Links
- Repo: <URL>
- Pull Request with fixes: <PR URL>
- Issues: <#1>, <#2>, <#3>
