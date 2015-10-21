# this is what I built the thing for: reading papers from a JSON Zotero feed
# and writing them out to Slack

import os
import requests

# this formats a JSON entry and makes a nice Slack message with
# the person who added it, the paper title and journal, and a link
def format_json(entry):
    if 'creator' in entry['data']:
        return '{creator} added <{url}|{title}> - {journalAbbreviation}'.format(
            creator=entry['meta']['createdByUser']['name'], **entry['data'])
    else:
        return '{username} added <{url}|{title}> - {journalAbbreviation}'.format(
            creator=entry['meta']['createdByUser']['name'], **entry['data'])


# this is a hook for taking the new entries and sending them to a Slack app
# that will post them in the chat.
def output_entries(entries):
    for entry in entries:
        payload = {'channel': '#general', 'username': 'Zotero', 'text': entry}
        requests.post(url=os.environ['SLACK_WEBHOOK'], json=payload)
