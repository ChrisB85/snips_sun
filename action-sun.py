#!/usr/bin/env python3
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import sched, time
import os, json, ast
import snips_common as sc
import snips_day as sd
import mqtt_client
from pprint import pprint

intents = mqtt_client.get_config().get('global', 'intent').split(",")
INTENT_FILTER_START_SESSION = []
for x in intents:
    INTENT_FILTER_START_SESSION.append(x.strip())

prefix = mqtt_client.get_config().get('global', 'prefix')

def start_session(hermes, intent_message):
    session_id = sc.get_session_id(intent_message)
    site_id = sc.get_site_id(intent_message)
    intent_name = sc.get_intent_name(intent_message)

    print("Starting device control session " + session_id)

    json_string = os.popen('/srv/homeassistant-cli/sun.sh').read()
    #print(json_string)
    json_data = ast.literal_eval(json_string)
    sun = json.loads(json.dumps(json_data))
    #pprint(sun)
    if intent_name == 'next_rising':
      text = "Słońce wschodzi o godzinie " + sd.get_local_time(sun["next_rising"])
    if intent_name == 'next_setting':
      text = "Słońce zachodzi o godzinie " + sd.get_local_time(sun["next_setting"])
    if intent_name == 'next_dusk':
      text = "Ciemno robi się o godzinie " + sd.get_local_time(sun["next_dusk"])
    if intent_name == 'next_dawn':
      text = "Jasno robi się o godzinie " + sd.get_local_time(sun["next_dawn"])

    hermes.publish_end_session(session_id, text)

with Hermes(mqtt_options = mqtt_client.get_mqtt_options()) as h:
    for a in INTENT_FILTER_START_SESSION:
        h.subscribe_intent(prefix + a, start_session)
    h.start()
