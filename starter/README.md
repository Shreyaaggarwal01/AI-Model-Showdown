# 20-minute coding exercise

Keep the completed browser app running. Complete the three functions in tasks.py:

1. **build_payload (4 min):** Convert the user's prompt to JSON under prompt_to_evaluate.
2. **request_evaluation (6 min):** Send it to the selected model with the shared rubric as the system instruction. Use the supplied API wrapper.
3. **evaluate_prompt (5 min):** Parse and validate the returned evaluation, then return it.
4. **Try it (5 min):** In the browser sidebar expand Workshop coding exercise and select Attendee TODOs. Submit one short prompt and inspect the scores. Unfinished TODOs appear as clear messages; they do not break the Completed app mode.

Reference solution mode runs solution.py through the same browser interface. Never put API keys into these files. Every live submission uses quota and may cost money for paid models. Run tests without an API key with `python3 -m unittest -v test_app test_workshop`.

For local development save edits, then let Streamlit rerun. If it still uses an old imported module, stop and restart Streamlit once.
