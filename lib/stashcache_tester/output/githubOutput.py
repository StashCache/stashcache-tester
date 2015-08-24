
import logging
import json
import time
import shutil

from stashcache_tester.output.generalOuput import GeneralOutput
from stashcache_tester.util.Configuration import get_option
from stashcache_tester.util.ExternalCommands import RunExternal


class GithubOutput(GeneralOutput):
    """
    
    :param dict sitesData: Dictionary described in :ref:`sitesData <sitesData-label>`.
    
    This class summarizes and uploads the download data to a github account.
    
    Github output requires additional configuration options in the main configuration in the section `[github]`.  An example configuration could be::
    
        [github]
        repo = https://github.com/StashCache/StashCache-Tests.git
        branch = gh-pages
        pushkey = ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1mvou4au5Gwot1InmenfkazSc8I+7jVjww6ognZhUJfPI7IZUiEU2piM9tUpQjr+7nEMca+JBPj37wfDY5C2jG6xIarqfJlieruCvfj3OQ/YAEm+YBQ5s0snVv/yNLEPs9rtp7Q7ZDuqlX/vRKnZCTAVXE5bpvJ+VGKWZqJRa1vW93hkCgvZUzcHzMEbUNEjyVoWRUA0VJJ/ZWg1oYgng4etEEahTqEqPaRSYucjq9okERP9X0mAl5c31MtsSvF6BVssHVpbQBSu7z3WOsI2SA1VPsiSpwjbo354eiF40b1FelXdS6+hUZNQa3yiw5R86VjjoyQFHcTWJoAw7N8Yr deploykey
        directory = data
        
        
    The configuration is:
    
    repo
        The git repo to commit the data to.
        
    branch
        The branch to install repo.
        
    pushkey
        The key to use to push to the repo.
        
    directory
        The directory to put the data summarized files into.
        
    
    """
    def __init__(self, sitesData):
        GeneralOutput__init__(self, sitesData)
        
        
    def _get_option(self, option, default = None):
        get_option(option, section="github", default=default)
        
    
    def _summarize_data(self):
        summarized = {}
        
        # Average download time per site.
        
        
        # Should we do violin plot?
        
        summarized = sitesData 
        return summarized
        
    
    def startProcessing(self):
        """
        Begin summarizing the data.
        """
        
        summarized_data = self.summarize_data(self.sitesData)
        
        # Download the git repo
        git_repo = self._get_option("repo")
        git_branch = self._get_option("branch")
        push_key = self._get_option("pushkey")
        RunExternal("git --quiet --branch %s clone https://%s@github.com/%s output_git" % (git_branch, push_key, git_repo))
        
        # Write summarized data to new file
        output_dir = self._get_option("directory")
        output_filename = "%s.json" % time.strftime("%Y%m%d-%H%M%S")
        output_file = os.path.join("output_git", output_dir, output_filename)
        if os.path.exists(output_file):
            logging.error("Error, output file %s already exists!" % output_file)
            sys.exit(1)
        
        with open(output_file, 'w') as outfile:
            json.dump(summarized_data, outfile)
        
        # Write filename to index file
        index_filename = os.path.join("output_git", output_dir, "index.json")
        if not os.path.exists(index_filename):
            logging.error("Index file does not exist, bailing")
            sys.exit(1)
        with open(index_filename) as index_file:
            index = json.load(index_file)
        
        # Should we limit the size of 'files' to only ~30 files (30 days?)
        index.files.append(output_filename)
        
        with open(index_filename, 'w') as index_file:
            json.dump(index, index_file)
        
        # Commit to git repo
        ExternalCommand("cd output_git; git add -f .")
        ExternalCommand("cd output_git; git commit -m \"Adding file %s\"" % output_filename)
        ExternalCommand("cd output_git; git push -fq origin %s" % git_branch)
        
        shutil.removetree("output_git")
        
