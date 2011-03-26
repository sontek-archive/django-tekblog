import textile

def parse(text):
    """
    Parses textile markup into HTML
    """
    return textile.textile(text)
