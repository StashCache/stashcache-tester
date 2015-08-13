
import ConfigParser
import logging
import logging.handlers
import os, sys
import re
import subprocess
# TODO: possibly use PackageLoader
from jinja2 import Environment, FileSystemLoader
import shutil

import humanfriendly
from stashcache_tester.Site import Site
from stashcache_tester.util.ExternalCommands import RunExternal

from stashcache_tester.util.StreamToLogger import StreamToLogger


class StashCacheTester(object):
    """Main class for the stash cache tester"""
    def __init__(self, configFiles):
        
        # First, read in the configuration
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(configFiles)
        self.config_location = os.path.abspath(configFiles)
        
        if self.config.has_section("logging"):
            loglevel = self.config.get("logging", "loglevel")
            logdirectory = self.config.get("logging", "logdirectory")
            self._setLogging(loglevel, logdirectory)
            

        
    def _setLogging(self, loglevel, logdirectory):
        logging_levels = {'debug': logging.DEBUG,
                          'info': logging.INFO,
                          'warning': logging.WARNING,
                          'error': logging.ERROR,
                          'critical': logging.CRITICAL}

        level = logging_levels.get(loglevel)
        handler = logging.handlers.RotatingFileHandler(os.path.join(logdirectory, "stashcachetester.log"),
                        maxBytes=10000000, backupCount=5)
        root_logger = logging.getLogger()
        # Clear out the logger
        root_logger.handlers = []
        
        root_logger.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        
        # Send stdout to the log
        stdout_logger = logging.getLogger()
        sl = StreamToLogger(stdout_logger, logging.INFO)
        sys.stdout = sl
 
        stderr_logger = logging.getLogger()
        sl = StreamToLogger(stderr_logger, logging.ERROR)
        sys.stderr = sl
        
        
    
    def runTests(self):
        """
        Run the tests prescribed in the configuration
        """
        # First, get the sites from the configuration
        sites = self.config.get("general", "sites")
        logging.debug("Got sites:\"%s\" from config file" % sites)
        if sites is None or sites is "":
            logging.error("No sites defined, therefore no tests created.")
            return
        
        split_sites = re.split("[,\s]+", sites)
        
        # Parse the size of the test in bytes
        raw_testsize = humanfriendly.parse_size(self.config.get("general", "testsize"))
        
        self.createTestFile(raw_testsize, self.config.get("general", "stashdir"))
        
        
        # Create the site specific tests
        env = Environment(loader=FileSystemLoader('templates'))
        env.globals = {
            "config_location": self.config_location,
            "stash_test_location": os.path.abspath(sys.argv[0]),
            "pythonpath": ":".join(sys.path),
            "testurl": self.config.get("general", "testurl"),
            "localpath": self.config.get("general", "stashdir"),
            "testsize": raw_testsize,
            "humantestsize": humanfriendly.format_size(raw_testsize)
        }
        
        test_dirs = []
        testingdir = self.config.get("general", "testingdir")
        for site in split_sites:
            tmp_site = Site(site)
            test_dir = tmp_site.createTest(testingdir, env)
            test_dirs.append(test_dir)
        
        
        # Create the DAG from the template
        
        dag_template = env.get_template("dag.tmpl")
        test_dag = os.path.join(testingdir, "submit.dag")
        with open(test_dag, 'w') as f:
            f.write(dag_template.render(sites=split_sites))
            
        
        reduce_template = env.get_template("test_reduce.tmpl")
        reduce_submit = os.path.join(testingdir, "reduce.submit")
        with open(reduce_submit, 'w') as f:
            f.write(reduce_template.render())
            
        shutil.copyfile("templates/site_post.py", os.path.join(self.config.get("general", "testingdir"), "site_post.py"))
        os.chmod(os.path.join(self.config.get("general", "testingdir"), "site_post.py"), 0755)
        
        # Start the DAG
        (stdout, stderr) = RunExternal("cd %s; condor_submit_dag submit.dag" % testingdir)
        logging.debug("output from condor_submit_dag: %s" % stdout)
        if stderr is not None or stderr is not "":
            logging.error("Error from condor_submit_dag: %s" % stderr)
        
    
    def createTestFile(self, size, location):
        """
        Create a file of size at location
        
        :param int size: size of the requested file
        :param str location: location to store test file
        """
        
        if os.path.isfile(location):
            logging.warning("File %s already exists." % location)
            if size == os.path.getsize(location):
                logging.warning("File %s is the correct size, not modifying")
                return
            else:
                logging.warning("File %s is incorrect size.  Should be %i, was %i" % (location, size, os.path.getsize(location)))
                logging.warning("Removing %s in order to create correctly sized test file" % location)
                os.remove(location)
        
        # Now, create the file of the correct size
        with open(location, 'wb') as f:
            # block size of 10 MB
            blocksize = 10 * (1024*1024)
            while (size > 0):
                f.write("\0" * blocksize)
                size -= blocksize
            
        
    
        
    def reduceResults(self):
        """
        Reduce the results from the DAG to something useful
        """
        pass
        
        
