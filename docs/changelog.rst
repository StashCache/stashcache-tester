Changelog
=========


Version 0.0.3
-------------

* Added plugin based output formation.  The output class can now be specified in the configuration variable ``outputtype``.  The plugin should subclass the :py:class:`stashcache_tester.output.generalOutput.GeneralOutput` class.
* Adding Git output plugin to upload summarized data to a github repo.  It's further documented at :py:class:`stashcache_tester.output.githubOutput.GithubOutput`
