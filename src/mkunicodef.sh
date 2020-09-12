#!/bin/sh

# split defs to sequences and expansions
awk '{ print $1; }' defs > defs.seq
awk '{ print $2; }' defs > defs.exp

# [unicodef.md]
sed 's/^\(.*\)$/\| `\1` \|/g' defs.seq > tmp.seq
sed 's/$/ |/'                 defs.exp > tmp.exp
print '# List of unicodefs \n'   >  unicodef.md
print '| Sequence | Expansion |' >> unicodef.md
print '| :------- | :-------: |' >> unicodef.md
paste -d ' ' tmp.seq tmp.exp     >> unicodef.md

# [unicodef.vim]
sed 's/^/inoremap \\\\/g' defs > unicodef.vim

# [.XCompose-unicodef]
sed -f XCompose.sed  defs.seq > tmp.seq
sed 's/\(.*\)/"\1"/' defs.exp > tmp.exp
paste -d ' ' tmp.seq tmp.exp  > XCompose-unicodef

# clean tmpfiles
rm -f tmp.seq tmp.exp

