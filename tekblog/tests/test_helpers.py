def get_context(mock_called_method):
    from mock import Mock
    assert isinstance(mock_called_method, Mock)
    assert len(mock_called_method.call_args)
    assert len(mock_called_method.call_args[0]) > 0
    return mock_called_method.call_args[0][1]

def pop_last_call(mock):
    if not mock.call_count:
        raise AssertionError('Cannot pop last call: call_count is 0')

    mock.call_args_list.pop()

    try:
        mock.call_args = mock.call_args_list[-1]
    except IndexError:
        mock.call_args = None
        mock.called = False

    mock.call_count -=1

