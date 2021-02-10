#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import datetime

AUTHOR = 'Aneesh Vartakavi'
SITENAME = 'Aneesh Vartakavi'
SITEURL = ''
SITESUBTITLE = ''
PATH = 'content'
STATIC_PATHS = ['images']
SITELOGO = '/images/profile.jpg'
ARTICLE_PATHS = ['articles']
COPYRIGHT_NAME = 'Aneesh Vartakavi'
COPYRIGHT_YEAR = datetime.datetime.now().year

HOME_HIDE_TAGS = True
DISABLE_URL_HASH = True

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('', ''),
#         )

MENUITEMS = (
    ("About Me", "/about_me"),
)

DISPLAY_PAGES_ON_MENU = True

# Social widget
SOCIAL = (('LinkedIn', 'https://www.linkedin.com/in/aneeshvartakavi/'),
          ('Github', 'https://github.com/aneeshvartakavi'),
          )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = '../pelican-themes/Flex'

GITHUB_URL = 'https://github.com/aneeshvartakavi'
