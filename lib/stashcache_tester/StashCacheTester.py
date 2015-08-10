
import ConfigParser
import logging
import logging.handlers
import os, sys
import re
# TODO: possibly use PackageLoader
from jinja2 import Environment, FileSystemLoader

from stashcache_tester.Site import Site

from stashcache_tester.util.StreamToLogger import StreamToLogger


class StashCacheTester(object):
    """Main class for the stash cache tester"""
    def __init__(self, configFiles):
        
        # First, read in the configuration
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(configFiles)
        
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
        
        # Create the site specific tests
        test_dirs = []
        for site in split_sites:
            tmp_site = Site(site)
            test_dir = tmp_site.createTest()
            test_dirs.append(test_dir)
        
        
        # Create the DAG from the template
        env = Environment(loader=FileSystemLoader('templates'))
        dag_template = env.get_template("dag.tmpl")
        print dag_template.render(sites=split_sites)
        
        
        # Start the DAG
        
        
    def reduceResults(self):
        """
        Reduce the results from the DAG to something useful
        """
        pass
        
        