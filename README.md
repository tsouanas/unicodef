# unicodef

This program generates definitions of expandable sequences for use in
Xorg/Xenocara/Wayland (via XCompose), macOS (via [Karabiner-Elements]),
Windows (via [WinCompose]), and Vim, usually to type unicode characters;

See [unicodef-thatex] for my own defs and their compiled outputs as an example use.


## Installation of unicodef

Just place `unicodef.py` somewhere in your path.


## Installation of outfiles

**tl;dr:** Just place the outfile(s) you want (or their content) in the
appropriate place and you are good to go.

See [unicodef-thatex] for examples of outfiles already compiled by unicodef
(under its `outfiles/` directory), along with the input defs files that were
used to produce them (under its `defs/`).
Feel free to use them directly if you wish; there is no need to install the
unicodef compiler to use them.

**N.B.:** You will need to restart your programs for changes to take effect,
and if you have multiple windows of the same program running you may need to
quit all of them.

### …for X11/Xorg (BSD, Linux, …)

Place `unicodefs.XCompose` somewhere (for example, in `~/.unicodef/`) and have
your `~/.XCompose` include it.  Make sure you include first the locale-specific
Compose file of your system if you want to access its definitions as well.
An example `~/.XCompose` file:
```
# locale-specific default Compose file
include "%L"

# unicodef
include "%H/.unicodef/unicodefs.XCompose"
```

Note that some programs might ignore `~/.XCompose`.  Hopefully you can make them behave
by setting the environmental variables `$GTK_IM_MODULE` and `$QT_IM_MODULE` to `xim`,
and `$XMODIFIERS` to `@im=none`.
For example, if you are using a sh-like shell, add the following lines to your shell configuration file
```sh
export GTK_IM_MODULE=xim
export QT_IM_MODULE=xim
export XMODIFIERS="@im=none"
```
**N.B.:** If you are not using `xim` alter the above lines accordingly.

### …for Windows

1. Install [WinCompose].
2. The `include` command works, so the same instructions apply as for Xorg, mutatis mutandis.

### …for macOS

macOS does not use XCompose, so it needs some further setup:

1. Install [Karabiner-Elements] and configure it (see below).
2. Create `~/Library/KeyBindings` if it does not exist:
   ```sh
   mkdir -p ~/Library/KeyBindings
   ```
3. Copy `unicodefs.dict` to `~/Library/KeyBindings/DefaultKeyBinding.dict`
4. Reboot(!)

**Warning.**
Do **NOT** symlink `DefaultKeyBinding.dict`, since this makes a lot of macOS programs ignore it!

#### Karabiner-Elements configuration

The idea is to sacrifice one key so that every time it is pressed
it sends the special character `§` which unicodef uses by default
as a "leader" for micros and macros.

A good option is to sacrifice the <kbd>RightCmd ⌘</kbd> key.
Note that your <kbd>RightCmd ⌘</kbd> key will not function as a command key anymore.
Feel free to choose some other key if you prefer.

You set up these modifications under the following settings path:

   Setting › Simple Modifications › For all devices

(If you want a per-keyboard configuration, select a specific keyboard instead of «For all devices».)

Exactly which modification will work for you depends on your keyboard type and on your macOS version.

The following options are known to work for certain combination:

* Option 1: `right_command → grave_accent_and_tilde`;
* Option 2: `right_command → non_us_backslash`;
* Option 3: `right_command → non_us_backslash` AND `non_us_backslash → grave_accent_and_tilde`.

`right_command` is under «Modifier keys»;  
`non_us_backslash` and `grave_accent_and_tilde` are under «Controls and symbols».

After setting this up, restart Karabiner-Elements from its menu,
quit (completely, as in `⌘-Q`) a program in which you want to test this (for example the Terminal),
launch the program from scratch, and press your <kbd>RightCmd ⌘</kbd> key once.
You should see a `§` printed on your terminal.
Complete the rest of the steps above.

### …for Vim

Place `unicodefs.vim` somewhere (for example, in `~/.unicodef/`) and have your `.vimrc` source it:
```vim
source ~/.unicodef/unicodefs.vim
```

## Usage (typing)

There are two kinds of sequences: **micro** and **macro**.

To use a *micro* sequence σ, single-hit the <kbd>Compose</kbd> key and type the sequence σ:

E.g.: Typing <kbd>f</kbd><kbd>u</kbd><kbd>n</kbd><kbd>Compose</kbd><kbd>c</kbd><kbd>,</kbd><kbd>Compose</kbd><kbd>a</kbd><kbd>~</kbd><kbd>o</kbd> writes `função`.

To use a *macro* sequence σ, *double-hit* the <kbd>Compose</kbd> key, type the sequence σ, then hit the space key:

E.g.: Typing <kbd>Compose</kbd><kbd>Compose</kbd><kbd>n</kbd><kbd>a</kbd><kbd>t</kbd><kbd>s</kbd><kbd>space</kbd> simply writes `ℕ`.

* **In Xorg / Windows** use <kbd>AltGr</kbd> for <kbd>Compose</kbd>.
* **In macOS** use <kbd>RightCmd ⌘</kbd>.
* **In Vim** (in INSERT MODE) use <kbd> \ </kbd>: e.g., typing `f : \\nats \\to \\nats` you get `f : ℕ → ℕ`.


## Usage (unicodef compiler)

**Requirements:** you will need Python 3 installed.

### Editing or creating your own defs

The so-called defs are defined in files; the file format is very simple:
each line is a sequence, followed by one or more spaces, followed by its expansion.
You may have blank lines and a `#` at the beginning of a line indicates a comment.
To add inline comments with `#` make sure it is following a space after the expansion
(otherwise the `#` symbol is considered to be part of that expansion).

Definitions in files whose names end with an underscore (`_`) are considered **micro**;
otherwise they are **macro**.  (See above for the difference in use.)

See the directory `defs/` of [unicodef-thatex] for examples of input defs files;
and the directory `outfiles/` of [unicodef-thatex] for examples of (generated) output files.

#### Custom contexts

The format described above makes it impossible for an expansion
to begin or to end with a space character.  To achieve such expansions you can use
the unicodef directive `#@[… ]` like so:
after the expansion place `@[𝑎X𝑧]` in a comment where `𝑎` and `𝑧` are strings
not including the character `X` (case sensitive).

For example, to have an expansion start with the space character, use `@[ X]`
(here `𝑎` is ` ` and `𝑧` is the empty string);
to have an expansion end with two space characters, use `@[X  ]`.

This is especially useful if you want to apply a combining character on the actual
space character and have the resulting character as (part of) the expansion.

### Compiling your defs

Once you are done editing your defs files, use `unicodef.py` to generate the output files.

For example, if you have your input files in a directory `defs/` and want the generated files
to be written in a directory `outfiles/`, run:

```shell
unicodef.py defs/* outfiles
```

This creates under the directory `outfiles`, for each input file φ, the files

* φ`.md`
* φ`.XCompose`
* φ`.dict`
* φ`.vim`

(to be used if separate inclusion is needed—rarely); as well as the files

* `unicodefs.md`
* `unicodefs.XCompose`
* `unicodefs.dict`
* `unicodefs.vim`

each containing all defined sequences from your input files.
(Usually you should just use these ones.)
**N.B.:** this means that you cannot call any input file `unicodefs`.


[unicodefs.md]:       outfiles/unicodefs.md
[unicodef-thatex]:    https://github.com/tsouanas/unicodef-thatex
[ThaTeX]:             https://github.com/tsouanas/thatex
[WinCompose]:         https://github.com/samhocevar/wincompose
[Karabiner-Elements]: https://karabiner-elements.pqrs.org/

