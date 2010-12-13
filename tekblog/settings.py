import os
PROJECT_ROOT = os.path.dirname(__file__)

# Search Settings
HAYSTACK_SITECONF = 'tekblog.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, 'haystack')

# Comment Settings
COMMENTS_APP = 'tekrecaptcha'
