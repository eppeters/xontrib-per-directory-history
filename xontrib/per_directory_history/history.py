import logging
from collections import defaultdict
from collections.abc import Sequence

import prompt_toolkit

from xonsh.ptk2.history import PromptToolkitHistory

from builtins import __xonsh__
from xonsh.events import events

logger = logging.getLogger(__name__)

use_local_history = True


def get_pwd():
    return __xonsh__.env.get('PWD')


def toggle_per_directory_history():
    global use_local_history
    use_local_history = not use_local_history
    if use_local_history:
        return 'local'
    else:
        return 'global'


_print = print


def print(*args, debug=True, **kwargs):
    """Prints debug messages only if env var is on."""
    if __xonsh__.env.get('XONTRIB_PER_DIRECTORY_HISTORY_DEBUG') or not debug:
        prompt_toolkit.application.run_in_terminal(
            lambda: _print(*args, **kwargs))


@events.on_ptk_create
def custom_keybindings(bindings, **kw):
    def do_nothing(func):
        pass

    key = __xonsh__.env.get('PER_DIRECTORY_HISTORY_TOGGLE')

    @bindings.add(key)
    def switch_between_global_and_local_history(_):
        new_hist_type = toggle_per_directory_history()
        print(f'Switching to {new_hist_type} history.', debug=False)
        __xonsh__.shell.prompter.default_buffer.reset()
        __xonsh__.shell.prompter.search_buffer.reset()


class PerDirectoryHistoryStrings(Sequence):
    """Act like a list, return PWD items based on use_local_history"""

    def __init__(self):
        self._pwd_strings = defaultdict(list)
        self._strings = []

    @property
    def pwd(self):
        return __xonsh__.env['PWD']

    def prepend_from_storage(self, string, pwd):
        self._pwd_strings[pwd].insert(0, string)
        self._strings.insert(0, string)

    def __multiplex_dunder_read(self, dunder_name, *args):
        """Read from global or local strings based on use_local_history."""
        global use_local_history
        if use_local_history:
            _list = self._pwd_strings[self.pwd]
        else:
            _list = self._strings
        return getattr(_list, dunder_name)(*args)

    def __getitem__(self, *args):
        return self.__multiplex_dunder_read('__getitem__', *args)

    def __missing__(self, *args):
        return self.__multiplex_dunder_read('__missing__', *args)

    def __iter__(self, *args):
        return self.__multiplex_dunder_read('__iter__', *args)

    def __reversed__(self, *args):
        return self.__multiplex_dunder_read('__reversed__', *args)

    def __contains__(self, *args):
        return self.__multiplex_dunder_read('__contains__', *args)

    def __len__(self, *args):
        return self.__multiplex_dunder_read('__len__', *args)

    def append(self, value):
        self._strings.append(value)
        self._pwd_strings[self.pwd].append(value)

    def insert(self, index, value):
        raise NotImplementedError(
            'Insertion anywhere but the beginning or end '
            'of history is not implemented (use append and prepend)!')


class PerDirectoryHistory(prompt_toolkit.history.ThreadedHistory):
    def __init__(self):
        super().__init__(PerDirectoryPTKHistory())
        self._loaded_strings = PerDirectoryHistoryStrings()

    def _start_loading(self):
        """
        Consume the asynchronous generator: `load_history_strings_async`.

        This is only called once, because once the history is loaded, we don't
        have to load it again.
        """

        def add_item(item):
            " Got one string from the asynchronous history generator. "
            self._loaded_strings.prepend_from_storage(*item)
            if self._filter_history_item(item):
                self._item_loaded.fire()

        yield prompt_toolkit.eventloop.From(
            prompt_toolkit.eventloop.consume_async_generator(
                self.load_history_strings_async(),
                cancel=lambda: False,  # Right now, we don't have cancellation
                # of history loading in any way.
                item_callback=add_item))

    def _filter_history_item(self, item):
        print(f'Got item {item}')
        global use_local_history
        if use_local_history and item[1] and \
                get_pwd() == item[1]:
            print('Using item')
            return True
        print('Not using item')
        return False

    def append_string(self, string):
        self._loaded_strings.append(string)

    def __repr__(self):
        return 'PerDirectoryPTKHistory(%r)' % (self.history, )


class PerDirectoryPTKHistory(PromptToolkitHistory):
    def __init__(self, load_prev=True, *args, **kwargs):
        """Initialize history object."""
        super().__init__(load_prev=load_prev, *args, **kwargs)
        print('Using per_directory_history plugin to provide PTK history')

    def load_history_strings(self):
        """Loads synchronous history strings"""
        print(f'load_prev={self.load_prev}')
        if not self.load_prev:
            return
        hist = __xonsh__.history
        if hist is None:
            return
        print('In load_history_strings')
        for cmd in hist.all_items(newest_first=True):
            print(f'Loading history item {cmd}')
            item = (
                cmd["inp"].rstrip(),
                cmd.get("pwd"),
            )
            strs = self.get_strings()
            if len(strs) == 0 or item[0] != strs[-1]:
                yield item
