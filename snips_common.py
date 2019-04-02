
def get_session_id(intent_message):
    return intent_message.session_id

def get_site_id(intent_message):
    return intent_message.site_id

def get_intent_name(intent_message):
    return intent_message.intent.intent_name.split(':')[-1]
