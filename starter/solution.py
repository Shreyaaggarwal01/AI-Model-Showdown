"""Completed workshop solution; the production app uses evaluator.py by default."""
import json
from models import send_prompt
from evaluator import parse_evaluation
from rubric import RULES


def build_payload(prompt):
    return json.dumps({'prompt_to_evaluate': prompt})


def request_evaluation(key, model, prompt):
    return send_prompt(model, build_payload(prompt), api_key=key, system=RULES)


def evaluate_prompt(key, model, prompt):
    return parse_evaluation(request_evaluation(key, model, prompt))
