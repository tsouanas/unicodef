#!/bin/sh

BUILDDIR=build

if [ "$#" -eq 0 ]; then
    printf "Usage: $0 DESFILE ..\n" >&2
    exit 1
fi

mkdir -p $BUILDDIR
rm -f $BUILDDIR/unicodefs.*

print '# List of defs \n' > $BUILDDIR/unicodefs.md

for defs in "$@"; do

    # skip if unreadable
    if ! [ -f "$defs" ]; then
        printf "Cannot read $defs." >&2
        continue
    fi

    defsname=$(basename "$defs")

    # abort if called "unicodefs"
    if [ "$defsname" = "unicodefs" ]; then
        printf 'ERROR: "unicodefs" is pretty much the only name you cannot use.\n' >&2
        printf 'unicodef.sh uses it to create a single file with all defs in it.\n' >&2
        exit 1
    fi

    # split $defs to raw.seq(uences) and raw.exp(ansions)
    awk '/^[^#]/{ print $1 > "raw.seq" ; print $2 > "raw.exp" }' "$defs"

    # markdown
    printf '\n## %s defs\n' "${defsname}" | tee -a "$BUILDDIR/unicodefs.md"  >  "$BUILDDIR/${defsname}.md"
    sed 's/^\(.*\)$/\| `\1` \|/g' raw.seq     > tmp.seq
    sed 's/\|/\\\|/' raw.exp | sed 's/$/ \|/' > tmp.exp
    printf '| Sequence | Expansion |\n'   | tee -a "$BUILDDIR/unicodefs.md"  >> "$BUILDDIR/${defsname}.md"
    printf '| :------- | :-------: |\n'   | tee -a "$BUILDDIR/unicodefs.md"  >> "$BUILDDIR/${defsname}.md"
    paste -d ' ' tmp.seq tmp.exp          | tee -a "$BUILDDIR/unicodefs.md"  >> "$BUILDDIR/${defsname}.md"

    # vim
    sed 's/^/inoremap \\\\/g' raw.seq > tmp.seq
    cat                       raw.exp > tmp.exp
    paste -d ' ' tmp.seq tmp.exp          | tee -a "$BUILDDIR/unicodefs.vim" > "$BUILDDIR/${defsname}.vim"

    # XCompose
    sed -f XCompose.sed  raw.seq > tmp.seq
    sed 's/\(.*\)/"\1"/' raw.exp > tmp.exp
    paste -d ' ' tmp.seq tmp.exp          | tee -a "$BUILDDIR/unicodefs.XCompose" >  "$BUILDDIR/${defsname}.XCompose"

    # YAML
    sed -f Karabiner.sed  raw.seq > tmp.seq
    sed 's/\(.*\)/"\1"/'  raw.exp > tmp.exp
    paste -d ' ' tmp.seq tmp.exp          | tee -a "$BUILDDIR/unicodefs.yaml" >  "$BUILDDIR/${defsname}.yaml"

done

# clean up
rm -f raw.seq raw.exp tmp.seq tmp.exp

