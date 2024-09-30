# unicodef

This project consist of:

* `unicodef.py`: a script that generates definitions of expandable sequences for use in Xorg (via XCompose), macOS, Windows (needs [WinCompose]), and Vim, usually to type unicode characters;
* `defs/*`: my own (mostly [ThaTeX] influenced) definitions;
* `outfiles/*`: the "compiled" outputs of my inputs, ready to use.

See [unicodefs.md] for a list of all sequences defined by the provided files in `defs/`.


## Installation of outfiles

**tl;dr:** Just place the outfile(s) you want in the appropriate places and you're good to go.
No other file is needed.

**Beware.** You will need to restart your programs for changes to take effect,
and if you have multiple windows of the same program running you may need to quit all of them.


### for X11/Xorg

Place `unicodefs.XCompose` somewhere (for example, in `~/.unicodef/`) and have your `.XCompose` include it:
```
include "%H/.unicodef/unicodefs.XCompose"
```
In case you are not using a `.XCompose` file already, there is one provided in `examples/`.

Note that some programs might ignore `~/.XCompose`.  Hopefully you can make them behave by setting the environmental variables `$GTK_IM_MODULE` and `$QT_IM_MODULE` to `xim`.  For example, if you are using a sh-like shell:
```
export GTK_IM_MODULE=xim
export QT_IM_MODULE=xim
```

### for macOS

1. Install [Karabiner-Elements] and configure:  
   Simple Modifications › For all devices › `right_command → non_us_backslash`.  
   (`right_command` is under «Modifier keys» and `non_us_backslash` is under «Controls and symbols».)  
   Note that your <kbd>RightCmd</kbd> key will not function as a command key anymore.
   Feel free to choose some other key if you prefer.
2. Run `git clone https://github.com/tsouanas/unicodef` to clone this repo, `cd` into it, and run `make macosinstall`.

#### Warnings

1. If you are already using a `DefaultKeyBinding.dict`, then `make macosinstall`
   will overwrite the existing file, and `make macosuninstall` will delete it.
2. Do not symlink `DefaultKeyBinding.dict`, as some macOS programs will end up ignoring them!

### for Windows

1. Install [WinCompose].
2. The `include` command works, so the same instructions apply as for Xorg, mutatis mutandis.

### for Vim

Place `unicodefs.vim` somewhere (for example, in `~/.unicodef/`) and have your `.vimrc` source it:
```
source ~/.unicodef/unicodefs.vim
```


## Usage (typing)

There are two kinds of sequences: **micro** and **macro**.

To use a *micro* sequence σ, single-hit the <kbd>Compose</kbd> key and type the sequence σ:

E.g.: Typing <kbd>f</kbd><kbd>u</kbd><kbd>n</kbd><kbd>Compose</kbd><kbd>c</kbd><kbd>,</kbd><kbd>Compose</kbd><kbd>a</kbd><kbd>~</kbd><kbd>o</kbd> writes `função`.

To use a *macro* sequence σ, *double-hit* the <kbd>Compose</kbd> key, type the sequence σ, then hit the space key:

E.g.: Typing <kbd>Compose</kbd><kbd>Compose</kbd><kbd>n</kbd><kbd>a</kbd><kbd>t</kbd><kbd>s</kbd><kbd>space</kbd> simply writes `ℕ`.

* **In Xorg / Windows** use <kbd>AltGr</kbd> for <kbd>Compose</kbd>.
* **In macOS** use <kbd>RightCmd</kbd>.
* **In Vim** (in INSERT MODE) use <kbd> \ </kbd>: e.g., typing `f : \\nats \\to \\nats` you get `f : ℕ → ℕ`.


## Editing or creating your own defs

Sequences are defined by files under `defs/`; the file format is very simple:
each line is a sequence, followed by one or more spaces, followed by its expansion.
You may have blank lines and a `#` at the beginning of a line indicates a comment.

See `defs/simple_` or `defs/thatex` for examples.

Definitions in files whose names end with an underscore (`_`) are considered **micro**;
otherwise they are **macro**.  (See above.)

### Compiling defs

**Requirements:** you will need Python 3 installed.

Once you are done editing your defs files, use `unicodef.py` to generate the output files.
From within the `unicodef` directory run:

```shell
make
```

This creates, for each input file φ under `defs/`, the files

* φ`.md`
* φ`.XCompose`
* φ`.dict`
* φ`.vim`

under `outfiles/` (to be used if separate inclusion is needed—rarely);
as well as the files

* `unicodefs.md`
* `unicodefs.XCompose`
* `unicodefs.dict`
* `unicodefs.vim`

that contain all defined sequences.  (Usually you should just use these ones.)
N.B.: this means that you cannot call any input file `unicodefs`.

To update your files from the new outfiles run:

```shell
make install
```

on traditional Unix systems or

```shell
make macosinstall
```

on macOS.

#### Using make(1):

Inside the `unicodef` directory you can run:

* `make` runs `unicodef.py` on `defs/` generating files at `outfiles/`;
* `make install` copies all oufiles to `~/.unicodef/`;
* `make uninstall` removes `~/.unicodef/`;
* `make macosinstall` installs then copies `unicodefs.dict` to `~/Library/KeyBindings/DefaultKeyBinding.dict`;
* `make macosuninstall` uninstalls and also removes `~/Library/KeyBindings/DefaultKeyBinding.dict`;
* `make clean` removes all outfiles.

[unicodefs.md]: outfiles/unicodefs.md
[ThaTeX]:       https://github.com/tsouanas/thatex
[WinCompose]:   https://github.com/samhocevar/wincompose
[Karabiner-Elements]: https://karabiner-elements.pqrs.org/

