import os
os.environ["GOOGLE APPL CREDS HERE"] = "client.json"
import dialogflow_v2 as dflow
from gnewsclient import gnewsclient
dflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "DIALOGFLOW PROJECT ID HERE"
client = gnewsclient.NewsClient()

def intent_detection(text, session_id, language_code='en'):
    session = dflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dflow.types.TextInput(text = text, language_code)
    query_input = dflow.types.QueryInput(text = text_input)
    response = dflow_session_client.detect_intent(session = session, query_input=query_input)
    return response.query_result

def get_reply(query, chat_id):
    response = intent_detection(query, chat_id)

    if response.intent.display_name == 'get_news':
        return "get_news", dict(response.parameters)
    else:
        return "small_talk", response.fulfilment_text

def fetch_news(parameters):
    client.language = parameters.get("language")
    client.location = parameters.get("geo-location")
    client.topic = parameters.get("topic")
    return client.get_news()[:5]