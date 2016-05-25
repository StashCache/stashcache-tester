Changelog
=========

Version 0.4.0
-------------

* Check MD5sum of test file
* Correctly report failed downloads
* Use new module stashcp/3.0

Version 0.3.0
-------------

* Adding the ``maxdays`` to :py:class:`stashcache_tester.output.githubOutput.GithubOutput` to limit the number of days to keep data.


Version 0.2.0
-------------

* Add caching site to the output data for :py:class:`stashcache_tester.output.githubOutput.GithubOutput`

Version 0.1.1
-------------

* Fix bug in post site processing when certain output exists but is blank.

Version 0.1.0
-------------

* Reconfigure data layout for github output plugin.  It will now write to a single file, ``data.json``.  


Version 0.0.8
-------------

* Remove host key check from the github output type.
* Add condition to remove jobs which have had shadow exceptions more than 5 times.

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
