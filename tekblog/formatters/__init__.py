import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from BeautifulSoup import BeautifulSoup
from django.conf import settings

SHOW_LINE_NUMBERS = getattr(settings, 'TEKBLOG_SHOW_LINE_NUMBERS', True)

def parse_content_with_code(formatter_class, text):
    """
    This will split out code blocks and highlight them
    and then format with the mark up language passed in.
    """
    index = 0
    last_index = 0
    escaped_blocks = []

    # Grab all code blocks, match <code> and <code class="foo">
    while index >= 0:
        index = text.find('<code', last_index)

        if index < 0:
            break

        mid_index = text.find('>', index)
        last_index = text.find('</code>', mid_index)

        # Whats between <code> and </code>
        code_to_esc = text[mid_index+1:last_index]

        lang = None

        lang_index = text[index:mid_index+1].find('class=')

        if lang_index > 0:
            lang = text[index:mid_index+1][lang_index+len('class="'):-2]

        if lang:
            try:
                lexer = get_lexer_by_name(language, stripnl=True,
                        encoding='UTF-8')
            except ValueError:
                # We eat this exception because handling if a language
                # wasn't found is the same as if this failed.
                pass

        if not lexer:
            try:
                lexer = guess_lexer(code_to_esc)
            except ValueError, e:
                lexer = get_lexer_by_name('text', stripnl=True,
                            encoding='UTF-8')

        formatter = HtmlFormatter(linenos=SHOW_LINE_NUMBERS, 
                cssclass='source')

        # Format the code as HTML and syntax highlight it
        escaped_code = highlight(code_to_esc, lexer, formatter)
        escaped_blocks.append(escaped_code)

    soup = BeautifulSoup(text)
    code_blocks = soup.findAll(u'code')

    # We have already formatted the code, don't allow the markup language
    # to do it a second time.
    for block in code_blocks:
        block.replaceWith(u'<code class="removed"></code>')

    # We run the formatted content back through beautiful soup
    # just to make sure its valid HTML
    soup = BeautifulSoup(parse_content(formatter_class, text))

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

    # Replace all the empty code blocks with the syntax highlighted html
    empty_code_blocks = soup.findAll('code', 'removed')
    for index, escaped_block in enumerate(escaped_blocks):
        empty_code_blocks[index].replaceWith(escaped_block)

    return str(soup)


def parse_content(formatter_class, text):
    """
    This will generate HTML for a specific markup language but will not
    highlight source code
    """
    if formatter_class:
        formatter = __import__('tekblog.formatters.%s' % formatter_class,
                fromlist=[formatter_class])

        if formatter:
            return formatter.parse(text)

    return text
