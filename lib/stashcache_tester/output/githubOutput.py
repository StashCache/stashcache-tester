
import logging
from stashcache_tester.output.generalOuput import GeneralOutput
from stashcache_tester.util.Configuration import get_option


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
        
    pushkey
        The key to use to push to the repo.
        
    directory
        The directory to put the data summarized files into.
        
    branch
        The branch to install repo.
    
    """
    def __init__(self, sitesData):
        GeneralOutput__init__(self, sitesData)
        
        
    def _get_option(self, option, default):
        get_option(option, section="github", default=default)
        
    
    def _summarize_data(self):
        summarized = {}
        
        # Average download time per site.
        
        
        # Should we do violin plot?
        
        
        return summarized
        
    
    def startProcessing(self):
        """
        Begin summarizing the data.
        """
        
        summarized_data = self.summarize_data()
        
        # Download the git repo
        
        # Write summarized data to new file
        
        # Write filename to index file
        
        # Commit to git repo
        
        
        
        
