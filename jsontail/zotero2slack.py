# this is what I built the thing for: reading papers from a JSON Zotero feed
# and writing them out to Slack

import os
import requests

import html2text

text_maker = html2text.HTML2Text()
text_maker.body_width = 0

# this formats a JSON entry and makes a nice Slack message with
# the person who added it, the paper title and journal, and a link
def format_json(entry):
    name = text_maker.handle(entry['meta']['createdByUser']['name']
                             or entry['meta']['createdByUser']['username']
                             or 'somebody').strip()
    journal = text_maker.handle(entry['data'].get('journalAbbreviation', '')
                                or entry['data'].get('publicationTitle', '')
                                or 'some journal').strip()
    paper_title = text_maker.handle(entry['data']['title']).strip()

    if 'url' in entry['data'] and entry['data']['url']:
        return u'{creator} added <{url}|{paper_title}> - {journal}'.format(
            creator=name, journal=journal, paper_title=paper_title, **entry['data'])
    elif 'DOI' in entry['data'] and entry['data']['DOI']:
        return u'{creator} added <http://dx.doi.org/{DOI}|{paper_title}> - {journal}'.format(
            creator=name, journal=journal, paper_title=paper_title, **entry['data'])
    else:
        return u'{creator} added {paper_title} - {journal}'.format(
            creator=name, journal=journal, paper_title=paper_title, **entry['data'])


# this is a hook for taking the new entries and sending them to a Slack app
# that will post them in the chat.
def output_entries(entries, cachefile=None):
    if cachefile is not None:
        with open(cachefile) as f:
            recent = [line[:-1] for line in f]

    for entry in entries:
        if entry not in recent:
            payload = {'channel': os.environ['SLACK_CHANNEL'],
                       'username': os.environ['SLACK_USER'],
                       'text': entry}
            requests.post(url=os.environ['SLACK_WEBHOOK'], json=payload)
            recent.append(entry)

    if cachefile is not None:
        with open(cachefile, 'w') as OUT:
            print >> OUT, '\n'.join(recent[-5:])
