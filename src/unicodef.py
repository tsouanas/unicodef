# unicodef.py

import os
import re
import yaml
from glob import glob
from gencompose import data_to_mac_dict, read_paths
import click
from click import echo

# dict generator

def gendict(yaml_in, dict_out):
    yamldata = yaml.load(yaml_in.read(), Loader=yaml.Loader)
    all_maps = {}
    all_maps.update(**{str(k): str(v) for k, v in yamldata.items()})
    all_maps = read_paths(all_maps)
    text = data_to_mac_dict(all_maps)
    based = f'{{"§" = {text}}}'
    text = text.replace('"^" = ', r'"\\^" = ')
    text = text.replace('"~" = ', r'"\\~" = ')
    dict_out.write(text)
    dict_out.write('\n')

# shared

def translate(translator, w):
    return ''.join([ translator(c) for c in list(w) ])

def simple_trans(reps):
    return lambda c: reps[c] if c in reps else c

# XCompose

xcompose_reps = {
    '`': '<grave>',
    '~': '<asciitilde>',
    '!': '<exclam>',
    '@': '<at>',
    '#': '<numbersign>',
    '$': '<dollar>',
    '%': '<percent>',
    '^': '<asciicircum>',
    '&': '<ampersand>',
    '*': '<asterisk>',
    '(': '<parenleft>',
    ')': '<parenright>',
    '-': '<minus>',
    '_': '<underscore>',
    '=': '<equal>',
    '+': '<plus>',
    '"': '<quotedbl>',
    "'": '<apostrophe>',
    '/': '<slash>',
    '\\': '<backslash>',
    '|': '<bar>',
    '<': '<less>',
    '>': '<greater>',
    ',': '<comma>',
    '.': '<period>',
    ':': '<colon>',
    ';': '<semicolon>',
    ' ': '<space>',
    }

def xcompose_trans(c):
    if c in xcompose_reps:
        return xcompose_reps[c]
    elif c.isascii() and c.isalnum():
        return f'<{c}>'
    else:
        return ''

def micro_xcompose(k, v):
    assert '"' not in v, f'double quote found in value «{v}» of key «{k}»'
    return f'<Multi_key>{translate(xcompose_trans, k)} : "{v}"\n'

def macro_xcompose(k, v):
    assert '"' not in v, f'double quote found in value «{v}» of key «{k}»'
    return f'<Multi_key><Multi_key>{translate(xcompose_trans, k)}<space> : "{v}"\n'

# Vim

vim_reps = { '|': '<Bar>' }
vim_trans = simple_trans(vim_reps)

def micro_vim(k, v):
    return f'inoremap \\{translate(vim_trans, k)} {v}\n'

def macro_vim(k, v):
    return f'inoremap \\\\{translate(vim_trans, k)} {v}\n'

# Markdown

def firstlines_md(df_name):
    return [ f'## {df_name}\n',
             '| Sequence | Expansion |\n',
             '| :------- | :-------: |\n'
           ]

def common_md(k, v):
    return f'| ``{k}`` | {v} |\n'

# Yaml

yaml_reps = { "'": "''" }
yaml_trans = simple_trans(yaml_reps)

def micro_yaml(k, v):
    return f"'{translate(simple_trans(yaml_reps), k)}': '{translate(simple_trans(yaml_reps), v)}'\n"

def macro_yaml(k, v):
    return f"'§{translate(simple_trans(yaml_reps), k)} ': '{translate(simple_trans(yaml_reps), v)}'\n"

# Processors

writers = dict(
    xcompose = dict(micro = micro_xcompose, macro = macro_xcompose, ext = '.XCompose', tee = True),
    yaml     = dict(micro = micro_yaml,     macro = macro_yaml,     ext = '.yaml',     tee = True),
    md       = dict(micro = common_md,      macro = common_md,      ext = '.md',       tee = True),
    vim      = dict(micro = micro_vim,      macro = macro_vim,      ext = '.vim',      tee = True),
    )

def df_kvs(df):
    kvs = []
    for line in df:
        line = line.lstrip()
        if line.startswith('#') or not line.rstrip(): continue
        else:
            # micro file
            if df_mode(df) == 'micro':
                k, v = re.split(': +', line.strip())
                k, v = k[1:-1], v[1:-1]
            # macro file
            else:
                line = line.strip('\u0020\n')
                k, v = re.split(' +', line)
            kvs.append((k,v))
    return kvs

def df_name(df):
    return df.name.split('/')[-1].rstrip('.yaml')

def df_mode(df):
    return 'micro' if df.name.split('/')[-1].endswith('.yaml') else 'macro'

def process_df(df, outdir):
    kvs = df_kvs(df)
    mode = df_mode(df)
    name = df_name(df)
    for (wlang, writer) in writers.items():
        processor, ext, tee = writer[mode], writer['ext'], writer['tee']
        firstlines = firstlines_md(name) if wlang == 'md' else []
        lines = firstlines + [ processor(k,v) for (k,v) in kvs ]
        if tee:
            # write wlang chapter
            with open(f'{outdir}/{name}{ext}', 'w') as chapter_wlang:
                chapter_wlang.writelines(lines)
        with open(f'{outdir}/unicodefs{ext}', 'a') as book_wlang:
            book_wlang.writelines(lines)

# main

@click.command()
@click.argument('indir',  type=click.Path(exists=True))
@click.argument('outdir', type=click.Path(exists=True))
def main(indir, outdir):

    # clear outdir
    outfiles = os.listdir(outdir)
    for outfile in glob(f'{outdir}/*'):
        os.remove(outfile)

    # initialize unicodefs.md
    with open(f'{outdir}/unicodefs.md', 'w') as unicodefs_md:
        unicodefs_md.write('# unicodefs\n\n')

    # assertions
    defsfiles = os.listdir(indir)
    assert 'unicodefs' not in defsfiles and 'unicodefs.yaml' not in defsfiles, 'You cannot name your input file "unicodefs".'
    for defsfile in defsfiles:
        assert f'{defsfile}.yaml' not in defsfiles, f'conflict: both {defsfile} and {defsfile}.yaml exist; pick distinct names!'

    # process def files
    for defsfile in defsfiles:
        echo(f"Processing {defsfile}.")
        with open(f'{indir}/{defsfile}', 'r') as df:
            process_df(df, outdir)

    # use gencompose to create dicts
    echo(f"Creating dicts.")
    for y in glob(f'{outdir}/*.yaml'):
        with open(y, 'r') as yaml_in, \
             open(y.replace('.yaml', '.dict'), 'w') as dict_out:
            gendict(yaml_in, dict_out)
        os.remove(y)

if __name__ == '__main__':
    main()

