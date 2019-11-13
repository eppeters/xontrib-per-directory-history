import builtins

from .history import PerDirectoryHistory

builtins.__xonsh__.env['XONSH_STORE_PWD'] = True
builtins.__xonsh__.env['XONSH_PTK_HISTORY_CLASS'] = PerDirectoryHistory

__all__ = []
