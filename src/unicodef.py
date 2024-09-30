# unicodef.py

import os
import sys
import re
from glob import glob
from gencompose import data_to_mac_dict, read_paths

# global

modes = ['macro', 'micro']
book = dict(macro={}, micro={})
chapters = {}

# shared

def translate(translator, w):
    return ''.join([ translator(c) for c in list(w) ])

def simple_trans(reps):
    return lambda c: reps[c] if c in reps else c

def error(msg, status=1, die=True):
    print(f'ERROR: {msg}', file=sys.stderr)
    if die:
        sys.exit(status)

def warn(msg):
    print(f'Warning: {msg}', file=sys.stderr)

def info(msg):
    print(msg, file=sys.stderr)


# XCompose

xcompose_k_reps = {
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
    '?': '<question>',
    '\\': '<backslash>',
    '[': '<bracketleft>',
    ']': '<bracketright>',
    '{': '<braceleft>',
    '}': '<braceright>',
    '|': '<bar>',
    '<': '<less>',
    '>': '<greater>',
    ',': '<comma>',
    '.': '<period>',
    ':': '<colon>',
    ';': '<semicolon>',
    ' ': '<space>',
    }

xcompose_v_reps = {
    '"': '\\"',
    '\\': '\\\\',
    }


def xcompose_trans_k(c):
    if c in xcompose_k_reps:
        return xcompose_k_reps[c]
    elif c.isascii() and c.isalnum():
        return f'<{c}>'
    else:
        warn(f'Ignoring unexpected special character «{c}» on XCompose key.')
        return ''

xcompose_trans_v = simple_trans(xcompose_v_reps)

def xcompose_line(k, v, mode):
    k = translate(xcompose_trans_k, k)
    v = translate(xcompose_trans_v, v)
    if mode == 'micro':
        line = f'<Multi_key>{k} : "{v}"\n'
    else:
        line = f'<Multi_key><Multi_key>{k}<space> : "{v}"\n'
    return line


# Vim

vim_reps = { '|': '<Bar>' }
vim_trans = simple_trans(vim_reps)

def vim_line(k, v, mode):
    k = translate(vim_trans, k)
    v = translate(vim_trans, v)
    if mode == 'micro':
        line = f'inoremap \\{k} {v}\n'
    else:
        line = f'inoremap \\\\{k} {v}\n'
    return line


# Markdown

def md_header(title, level=1):
    return ''.join([
            f'{"#" * level} {title}\n',
             '| Sequence | Expansion |\n',
             '| :------- | :-------: |\n',
           ])

def md_line(k, v):
    return f'| ``{k}`` | {v} |\n'


# macOS dict

def chapter_pydict(chapter, macosprefix='§'):
    d = {}
    for (k,v) in chapter['micro'].items():
        d[k] = v
    for (k,v) in chapter['macro'].items():
        d[f'{macosprefix}{k} '] = v
    return d

def pydict_macosdict(pydict, macosprefix='§'):
    text = data_to_mac_dict(read_paths(pydict))
    text = f'{{"{macosprefix}" = {text}}}\n'
    text = text.replace('"^" = ', r'"\\^" = ')
    text = text.replace('"~" = ', r'"\\~" = ')
    return text


# Processors

langs = dict(
    xcompose = dict(liner=xcompose_line, ext='.XCompose'),
    vim      = dict(liner=vim_line,      ext='.vim'),
    )

def cf_name(cf):
    return cf.name.split('/')[-1].lstrip('_')

def cf_mode(cf):
    return 'micro' if cf.name.split('/')[-1].startswith('_') else 'macro'

def process_cf(cf, outdir):
    """
    Updates book and chapters global dicts by adding this cf's content.
    Also appends to markdown files of cf's chapter and of the book.
    """
    global book
    global chapters
    mode = cf_mode(cf)
    name = cf_name(cf)
    # initialize chapter if new
    if name not in chapters:
        chapters[name] = dict(macro={}, micro={})
    # open chapetr and book md files for appending
    with open(f'{outdir}/{name}.md', 'a') as chap_md, \
         open(f'{outdir}/unicodefs.md', 'a') as book_md:
        # append headers to md files
        chap_md.write(md_header(f'{name} ({mode})', level=1))
        book_md.write(md_header(f'{name} ({mode})', level=2))
        # process cs lines
        for line in cf:
            line = line.lstrip()
            if line.startswith('#') or not line.rstrip(): continue
            line = line.strip('\u0020\n')
            k, v = re.split(' +', line)
            # check for redefinitions
            if k in book[mode]:
                detail = f'to the same expansion: {v}' if v == book[mode][k] else f'{book[mode][k]} ↦ {v}'
                warn(f'{mode} sequence «{k}» redefined in {name} ({detail})')
            # update book and chapters
            book[mode][k] = v
            chapters[name][mode][k] = v
            # append content to md files
            chap_md.write(md_line(k, v))
            book_md.write(md_line(k, v))

def process_chapter(chapter, name, outdir):
    """
    Creates and writes .XCompose, .dict, and .vim outfiles.
    """
    # write lang files for chapter
    for (lang, writer) in langs.items():
        liner, ext = writer['liner'], writer['ext']
        lines = []
        for mode in modes:
            lines = lines + [ liner(k,v,mode) for (k,v) in chapter[mode].items() ]
        # write lang chapter
        with open(f'{outdir}/{name}{ext}', 'w') as chapter_lang:
            chapter_lang.writelines(lines)
    # create macosdict
    with open(f'{outdir}/{name}.dict', 'w') as chapter_macosdict:
        chapter_macosdict.write(pydict_macosdict(chapter_pydict(chapter)))


# main

def main():

    _, indir, outdir, *junk = sys.argv
    if junk: error(f'Too many arguments (expected: 2; given: {len(junk)}).')
    if not os.path.exists(indir):  error(f'{indir} does not exist.')
    if not os.path.exists(outdir): error(f'{outdir} does not exist.')
    if not os.path.isdir(indir):   error(f'{indir} exists, but is not a directory.')
    if not os.path.isdir(outdir):  error(f'{outdir} exists, but is not a directory.')

    # clear outdir
    outfiles = os.listdir(outdir)

    for outfile in glob(f'{outdir}/*'):
        os.remove(outfile)

    # initialize unicodefs.markdown
    with open(f'{outdir}/unicodefs.md', 'w') as book_md:
        book_md.write('# unicodefs\n\n')

    # assertion
    chapfiles = glob(f'{indir}/*')
    if ('unicodefs' in chapfiles) or ('_unicodefs' in chapfiles):
        error(f'You cannot name your input file "unicodefs".')

    # process chaptfiles to create chapters and all markdown files
    for chapfile in chapfiles:
        info(f"Processing {chapfile}.")
        with open(f'{chapfile}', 'r') as cf:
            process_cf(cf, outdir)

    # add book as a chapter called 'unicodefs'
    chapters['unicodefs'] = book

    # process chapters to create output files (except markdown)
    for (name, chapter) in chapters.items():
        process_chapter(chapter, name, outdir)


if __name__ == '__main__':
    main()

