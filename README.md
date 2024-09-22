# unicodef

This project consist of:

* `unicodef.sh`: a script which, given appropriate input files, generates definitions of unicode sequences for use in X11 (via XCompose), Windows (needs [WinCompose]) and Vim;
* `defs/*`: my own (mostly [ThaTeX] influenced) input files for that script;
* `outfiles/*`: the "compiled" outputs of my input files, ready to use.


## Provided definitions of sequences

See [unicodefs.md] for a list of all sequences defined by the provided files in `defs/`.


## Installation

**tl;dr:** Just place `outfiles/unicodefs.XCompose` or `outfiles/unicodefs.vim` or `outfiles/DefaultKeyBinding.dict` in the appropriate places and you're good to go.  No other file is needed.

### for X11
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

### for Windows
First install [WinCompose].
The `include` command works, so the same instructions apply as above, mutatis mutandis.

### for Vim
Place `unicodefs.vim` somewhere (for example, in `~/.unicodef/`) and have your `.vimrc` source it:
```
source ~/.unicodef/unicodefs.vim
```

### for macOS
1. Install [Karabiner-Elements] and configure: Simple Modifications › For all devices › `right_command → non_us_backslash`.
2. Place `DefaultKeyBinding.dict` under `~/Library/KeyBindings/` and restart the program you need to type in.

If you keep a local copy of unicodef on your disk, just `git pull` and `make macosinstall` to update your bindings.



## Usage

### in X11 / Windows
To use a sequence σ type <kbd>AltGr</kbd><kbd>AltGr</kbd>σ<kbd>Space</kbd>.
E.g.: Typing <kbd>AltGr</kbd><kbd>AltGr</kbd><kbd>n</kbd><kbd>a</kbd><kbd>t</kbd><kbd>s</kbd><kbd>space</kbd> simply writes `ℕ`.

### in Vim
To use a sequence σ type <kbd>\\</kbd><kbd>\\</kbd>σ in INSERT MODE.
E.g.: Typing `f : \\nats \\to \\nats` you get `f : ℕ → ℕ`.

### in macOS
To use a sequence σ type <kbd>RightCmd</kbd><kbd>RightCmd</kbd>σ<kbd>Space</kbd>
E.g.: Typing <kbd>RightCmd</kbd><kbd>RightCmd</kbd><kbd>n</kbd><kbd>a</kbd><kbd>t</kbd><kbd>s</kbd><kbd>space</kbd> simply writes `ℕ`.

## Making

The needed files are generated by `unicodef.sh` which, for each input file φ given creates the files

* φ`.md`
* φ`.XCompose`
* φ`.vim`
* φ`.yaml`

to be used when separate inclusion is needed; as well as the overall

* `unicodefs.md`
* `unicodefs.XCompose`
* `unicodefs.vim`
* `unicodefs.yaml`
* `DefaultKeyBindings.dict`

files.  Usually you should just use these ones.
Note that this means that you cannot call any defs file `unicodefs`.  Deal with it.

Using make(1):

* `make` runs `unicodef.sh` using all of `defs/*` as input files to generate all files;
* `make nomacos` is like `make` but skips the macOS part (does not generate `unicodefs.dict`);
* `make install` copies the generated files to `~/.unicodef/`;
* `make macosinstall` installs then symlinks `unicodefs.dict` to `~/Library/KeyBindings/DefaultKeyBinding.dict`;
* `make uninstall` removes `~/.unicodef/`;
* `make macosuninstall` uninstalls then removes the symlink mentioned above;
* `make clean` removes the auxiliary generated files;
* `make cleanall` removes *all* generated files.


[unicodefs.md]: outfiles/unicodefs.md
[ThaTeX]:       https://github.com/tsouanas/thatex
[WinCompose]:   https://github.com/samhocevar/wincompose
[Karabiner-Elements]: https://karabiner-elements.pqrs.org

