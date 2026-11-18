"""OpenRouter API connection; this module never stores or logs keys."""
import requests
from errors import EvaluationError


def send_prompt(model, prompt, *, api_key, system=None):
    if not api_key.strip() or not model.strip() or not prompt.strip():
        raise EvaluationError('Enter an OpenRouter key, evaluator model, and prompt.')
    messages = [{'role': 'system', 'content': system}] if system else []
    messages.append({'role': 'user', 'content': prompt})
    payload = {'model': model.strip(), 'messages': messages, 'max_tokens': 8192}
    # The default model supports optional reasoning. Prompt review needs the final
    # rubric JSON, not a long reasoning trace or a solution to the embedded task.
    if model.strip().split(':')[0] == 'nvidia/nemotron-3.5-lightning':
        payload['reasoning'] = {'enabled': False}
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': 'Bearer ' + api_key.strip()},
            json=payload,
            timeout=(10, 75),
        )
    except requests.RequestException:
        raise EvaluationError('Connection failed or timed out. Please try again later.') from None
    if not response.ok:
        hints = {
            400: 'Check the exact model ID and account settings.',
            401: 'Key rejected. Paste your full OpenRouter secret key.',
            402: 'Credits are required for this request.',
            403: 'Check model access, permissions, and privacy settings.',
            404: 'Model or endpoint not found. Check the exact model ID.',
            429: 'Rate or daily quota reached. Pause requests and check usage.',
            503: 'Provider temporarily unavailable. Try later or another model.',
        }
        raise EvaluationError(f'HTTP {response.status_code}: ' + hints.get(
            response.status_code, 'The provider could not complete the request.'))
    try:
        data = response.json()
        if data.get('error'):
            raise EvaluationError('The provider returned an error. Check access and usage.')
        choice = data['choices'][0]
        if choice.get('finish_reason') == 'length':
            raise EvaluationError('The evaluator reached its output limit before finishing. Your prompt is kept. Try again later or use another evaluator model.')
        text = choice['message']['content']
        if not isinstance(text, str) or not text.strip():
            raise EvaluationError('The provider returned no text.')
        return text.strip()
    except (ValueError, KeyError, IndexError, TypeError):
        raise EvaluationError('The provider returned an unreadable response.') from None
