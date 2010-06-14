try:
    import markdown
except:
    pass

try:
    import textile
except:
    pass

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from BeautifulSoup import BeautifulSoup

class Formatter:
    # The types of markup that are available
    MARKUP_CHOICES = (
        ('none', 'None'),
        ('brk', 'Linebreaks'),
        ('txl', 'Textile'),
        ('mrk', 'Markdown'),
    )
    def format(self, format, text):
        soup = BeautifulSoup(text)
        code_blocks = soup.findAll(u'code')

        # Put place holder blocks
        for block in code_blocks:
            block.replaceWith(u'<code class="removed"></code>')

        if format == 'none':
            text = str(soup) 
        elif format == 'brk':
            text = self.linebreaks(str(soup))
        elif format == 'txl':
            text = self.textile(str(soup))
        elif format == 'mrk':
            text = self.markdown(str(soup))

        soup = BeautifulSoup(text)
        index = 0
        empty_code_blocks = soup.findAll('code', 'removed')
        formatter = HtmlFormatter(linenos=False, cssclass='source')

        language = None
        for block in code_blocks:
            if block.has_key('class'):
                language = block['class']

        if language:
            try:
                lexer = get_lexer_by_name(language, stripnl=True, encoding='UTF-8')
            except ValueError, e:
                try:
                    lexer = guess_lexer(block.renderContents())
                except ValueError, e:
                    lexer = get_lexer_by_name('text', stripnl=True, encoding='UTF-8')

        else:
            try:
                lexer = guess_lexer(block.renderContents())
            except ValueError, e:
                lexer = get_lexer_by_name('text', stripnl=True, encoding='UTF-8')

        empty_code_blocks[index].replaceWith(
                highlight(block.renderContents(), lexer, formatter))

        index = index + 1

        return str(soup)

    def markdown(self, text):
        return markdown.markdown(text)

    def textile(self, text):
        return textile.textile(text)
    
    def linebreaks(self, text):
        return text.replace('\n', '<br />')
