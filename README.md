# Odin message retry: blank recording scaffold

This folder contains preparation material for the approved task: build a local
message-sending workflow with one optional retry. The Python files are blank
placeholders. No workflow implementation, completed tests, finished diagram or
test results are included.

The scaffold and sample inputs were prepared with Codex assistance. Follow the
project's disclosure rules; starter-code eligibility and use of AI-prepared
reference material must be confirmed with the Odin team. Complete the diagram,
implementation and tests during recording, as specified in the approved idea.

## Mac setup, before recording

Use Python 3.12 for the version combination selected for this exercise.

```bash
python3.12 --version
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -c "import fastapi, pydantic, uvicorn, langgraph, pytest, httpx; print('Dependencies ready')"
```

If Python 3.12 is unavailable, install it from the official Python source before
continuing. Do not reuse the Interviewer project's virtual environment.

Open this folder in VS Code, activate its virtual environment in Terminal, and
open a blank draw.io document in Chrome. Check the current eligibility of each
app in Studio. Test the recording tools before starting the real task. No API
keys, AI providers, live messaging service or database are needed.

## Work to perform during recording

1. Draw the workflow and save it under `diagram/`.
2. Implement the local sender, LangGraph workflow and FastAPI endpoint in `app.py`.
3. Implement the tests in `test_app.py`.
4. Run each example and compare actual results against the approved scenarios.
5. Save the results, inspect the finished files and record the required epilogue.

The `scenario` field in the fictional inputs controls a local simulation. It is
not an option for a real delivery service. Every request must start with a fresh
attempt counter and history.

## Commands to use AFTER implementing the application

These commands intentionally do not work against the blank placeholder files.
Name the FastAPI application object `app` and expose `POST /send`.

```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs` in Chrome. In another activated Terminal tab:

```bash
python -m pytest -v | tee results/pytest-results.txt
curl -sS -X POST http://127.0.0.1:8000/send -H 'Content-Type: application/json' --data-binary @examples/success.json | tee results/success-response.json
curl -sS -X POST http://127.0.0.1:8000/send -H 'Content-Type: application/json' --data-binary @examples/retry_success.json | tee results/retry-success-response.json
curl -sS -X POST http://127.0.0.1:8000/send -H 'Content-Type: application/json' --data-binary @examples/always_fail.json | tee results/always-fail-response.json
```

Check the pytest summary as well as the saved file. `tee` displays and saves
output; its exit status alone is not proof that pytest passed.

For submission, package the source, tests, requirements, diagram, sample inputs
and actual results as Studio requests. Exclude `.venv/` and Python caches.
Recordings and their exports are submitted separately according to Studio's UI.

The prepared study solution and narration notes remain on the Windows PC only;
they are not in this branch. Do not present prepared AI-generated work or
reasoning as work newly created during the recording.
