Brainfuck to Sphinx
===================

``to_sphinx.py`` translates brainfuck to Sphinx with a fixed input.

There are two modes:

The ``runner`` mode is a direct translation, where termination of the
brainfuck program translates into a done flag followed by terminal
non-termination in Sphinx.

Based on `examples/branch_table.s <../branch_table.s>`_, we *could*
transform halting brainfuck programs into a halting sphinx program, but
it's easier just to use terminal non-termination.  We technically don't
even need to use halt propagation in ``runner`` mode as brainfuck itself
has no time-travel capabilities, but it is used anyway for consistency
(see discussion below).

The ``forecaster`` mode produces a sphinx program which "immediately"
outputs a flag to the user indicating whether the brainfuck program
would halt, and then a done flag before entering an infinite loop.  This
is a bit of a trick -- in the case that the brainfuck code will not halt
this infinite loop is not the usual terminal non-termination that often
follows a done flag, it's just running the brainfuck program with output
suppressed.  In the other case, it doesn't need to enter an infinite
loop at all, and just does so for consistency.

Usage::

    $ python to_sphinx.py MODE BF_FILE [DATA_SIZE] > SPHINX_FILE
    $ spasm SPHINX_FILE [INPUT]

Where MODE is either ``runner`` or ``forecaster``, BF_FILE is the
brainfuck source file and DATA_SIZE is the number of bytes of data
(default 1000).

The resulting sphinx code takes the input to be read by ``,`` as a
command line argument INPUT (default: empty string).

For example::

    $ spasm cat.b.s "this will be read as input"
    this will be read as input
    Reached done flag
        CPU time: 215 clock cycles
        Emulator efficiency: 44.89%

Translation
-----------

``to_sphinx.py`` uses the following translation from brainfuck to Sphinx
instructions:

========= ======
Brainfuck Sphinx
========= ======
``>``     | add [dp], [dp], 1
``<``     | sub [dp], [dp], 1
``+``     | lbs [value], [dp]
          | add [value], [value], 1
          | sbs [dp], [value]
``-``     | lbs [value], [dp]
          | sub [value], [value], 1
          | sbs [dp], [value]
``.``     | lbs [value], [dp]
          | yield [value]
``,``     | lbc [value], [ip]
          | sbs [dp], [value]
          | add [ip], [ip], 1
``[``     | j end_bracket_##
          | begin_bracket_##:
          | lbs [value], [dp]
          | heq [value], 0
``]``     | j begin_bracket_##
          | end_bracket_##:
          | lbs [value], [dp]
          | hne [value], 0
========= ======

In the above table, dp is the data pointer and ip is the input pointer.

In the case where there is always a path to an infinite loop, such as in
``runner`` mode, the ``[`` and ``]`` could be rewritten so that the
label comes after the halt, which would slightly reduce the number of
cycles.  Although this is unnecessary in ``runner`` mode, it makes the
code compatible with time-travel, as used in ``forecaster`` mode.  By
putting the labels before the condition, a halt is forced if sphinx
jumps for the "wrong" reason, such as the future halt that is tested for
in ``forecaster`` mode, effectively propagating that halt backwards
through time (see `examples/halt_propagation.s <../halt_propagation.s>`_).

Brainfuck is quite nice in that ``[`` and ``]`` have complementary
conditions, so the halt propagation for ``[`` is done using the same
code that ``]`` uses for the conditional jump.


Sphinxfuck
----------
Sphinxfuck is a brainfuck-like language that uses conditional halts for
control flow just like Sphinx.  I've written a mostly probably correct
sphinxfuck interpreter in Sphinx, see
`examples/sphinxfuck.s <../sphinxfuck.s>`_

Translating brainfuck to sphinxfuck is very simple, as demonstrated by
``to_sphinxfuck.py``.


Brainfuck examples
------------------

``hello.b``, ``cat.b``, and ``cell.b`` were taken from
`the esolangs wiki page <https://esolangs.org/wiki/Brainfuck>`_.

For simplicity, I didn't implement bounds checking, so probably not all
brainfuck programs work right.
