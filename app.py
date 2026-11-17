"""Browser interface. Start with: python3 -m streamlit run app.py"""
import json
from datetime import datetime, timezone

# Retained as a public module import for request mocking in the existing tests.
import requests
import streamlit as st
from errors import EvaluationError
from evaluator import evaluate_prompt, parse_evaluation
from prompts import PROMPTS
from rubric import CRITERIA, DEFAULT_MODEL


def clear_key():
    st.session_state.api_key = ''


def main():
    st.set_page_config(page_title='AI Prompt Evaluator', layout='wide')
    st.title('AI Prompt Evaluator')
    st.caption('CS AI Club · Shreya & Olivia · Evaluate your prompt—not the generated answer.')
    with st.sidebar:
        st.header('Evaluator setup')
        key = st.text_input('OpenRouter API key', type='password', key='api_key',
                            help='Use your own key. It is used for your session, not saved to a file or shared with other visitors.')
        model = st.text_input('Evaluator model ID', value=DEFAULT_MODEL)
        st.button('Clear my key', on_click=clear_key)
        st.caption('One request per evaluation. Free models have limits; paid models may incur charges.')
        st.link_button('Get an OpenRouter key', 'https://openrouter.ai/settings/keys')
        with st.expander('Workshop coding exercise'):
            implementation = st.selectbox('Implementation',
                ['Completed app', 'Attendee TODOs', 'Reference solution'])
            st.caption('The default app works as provided. TODO mode uses starter/tasks.py.')
    example = st.selectbox('Example prompt (optional)', ['Write my own'] + list(PROMPTS))
    with st.form('prompt_form'):
        prompt = st.text_area('Enter the prompt you want scored', height=160,
                              placeholder='Make an animal class', max_chars=8000,
                              value=PROMPTS.get(example, ''), key='prompt_' + example)
        submitted = st.form_submit_button('Evaluate my prompt', type='primary')
    if submitted:
        if not key.strip() or not model.strip() or not prompt.strip():
            st.error('Enter your API key, evaluator model, and prompt.')
        else:
            review = {'prompt': prompt.strip(), 'model': model.strip(),
                      'created_at': datetime.now(timezone.utc).isoformat()}
            st.session_state.review = review
            with st.spinner('Evaluating your prompt…'):
                try:
                    if implementation == 'Attendee TODOs':
                        from starter.tasks import evaluate_prompt as workshop_evaluate
                        review['evaluation'] = workshop_evaluate(key, model, prompt.strip())
                    elif implementation == 'Reference solution':
                        from starter.solution import evaluate_prompt as workshop_evaluate
                        review['evaluation'] = workshop_evaluate(key, model, prompt.strip())
                    else:
                        review['evaluation'] = evaluate_prompt(key, model, prompt.strip())
                except (EvaluationError, NotImplementedError) as exc:
                    review['error'] = str(exc)
    review = st.session_state.get('review')
    if not review:
        st.info('Enter a prompt to see its scores, feedback, and a suggested improvement.')
        return
    left, right = st.columns([3, 2])
    with left:
        st.subheader('Your prompt')
        st.write(review['prompt'])
        if 'evaluation' in review:
            st.subheader('Suggested improvement')
            st.write(review['evaluation']['improved_prompt'])
            st.caption('Fill in any [bracketed details] with your own requirements.')
    with right:
        st.subheader('Prompt evaluation')
        if 'error' in review:
            st.error(review['error'])
        else:
            result = review['evaluation']
            st.metric('Prompt score', f"{sum(result[c]['score'] for c in CRITERIA)} / 20")
            for criterion, label in CRITERIA.items():
                item = result[criterion]
                st.markdown(f"**{label}: {item['score']}/5**")
                st.progress(item['score'] / 5)
                st.caption(item['reason'])
    st.caption('Evaluator: ' + review['model'])
    if 'evaluation' in review:
        st.download_button('Save evaluation', json.dumps(review, indent=2),
                           file_name='prompt-evaluation.json', mime='application/json')
    st.caption('Scores are AI-generated guidance, not an objective grade. Keys are excluded from downloads. No automatic API retries are made.')


if __name__ == '__main__':
    main()
