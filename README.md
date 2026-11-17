# AI Prompt Evaluator
CS AI Club workshop project by Shreya and Olivia.

A simple Streamlit app evaluating **the prompt itself**, not a generated answer. Enter a prompt and see clarity, specificity, context, and output-requirement scores, explanations, and a suggested improved prompt beside it.

## Deploy a public website
1. Sign in at https://share.streamlit.io/ with GitHub.
2. Click **Create app** and choose **Deploy a public app from GitHub** if prompted.
3. Repository: `Shreyaaggarwal01/AI-Model-Showdown`.
4. Branch: `main`.
5. Main file path: `app.py`.
6. In Advanced settings select Python **3.12** if offered. No API key or secrets need to be added; attendees supply their own keys.
7. Click **Deploy**, then share the resulting `https://YOUR-APP.streamlit.app` URL.
8. Check sharing settings allow anyone with the link. Test from another browser/device before the meeting.

GitHub shares the code. `http://localhost:8501` only opens a local instance. Uploading code does not deploy the app; Streamlit deployment is a separate step.

## Attendee keys and limits
Each attendee enters their **own OpenRouter key** in the sidebar. The default evaluator is `nvidia/nemotron-3.5-lightning:free`; edit the ID if availability changes. Free models have rate and quota limits. Paid models may incur charges.

Streamlit's server handles the key transiently for that visitor's session and sends it to OpenRouter to authenticate the request. The app does not write keys to a file, include them in downloads, embed them in the repository, or share them across visitor sessions. Click **Clear my key** when finished. Do not add a club key to code, GitHub, or public configuration. This version does not load a `.env` or shared deployment secret: every visitor supplies their own key.

## Run locally
Python 3.10+ required; Python 3.12 recommended for deployment.
```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```
Open http://localhost:8501. Windows PowerShell activation: `.venv\Scripts\Activate.ps1`.

## Scoring and errors
Each criterion is 1–5, total 20. Requirements are judged proportionally: a simple question does not need elaborate context. Suggested improvements use placeholders for unknown requirements. Scores are AI opinions, may vary, and are not proof of prompt quality.

One API call per submission; no automatic retries. Invalid scores are rejected rather than fabricated. HTTP 401: key; 402: credits; 403: access; 404: model ID; 429: quota/rate limit; 503: provider availability. These are shown in the UI. Repeated retries or another key on the same account do not bypass quotas.

## Checks
```sh
python3 -m unittest -v test_app test_workshop
```
Tests use simulated API responses, not live credentials. Test a real evaluation with your own key before presenting. No secret keys are included in this repository.


## Project structure
```text
app.py               Streamlit browser interface and deployment entry point
main.py              Optional launcher: python3 main.py
models.py            OpenRouter API connection and safe error messages
evaluator.py         Prompt-scoring pipeline and JSON validation
rubric.py            Shared criteria and evaluator instructions
prompts.py           Academic, coding, creative, planning, math, writing, reasoning examples
errors.py            Shared expected-error type
starter/tasks.py     Three attendee coding TODOs
starter/solution.py  Completed reference solution
starter/README.md    Exercise steps and time guide
requirements.txt     Dependencies
test_app.py          Backend and browser checks
test_workshop.py     Starter/reference integration checks
```

## Work on your own computer
Clone this repo or click Code → Download ZIP. Open the project folder in VS Code and follow Run locally above. Enter your own OpenRouter key in the browser. You do not need the presenter's local files, virtual environment, or API key. Dependencies install from requirements.txt.

The example picker fills the prompt box; you can edit it before evaluating. For the coding activity follow starter/README.md. The sidebar's Workshop coding exercise selector switches between the completed app, attendee TODOs, and reference solution. The default remains Completed app, so deploying this repository runs the working evaluator.

**Deploy app.py on Streamlit Cloud**, not main.py or the starter files. main.py is only a convenience for starting the app locally. This project scores prompts; it does not compare generated answers across multiple models.
