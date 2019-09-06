# xontrib-per-directory-history

## Take back your up arrow!

Limits the history available to commands that were executed in the current
working directory, with the option to switch to the usual global history using
a keybinding (by default `ctrl+G`).

The functionality this plugin provides is an almost criminally underrated shell
UI improvement. You will both be surprised by how much faster your history
scrolling is and how much more relevant the history entries are.  By default,
the only history entries you can scroll through on the command line (with the
up/down errors) is the history of commands executed in your current directory.
If you can't find what you're looking for in the local history, just hit
`Ctrl+G` to switch to the global history that you're used to from every other
shell.

Hopefully, once you use this for a little bit, you'll be incredibly frustrated
by the next shell you use that uses global history, and hopefully you'll port
this feature to that shell, too!

## Status & Limitations

This only works with the Prompt Toolkit 2 Xonsh shell backend as of this
writing. I have a strong sense that this is what most people are using, though.

For now, it also relies on some changes to Xonsh that make Xonsh store the PWD alongside
history commands, which changes have not yet been merged. See my fork, which
has the required changes:
[eppeters/xontrib-per-directory-history](https://github.com/eppeters/xontrib-per-directory-history).

## Installation

Ensure you're using the changes to Xonsh that include `PWD` storage
([eppeters/xontrib-per-directory-history](https://github.com/eppeters/xontrib-per-directory-history) 
for now until my PR is created and merged into [xonsh/xonsh](https://github.com/xonsh/xonsh/) proper).

Install with `xpip`:

```
xpip install git@github.com:eppeters/xontrib-per-directory-history.git
```

In your `.xonshrc` file, load the xontrib:

```
xontrib load per_directory_history
```

## Origin

This is a port of the wonderful
[jimhester/per-directory-history](https://github.com/jimhester/per-directory-history)
from ZSH, which I used for years, now for xonsh.
