import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from BeautifulSoup import BeautifulSoup
from django.conf import settings
import os, sys, glob
import inspect

SHOW_LINE_NUMBERS = getattr(settings, 'TEKBLOG_SHOW_LINE_NUMBERS', True)

def parse_content_with_code(formatter_class, text):
    """
    This will split out code blocks and highlight them
    and then format with the mark up language passed in.
    """
    # We run the formatted content back through beautiful soup
    # just to make sure its valid HTML
    formatter = get_formatter(formatter_class, text)
    soup = formatter(text).get_html()

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

    return str(soup)

def load_modules(filemask='*.py', ignore_list=('__init__.py', )):
    """
    This loads all modules from the formatters directory
    """
    modules = {}
    dirname = os.path.dirname(__file__)

    if dirname:
        filemask = os.path.join(dirname, filemask)

    for fn in glob.glob(filemask):
        fn = os.path.split(fn)[1]

        if fn in ignore_list:
            continue

        fn = os.path.splitext(fn)[0]
        modules[fn] = __import__(fn, globals(), locals())

    return modules

def get_formatter(formatter_class, text):
    """
    This will generate HTML for a specific markup language but will not
    highlight source code
    """
    load_modules()
    current_module = sys.modules[__name__]
    formatter = get_module_classes(current_module, formatter_class)

    return formatter

def get_module_classes(module, formatter_class):
    """
    Recursively searches through all modules looking for the class
    that we are asking for
    """
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__name__ == formatter_class:
            return obj

    # Didn't find the class we want on that module, loop thorugh
    # its child modules
    for name, obj in inspect.getmembers(module, inspect.ismodule):
        if obj.__name__.startswith(__name__):
            cls = get_module_classes(obj, formatter_class)

            if cls:
                return cls

class HtmlCodeBlockFormatter(object):
    def __init__(self, text):
        self.text = text

    def pre_parse(self):
        """
        Parses out <code> blocks out of a block of text returns highlighted div
        list and a BeautifulSoup object for further parsing
        """
        index = 0
        last_index = 0
        escaped_blocks = []

        # Grab all code blocks, match <code> and <code class="foo">
        while index >= 0:
            index = self.text.find('<code', last_index)

            if index < 0:
                break

            mid_index = self.text.find('>', index)
            last_index = self.text.find('</code>', mid_index)

            # Whats between <code> and </code>
            code_to_esc = self.text[mid_index+1:last_index]

            lang = None

            lang_index = self.text[index:mid_index+1].find('class=')

            if lang_index > 0:
                lang = self.text[index:mid_index+1]
                lang = lang[lang_index+len('class="'):-2]

            if lang:
                try:
                    lexer = get_lexer_by_name(lang, stripnl=True,
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

        soup = BeautifulSoup(self.text)
        code_blocks = soup.findAll(u'code')

        # We have already formatted the code, don't allow the markup language
        # to do it a second time.
        for block in code_blocks:
            block.replaceWith(u'<code class="removed"></code>')

        self.soup = soup
        self.escaped_blocks = escaped_blocks

    def parse(self):
        pass

    def post_parse(self):
        # Replace all the empty code blocks with the syntax highlighted html
        empty_code_blocks = self.soup.findAll('code', 'removed')

        for index, escaped_block in enumerate(self.escaped_blocks):
            empty_code_blocks[index].replaceWith(escaped_block)

    def get_html(self):
        self.pre_parse()
        self.parse()
        self.post_parse()

        return self.soup
