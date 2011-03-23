try:
    import markdown
except:
    pass

try:
    import textile
except:
    pass

import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from BeautifulSoup import BeautifulSoup
from django.conf import settings

class Formatter:
    # The types of markup that are available
    MARKUP_CHOICES = (
        ('none', 'None'),
        ('brk', 'Linebreaks'),
        ('txl', 'Textile'),
        ('mrk', 'Markdown'),
    )

    def format(self, format, text):
        index = 0
        last_index = 0
        escaped_blocks = []

        while index >= 0:
            index = text.find('<code', last_index)

            if index < 0:
                break

            mid_index = text.find('>', index)
            last_index = text.find('</code>', mid_index)
            code_to_esc = text[mid_index+1:last_index]

            language = None

            lang_index = text[index:mid_index+1].find('class=')

            if lang_index > 0:
                language = text[index:mid_index+1][lang_index+7:mid_index-1]

            if language:
                try:
                    lexer = get_lexer_by_name(language, stripnl=True,
                            encoding='UTF-8')

                except ValueError, e:
                    try:
                        lexer = guess_lexer(code_to_esc)
                    except ValueError, e:
                        lexer = get_lexer_by_name('text', stripnl=True,
                                encoding='UTF-8')
            else:
                try:
                    lexer = guess_lexer(code_to_esc)
                except ValueError, e:
                    lexer = get_lexer_by_name('text', stripnl=True,
                            encoding='UTF-8')

            formatter = HtmlFormatter(linenos=False, cssclass='source')
            escaped_code = highlight(code_to_esc, lexer, formatter)
            escaped_blocks.append(text[0:mid_index] + escaped_code + text[mid_index+len(code_to_esc):])

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
        empty_code_blocks = soup.findAll('code', 'removed')

        # Find all instances of img tokens where the class has
        # replace-media-url replace all {{ MEDIA_URL }} tokens within the
        # src on that img token
        images = soup.findAll('img', attrs={
                'class':
                re.compile(r'.+replace-media-url')
            })

        for image in images:
            if 'src' in image and image['src'].startswith(
                    '{{ MEDIA_URL }}'):
                image['src'] = image['src'].replace(
                        '{{ MEDIA_URL }}', settings.MEDIA_URL)

        for index, escaped_block in enumerate(escaped_blocks):
            empty_code_blocks[index].replaceWith(escaped_block)

        return str(soup)


    def markdown(self, text):
        return markdown.markdown(text)

    def textile(self, text):
        return textile.textile(text)

    def linebreaks(self, text):
        return text.replace('\n', '<br />')
