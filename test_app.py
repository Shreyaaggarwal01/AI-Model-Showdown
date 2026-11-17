import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import requests
from streamlit.testing.v1 import AppTest
import app
VALID = {c: {'score': 3, 'reason': 'Important details are missing.'} for c in app.CRITERIA}
VALID['improved_prompt'] = 'Make an Animal class in [language] with [attributes].'

def reply(text):
    response = Mock(ok=True)
    response.json.return_value = {'choices': [{'finish_reason': 'stop', 'message': {'content': text}}]}
    return response

class PromptEvaluatorTests(unittest.TestCase):
    def test_accepts_json_fences_and_prose(self):
        for text in [json.dumps(VALID), '```json\n'+json.dumps(VALID)+'\n```', 'Here: '+json.dumps(VALID)]:
            self.assertEqual(app.parse_evaluation(text), VALID)

    def test_rejects_invalid_scores(self):
        for score in [True, 0, 6, '5', 2.5]:
            data = json.loads(json.dumps(VALID)); data['clarity']['score'] = score
            with self.assertRaises(app.EvaluationError): app.parse_evaluation(json.dumps(data))

    def test_prompt_only_request_and_private_key_exclusion(self):
        with patch('app.requests.post', return_value=reply(json.dumps(VALID))) as post:
            self.assertEqual(app.evaluate_prompt('private-key','model','Make an animal class'),VALID)
            body=post.call_args.kwargs['json']
            self.assertEqual(json.loads(body['messages'][1]['content']),{'prompt_to_evaluate':'Make an animal class'})
            self.assertNotIn('private-key',json.dumps(body))
            self.assertEqual(post.call_count,1)

    def test_api_errors_and_no_automatic_retries(self):
        for status in [401,402,403,404,429,503]:
            with patch('app.requests.post',return_value=Mock(ok=False,status_code=status)) as post:
                with self.assertRaisesRegex(app.EvaluationError,str(status)): app.evaluate_prompt('k','m','p')
                self.assertEqual(post.call_count,1)

    def test_timeout_and_truncation(self):
        with patch('app.requests.post',side_effect=requests.Timeout):
            with self.assertRaisesRegex(app.EvaluationError,'timed out'): app.evaluate_prompt('k','m','p')
        response=reply(json.dumps(VALID)); response.json.return_value['choices'][0]['finish_reason']='length'
        with patch('app.requests.post',return_value=response):
            with self.assertRaisesRegex(app.EvaluationError,'cut off'): app.evaluate_prompt('k','m','p')

    def test_browser_evaluation_rerender_and_clear_key(self):
        at=AppTest.from_file(str(Path(app.__file__)),default_timeout=10).run()
        at.sidebar.text_input[0].set_value('private-key')
        at.text_area[0].set_value('Make an animal class')
        with patch('app.requests.post',return_value=reply(json.dumps(VALID))) as post:
            next(b for b in at.button if b.label=='Evaluate my prompt').click().run()
            self.assertFalse(at.exception)
            self.assertEqual(at.metric[0].value,'12 / 20')
            self.assertNotIn('private-key',json.dumps(at.session_state['review']))
            at.run(); self.assertEqual(post.call_count,1)
            next(b for b in at.button if b.label=='Clear my key').click().run()
            self.assertFalse(at.exception)
            self.assertEqual(at.sidebar.text_input[0].value,'')
            self.assertEqual(post.call_count,1)

    def test_browser_error_keeps_prompt_without_fake_scores(self):
        at=AppTest.from_file(str(Path(app.__file__)),default_timeout=10).run()
        at.sidebar.text_input[0].set_value('key'); at.text_area[0].set_value('test prompt')
        with patch('app.requests.post',return_value=Mock(ok=False,status_code=429)):
            next(b for b in at.button if b.label=='Evaluate my prompt').click().run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.metric),0)
        self.assertEqual(at.session_state['review']['prompt'],'test prompt')
        self.assertIn('429',at.error[0].value)

if __name__=='__main__': unittest.main()
