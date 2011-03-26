import textile
from BeautifulSoup import BeautifulSoup
from tekblog.formatters.htmlblock_formatter import HtmlCodeBlockFormatter

class TextileFormatter(HtmlCodeBlockFormatter):
    """
    Parses textile markup into HTML
    """
    def parse(self):
        self.soup = BeautifulSoup(textile.textile(text))
