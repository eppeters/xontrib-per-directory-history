# xontrib-per-directory-history

Limits the history available to commands that were executed in the current working directory, with the option to switch to the usual global history using a keybinding (by default `ctrl+G`).

This is a port of [jimhester/per-directory-history](https://github.com/jimhester/per-directory-history) from ZSH, now for xonsh.

## Installation

Install with `xpip`:

`xpip install xontrib-per-directory-history`

In your `.xonshrc` file, enable the xontrib:

`xontrib load per-directory-history`

or just put `per-directory-history` at the end of the other xontribs you have loaded in your existing `xontrib load` statement.
