# unicodef

This project consist of:

* `unicodef.sh`: a script which given input files generates with definitions of unicode sequences for use in Xorg (via XCompose), Vim, etc.;
* `defs/*`: my own (mostly [ThaTeX] influenced) input files for that script;
* `outfiles/*`: the "compiled" outputs of my input files, ready to use.


## Provided definitions of sequences

See [unicodefs.md] for a list of all sequences defined by the provided files in `defs/`.


## Installation

**tl;dr:** Just place `build/unicodefs.XCompose` and `build/unicodefs.vim` in the appropriate places and you're good to go.  No other file is needed.

### for Xorg
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

### for Vim
Place `unicodefs.vim` somewhere (for example, in `~/.unicodef/`) and have your `.vimrc` source it:
```
source ~/.unicodef/unicodefs.vim
```


## Usage

### in X
To use a sequence σ type <kbd>AltGr</kbd><kbd>AltGr</kbd>σ<kbd>space</kbd>.
E.g.: Typing <kbd>AltGr</kbd><kbd>AltGr</kbd><kbd>n</kbd><kbd>a</kbd><kbd>t</kbd><kbd>s</kbd><kbd>space</kbd> simply writes `ℕ`.

### in Vim
To use a sequence σ type <kbd>\\</kbd><kbd>\\</kbd>σ in INSERT MODE.
E.g.: Typing `f : \\nats \\to \\nats` you get `f : ℕ → ℕ`.


## Making

The needed files are generated by `unicodef.sh` which, for each input file φ given creates the files

* φ`.md`
* φ`.XCompose`
* φ`.vim`

to be used when separate inclusion is needed; as well as the overall

* `unicodefs.md`
* `unicodefs.XCompose`
* `unicodefs.vim`

files.  Usually you should just use these ones.
Note that this means that you cannot call any defs file `unicodefs`.  Deal with it.

Using make(1):

* `make` runs `unicodef.sh` using all of `defs/*` as input files ;
* `make install` copies the generated files to `~/.unicodef/`;
* `make clean` removes the auxiliary generated files;
* `make cleanall` removes *all* generated files.


[defs]:        src/defs
[unicodef.md]: build/unicodef.md
[ThaTeX]:      https://github.com/tsouanas/thatex

