import textwrap
import math
import sys

import pytest

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

@pytest.mark.skipif(not math.isfinite(sys.maxsize), reason='Turing complete')
def test_missing_integers_for_inf_word_size():
    with raises(OSError, match='Your system lacks some of the integers'):
        make_program(get_lines("%format word inf"))

def test_cyclic_labels():
    assert make_program(get_lines("""
        %format word 2
        %section state
        .word end - begin  ; 2 bytes
        begin:
        .ascii "Hello"     ; 5 bytes
        .byte 0            ; 1 byte
        .word 0            ; 2 bytes
        .zero 2 * begin    ; begin = 2, so 4 bytes
        .fill end, begin   ; begin = 2, so 2 bytes
        end:
    """)).state[0] == 5 + 1 + 2 + 4 + 2

    with raises(LabelError, match='concrete'):
        # Here the after label is defined, but has a cyclic dependency
        # which cannot be resolved.
        make_program(get_lines("""
            %format word 2
            %section state
            .zero after
            after:
        """))

    with raises(ExpressionError, match='defined'):
        # The potato label is not defined at all.
        make_program(get_lines("""
            %format word 2
            %section state
            .zero potato
            after:
        """))

def test_label_sections():
    prog = make_program(get_lines("""
        %format word 2
        %section state
        .word label_state
        .zero 5
        label_state:
        
        %section const
        .word label_const
        .zero 10
        label_const:
    """))
    assert prog.state[0] == 2 + 5
    assert prog.const[0] == 2 + 10

    with raises(NameConflictError, match='redefined'):
        make_program(get_lines("""
            %format word 2
            %section state
            .word label
            .zero 5
            label:
            
            %section const
            .word label
            .zero 10
            label:
        """))

@pytest.mark.parametrize("expr, expected", [
    ("2+2", 2+2),
    ("2+3*4", 2+3*4),
    ("2*3+4", 2*3+4),
    ("(2+3)*4", (2+3)*4),
    ("--1", --1),
    ("~-+-~+0", ~-+-~+0),
    ("2--1", 2--1),
    # Sphinx does not follow C convention for bitwise op order
    ("1<<4-1", (1<<4)-1),
    ("1+2&2", 1+(2&2)),
    ("('B' + 3) * 2", (ord('B') + 3) * 2)
])
def test_math(expr, expected):
    assert make_program(get_lines(f"""
        %format word 2
        %section state
        .word {expr}
    """)).signed(('sv', 0)) == expected

@pytest.mark.parametrize("expr, error", [
    ("(()", AssemblerSyntaxError),
    ("())", AssemblerSyntaxError),
    ("2++", AssemblerSyntaxError),
    ("2+/", AssemblerSyntaxError),
    ("2 2", AssemblerSyntaxError),
    ("1/0", EvaluationError)
])
def test_bad_math(expr, error):
    with raises(error):
        make_program(get_lines(f"""
            %format word 2
            %section state
            .word {expr}
        """))

def test_word_suffix():
    assert make_program(get_lines("""
        %format word 3
        %section state
        .word 10w
    """)).signed(('sv', 0)) == 30

    assert make_program(get_lines("""
        %section state
        .word 10w
        %format word 3
    """)).signed(('sv', 0)) == 30
