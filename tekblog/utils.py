try:
    import markdown
except:
    pass

try:
    import textile
except:
    pass

class Formatter:
    # The types of markup that are available
    MARKUP_CHOICES = (
        ('none', 'None'),
        ('brk', 'Linebreaks'),
        ('txl', 'Textile'),
        ('mrk', 'Markdown'),
    )
    def format(self, format, text):
        if format == 'none':
            return text 
        elif format == 'brk':
            return self.linebreaks(text)
        elif format == 'txl':
            return self.textile(text)
        elif format == 'mrk':
            return self.markdown(text)

    def markdown(self, text):
        return markdown.markdown(text)

    def textile(self, text):
        return textile.textile(text)
    
    def linebreaks(self, text):
        return text.replace('\n', '<br />')
