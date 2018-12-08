# this is what I built the thing for: reading papers from a JSON Zotero feed
# and writing them out to Slack

import pathlib

import click
import html2text
import requests
import yaml


text_maker = html2text.HTML2Text()
text_maker.body_width = 0


# this formats a JSON entry and makes a nice Slack message with
# the person who added it, the paper title and journal, and a link
def format_json(entry):
    name = text_maker.handle(
        entry["meta"]["createdByUser"]["name"]
        or entry["meta"]["createdByUser"]["username"]
        or "somebody"
    ).strip()
    journal = text_maker.handle(
        entry["data"].get("journalAbbreviation", "")
        or entry["data"].get("publicationTitle", "")
        or entry["data"].get("libraryCatalog", "")
        or "some journal"
    ).strip()
    paper_title = text_maker.handle(entry["data"]["title"]).strip()

    if "url" in entry["data"] and entry["data"]["url"]:
        return f"{name} added <{entry['data']['url']}|{paper_title}> - {journal}"
    elif "DOI" in entry["data"] and entry["data"]["DOI"]:
        return f"{name} added <http://dx.doi.org/{entry['data']['DOI']}|{paper_title}> - {journal}"
    else:
        return f"{name} added {paper_title} - {journal}"


class FeedGenerator(object):
    def __init__(self, user, url, channel, webhook, most_recent=None, keep=10):
        self.user = user
        self.url = url
        self.channel = channel
        self.webhook = webhook

        self.most_recent = most_recent or []
        self.keep = keep

    def get_new(self):
        entries = requests.get(self.url).json()

        res = []
        for entry in map(format_json, entries):
            if entry not in self.most_recent:
                res.append(entry)
                self.most_recent.append(entry)

        self.most_recent = self.most_recent[-self.keep :]

        return res

    def post(self):
        for entry in self.get_new():
            payload = {"channel": self.channel, "username": self.user, "text": entry}
            requests.post(url=self.webhook, json=payload)


@click.command()
@click.option(
    "--config",
    "config_file",
    type=click.Path(),
    default=pathlib.Path.home() / ".config/zotero2slack/config.yaml",
)
@click.option("--build-cache", is_flag=True)
def main(config_file, build_cache):
    with open(config_file) as f:
        config = yaml.load(f)

    feed_names = [feed["user"] for feed in config["feeds"]]

    if len(feed_names) > len(set(feed_names)):
        raise ValueError("User for each feed should be unique")

    cache_file = pathlib.Path(config["cache_file"])
    keep = int(config["keep"])

    if cache_file.exists():
        with cache_file.open() as f:
            cache = yaml.load(f)
    else:
        cache = dict()

    feed_gens = dict()

    for feed in config["feeds"]:
        feed_gens[feed["user"]] = FeedGenerator(
            feed["user"],
            feed["url"],
            feed["channel"],
            feed["webhook"],
            most_recent=cache.get(feed["user"], []),
            keep=keep,
        )

    if build_cache:
        for user, feed_gen in feed_gens.items():
            cache[user] = feed_gen.get_new()
    else:
        for user, feed_gen in feed_gens.items():
            feed_gen.post()
            cache[user] = feed_gen.most_recent

    with cache_file.open("w") as out:
        yaml.dump(cache, out, default_flow_style=False)
