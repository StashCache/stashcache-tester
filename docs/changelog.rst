Changelog
=========

Version 0.0.8
-------------

* Remove host key check from the github output type.

Version 0.0.7
-------------

* Adding tests directory to contain configurations for testing the tester.
* Changing default test output directory from ``tests`` to ``stashtests`` to not conflict with the new tests directory.
* Add stdout and stderr redirection for the ``site_post.py`` post processing script.


Version 0.0.5 & 0.0.6
---------------------

* Small bug fixes from 0.0.4.  


Version 0.0.4
-------------

* Add timeout to site test jobs if they are running too long or idle too long.
* Changed the site_post.py to use HTCondor's Python bindings rather than regular expressions.


Version 0.0.3
-------------

* Added plugin based output formation.  The output class can now be specified in the configuration variable ``outputtype``.  The plugin should subclass the :py:class:`stashcache_tester.output.generalOutput.GeneralOutput` class.
* Adding Git output plugin to upload summarized data to a github repo.  It's further documented at :py:class:`stashcache_tester.output.githubOutput.GithubOutput`
