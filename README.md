# unicodef

This program generates definitions of expandable sequences for use in
BSD / Linux systems (using Xorg/Xenocara/Wayland via XCompose), macOS
(via [Karabiner-Elements]), Windows (via [WinCompose]), and Vim,
usually to type unicode characters.

See [unicodef-thatex] for my own defs and their compiled outputs as an example use.

Feel free to use them directly if you wish; there is no need to install the
unicodef compiler to use them.

The compiler only serves if you want to define your own,
either from zero or just by adding or changing existing ones.


## Installation of unicodef

Just place `unicodef.py` somewhere in your path.


## Installation of outfiles

**tl;dr:** Just place the outfile(s) you want (or their content) in the
appropriate place and you are good to go.

See [unicodef-thatex] for instructions on how to install
your outfiles.

**N.B.:** You will need to restart your programs for changes to take effect,
and if you have multiple windows of the same program running you may need to
quit all of them.


## Usage (unicodef compiler)

**Requirements:** you will need Python 3 installed and it should
be callable as `python`.

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

This creates under the directory `outfiles`,
for each input file _φ_, the files

* _φ_`.md`
* _φ_`.XCompose`
* _φ_`.dict`
* _φ_`.vim`

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
[WinCompose]:         https://github.com/samhocevar/wincompose
[Karabiner-Elements]: https://karabiner-elements.pqrs.org/

