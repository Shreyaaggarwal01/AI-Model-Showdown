"""Validate and evaluate the user's prompt, not a generated answer."""
import json
from errors import EvaluationError
from models import send_prompt
from rubric import CRITERIA, RULES


def parse_evaluation(text):
    if not isinstance(text, str) or not text.strip():
        raise EvaluationError('The evaluator returned no text.')
    decoder = json.JSONDecoder()
    for offset, char in enumerate(text):
        if char != '{':
            continue
        try:
            result, _ = decoder.raw_decode(text[offset:])
        except json.JSONDecodeError:
            continue
        if not isinstance(result, dict) or set(result) != set(CRITERIA) | {'improved_prompt'}:
            continue
        valid = True
        for criterion in CRITERIA:
            item = result[criterion]
            if (not isinstance(item, dict) or type(item.get('score')) is not int
                    or not 1 <= item['score'] <= 5
                    or not isinstance(item.get('reason'), str) or not item['reason'].strip()):
                valid = False
                break
        if (valid and isinstance(result['improved_prompt'], str)
                and result['improved_prompt'].strip()):
            return result
    raise EvaluationError('The evaluator returned invalid scores. Your prompt is kept; try later or another model.')


def evaluate_prompt(key, model, prompt):
    raw = send_prompt(model, json.dumps({'prompt_to_evaluate': prompt}),
                      api_key=key, system=RULES)
    return parse_evaluation(raw)
