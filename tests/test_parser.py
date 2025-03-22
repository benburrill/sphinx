import textwrap
from spasm.errors import *
from spasm.parser import Parser as SphinxParser

from pytest import raises

def get_lines(src, raw=False):
    if not raw:
        src = textwrap.dedent(src).strip('\n')
    return src.encode('utf-8').split(b'\n')

def make_program(lines, args=()):
    ps = SphinxParser(args)
    ps.parse_lines(lines)
    return ps.get_program()

def test_formats():
    assert make_program(get_lines("")).mf.word_size == 2
    assert make_program(get_lines("%format word 3")).mf.word_size == 3
    assert make_program(get_lines("""
        %format word 3
        %format output byte
    """)).mf.word_size == 3

    with raises(AssemblerSyntaxError, match='output'):
        make_program(get_lines("%format output potato"))

def test_format_conflict():
    with raises(AssemblerError, match='conflict'):
        make_program(get_lines("""
            %format word 2
            %format word 3
        """))

    with raises(AssemblerError, match='conflict'):
        make_program(get_lines("""
            %format output byte
            %format output unsigned
        """))
