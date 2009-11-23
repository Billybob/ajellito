import time
import string
import os

import settings

try:
    settings.CACHE_BACKEND
    CACHE_ENABLED = True
except AttributeError:
    CACHE_ENABLED = False

try:
    UNRESTRICTED_SIZE = settings.UNRESTRICTED_SIZE
except AttributeError:
    UNRESTRICTED_SIZE = False

class PrintableCards:
    def __init__(self, selected):
        self.ini = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'LabelSpecs.ini')
        self.selected = selected
        self.template = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates/template.odt')

try:
    PRINTABLE_CARDS = PrintableCards(settings.PRINTABLE_CARD_STOCK)
except AttributeError:
    PRINTABLE_CARDS = None

ALPHABET = ''.join(c for c in string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation if c != '.')
BASE = len(ALPHABET)

def num_encode(n):
    s = []
    while True:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
        if n == 0: break
    return ''.join(reversed(s))

CACHE_PREFIX = num_encode(os.getpid()) + '.'
CACHE_PREFIX += '.'.join(str(num_encode(int(p))) for p in str(time.time()).split('.'))

try:
    from dulwich.repo import Repo
    BACKLOG_ARCHIVE = settings.BACKLOG_ARCHIVE
    if not os.path.exists(os.path.join(BACKLOG_ARCHIVE, '.git')):
        BACKLOG_ARCHIVE = None
except AttributeError:
    BACKLOG_ARCHIVE = None
except ImportError:
    BACKLOG_ARCHIVE = None
