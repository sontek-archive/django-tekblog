from mock import Mock

def configure_mock(mock, **kwargs):
    if mock is None:
        mock = Mock()
    for arg, val in sorted(kwargs.items(),
                           key=lambda entry: len(entry[0].split('.'))):
        args = arg.split('.')
        final = args.pop()
        obj = mock
        for entry in args:
            obj = getattr(obj, entry)
        setattr(obj, final, val)
    return mock
