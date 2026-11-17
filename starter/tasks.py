"""Complete these TODOs, then select Attendee TODOs in the app sidebar."""
import json
from models import send_prompt
from evaluator import parse_evaluation
from rubric import RULES


def build_payload(prompt):
    """TODO 1: Return JSON text with the key prompt_to_evaluate and the user's prompt."""
    raise NotImplementedError('Complete TODO 1 in starter/tasks.py: build_payload.')


def request_evaluation(key, model, prompt):
    """TODO 2: Call send_prompt(model, build_payload(prompt), api_key=key, system=RULES)."""
    raise NotImplementedError('Complete TODO 2 in starter/tasks.py: request_evaluation.')


def evaluate_prompt(key, model, prompt):
    """TODO 3: Call request_evaluation, pass its text into parse_evaluation, and return scores."""
    raise NotImplementedError('Complete TODO 3 in starter/tasks.py: evaluate_prompt.')
