def get_context(mock_called_method):
    from mock import Mock
    assert isinstance(mock_called_method, Mock)
    assert len(mock_called_method.call_args)
    assert len(mock_called_method.call_args[0]) > 0
    return mock_called_method.call_args[0][1]
