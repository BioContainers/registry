edu.biocontainers.pro
=============

Share resources with the general public.

[![Build Status][travis]](https://travis-ci.org/BioContainers/edu)

[travis]: https://travis-ci.org/BioContainers/edu.svg?branch=master

How to contribute
---------------

For now here is a simple formula:

1. Fork the repository at [Github](https://github.com/BioContainers/edu)
2. Do awesomeness!
3. Send a pull request to [BioContainers/edu](https://github.com/BioContainers/edu)
4. Go back to step 2 and stay there as long as you want.
5. If we merge two or three pull requests, you get commit access. BAM.


Contributor list
----------------

Don't be shy - add yourself to the contributors list of an article.
The names are sorted alphabetically.

How to run
-----------

[Jekyll](http://jekyllrb.com/) is awesome.

```
bundle exec jekyll serve -w
```
(runs jekyll locally in the server mode + watching for changes)

[Install](http://jekyllrb.com/docs/installation/) jekyll.

Installing dependencies
-----------------------

We use [bundler](http://bundler.io/) (virtualenv for ruby).

```
gem install bundler
bundle install # in your edu root folder
```

You can then install all dependencies with

```
bundle install --path vendor/bundle
```

Jekyll layouts
-----------------

* `default`: the root layout (all layouts inherit from this)
* `series_item`: layout used to generate a page within a series


Special blocks: alert
--------------

Display alerts to the user

````
{% alert warn %}
Do you like BioContainers?
{% endalert %}
```

Available types include at the moment:

* `warn`: orange notification - use this for typical errors
* `danger`: red notification - deadly errors
* `info`: blue notification - some informative messages
* `ok`: green notification - positive messages (e.g. end of a tutorial)


Special blocks: hlblock
--------------

Can be used to emphasize content.

````
{% hlblock question %}
Do you like BioContainers?
{% endhlblock %}
```

Available types include at the moment:

* `info`: additional info and references
* `help`: tips, help, ...
* `task`: use this to assign tasks to your students
* `questions`: ask your readers questions
* `check`: checkpoint & verification
* `stop`: use this before you show a solution
* `raise`: (currently not used)

Special blocks: code
------------------------

We use `kramdown`, there you should use `~~~` to begin and mark a code block.
To enforce a language or make it collapsible (e.g. for solutions) you can use the `code` block.

```
{% code javascript collapsible=true %}
console.log("You can put this code block anywhere in your tutorial");
{% endcode %}
```

Add your own series
--------------------

It is super simple:

* add it to the `_config.yml`
* create a new folder in `series` (the name has to be identical with the `key` of your series in the `_config.yml`)
* add new pages to your series folder (don't forget to set your series in the header)
