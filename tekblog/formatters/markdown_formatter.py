import markdown
from BeautifulSoup import BeautifulSoup
from tekblog.formatters.htmlblock_formatter import HtmlCodeBlockFormatter

class MarkdownFormatter(HtmlCodeBlockFormatter):
    def parse(self):
        """
        Parses markdown text into HTML
        """
        self.soup = BeautifulSoup(markdown.markdown(str(self.soup)))
