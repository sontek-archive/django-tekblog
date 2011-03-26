import markdown

def parse(text):
    """
    Parses markdown text into HTML
    """
    return markdown.markdown(text)
