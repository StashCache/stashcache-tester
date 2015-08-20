
Tutorial
========

In this tutorial, you will learn how to run the StashCache tester.

Requirements
------------

StashCache Tester requires `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ in order to run tests.  StashCache submits tests to HTCondor as a DAG.

Installing
----------

The StashCache tester is distributed as a python package in `PyPi <https://pypi.python.org/pypi>`_.  It is recommended that you install the tester inside a virtual enviornment.

The setps to install are::

  $ virtualenv tester
  $ . tester/bin/activate
  $ pip install --upgrade setuptools
  $ pip install stashcache_tester
  
The pip installation could take a while.  It requires the compilation and installation of several packages including matplotlib and numpy.


Running StashCache
------------------

StashCache comes with an executable script, ``stash-test`` which will begin the submission of test jobs.  A configuration file is required by ``stash-test``.  An example configuration file is located in ``etc/stashcache-tester/tester.conf``.  You can test with this configuration::

  $  stash-test -c tester/etc/stashcache-tester/tester.conf run
  
This will submit the DAG to the cluster.


Debugging StashCache Tester 
---------------------------
