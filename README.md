## zotero2slack

This started a bit more generally, but it really only has one use case that I've bothered working on: retrieve the JSON feed from a Zotero group and post it to a Slack channel.

It was originally based on [Feedstail](https://github.com/Psycojoker/feedstail) but at this point it's much more specialized.

### License

zotero2slack is released under the terms of the [GNU General Public License v3](http://www.gnu.org/licenses/gpl-3.0.html) or later.

### Get started

Retrieve the project with git and install it:

```shell
$ git clone https://github.com/jamestwebber/zotero2slack.git
$ cd zotero2slack
$ python setup.py install
```

You should make a `config.yaml` file in `$HOME/.config/zotero2slack` that contains the necessary info for it to work. A template file is provided in the repo. You can include multiple different feeds/channels for a single Slack workspace. In the config file you should specify a path for caching. If you lose the cache file you can repopulate it (without posting) by running with the `--build-cache` option.

Previous versions of this project would run forever in a loop, but this made configuration a little cumbersome because it required restarting the script. The current version only runs once, and if you want periodic updates you can write a cronjob, e.g.:

```shell
# m h  dom mon dow   command
*/15 * * * * zotero2slack > zstderr.log 2>&1
```

That will run the script every 15 minutes and write any errors to file `ztderr.log`. If you install into a virtual environment, you might need to use the full path to the script instead.
