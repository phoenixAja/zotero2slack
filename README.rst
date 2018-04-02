jsontail
=========

`Feedstail`_ is a tail-f-like utility for feeds. It aims to be hackable, and I'm hacking it
to read JSON instead of RSS.

I have a specific use-case in mind here: I want to read the JSON feed
of a Zotero library and feed it into Slack.

.. _Feedstail : https://github.com/Psycojoker/feedstail

License
-------

Feedstail and jsontail are both released under the terms of the `GNU General Public License v3`_ or later.

.. _GNU General Public License v3 : http://www.gnu.org/licenses/gpl-3.0.html


Get started
-----------

Retrieve the project with git and install it:

::

  $ git clone https://github.com/jamestwebber/jsontail.git
  $ cd jsontail
  $ python setup.py install

Then, launch jsontail with a random feed to test it:

::

  $ jsontail -u https://api.zotero.org/groups/200000/items/top?start=0&limit=5&format=json

Examples
--------

By default, jsontail will checkout the feeds every 15 minutes. If you
want to customize this interval you can use the ``i`` option.
The following example will retrieve feeds every 5 seconds:

::

  $ jsontail -u [feed url] -i 5


Formatting a JSON feed is a bit trickier than dealing with RSS. Because
the data you're receiving can be some arbitrary structure, I'm going to punt
on formatting it. Instead, you should point to a python file containing
your own formatting function, called "format_json".

::

  $ jsontail -f my_formatter.py
  $ cat my_formatter.py
  def format_json(entry):
      return '{title} - {url}'.format(**entry['data'])


Feedstail compares the ``id`` element to find new entries. You can
choose another element of comparison with the ``k`` option.
The following example says to feedstail to use 'key' to find new
entries:

::

  $ jsontail -u [feed url] -i 2 -k key


Importing to other python project
---------------------------------

Jsontail could (probably?) be imported to another python project with:
::

   from jsontail import feedGenerator
   from jsontail.config import Config

Options :
   * key : The comparison key. By default: ``id``
   * reverse : Boolean value for reversing the entries of the feed. By default: False
   * number : At the first time, show x entries. By default, it is None and shows all the received entries.
   * ignore_key_error : Boolean value for ignore keys errors. By default: False
   * no_endl : Boolean value for ignoring end lines. By default: False
   * url : The url. By default: None
   * format : The format of entries.

Options not present :
   * interval : The interval time for checking the feed.
   * one shot : Get once the feed.

The feedGenerator take an instance of Config as parameters and return a generator. This generator will return
an array of entries (could be an empty array) with the defined format.

Example:
::

   from jsontail import feedGenerator
   from jsontail.config import Config

   feed = feedGenerator(Config(format=u'{title} - {link}'))
   print '\n'.join(feed.next())

Contribute !
------------

- Fork the project: `https://github.com/jamestwebber/jsontail.git`_
- Create your patch in a topic branch
- Send pull requests or send your patches via e-mail

Don't forget to mark your commits by one of the following flag:

- [enh]: Your commit add a notable enhancement, a new feature for instance
- [fix]: Your commit is a bugfix
- [doc]: Your commit improve the documentation
- [mod]: Your commit bring general changes, matching neither of the above, like refactoring

.. _`https://github.com/jamestwebber/jsontail.git` : https://github.com/jamestwebber/jsontail.git
