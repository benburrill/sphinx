Brainfuck to Sphinx
===================

``to_sphinx.py`` translates brainfuck to Sphinx with a fixed input.

There are two modes:

The ``runner`` mode is a direct translation, where termination of the
brainfuck program translates into a done flag followed by terminal
non-termination in Sphinx.

Based on examples/halting.s, we should be able to transform any halting
brainfuck program into a halting Sphinx program without it halting too
early, but it's easier just to use terminal non-termination to deal with
this problem.

The ``forecaster`` mode produces a sphinx program which "immediately"
outputs a flag to the user indicating whether the brainfuck program
would halt, and then a done flag before entering an infinite loop.  This
is a bit of a trick -- in the case that the brainfuck code will not halt
this infinite loop is not the usual terminal non-termination that often
follows a done flag, it's just running the brainfuck program with output
suppressed.  In the other case, it doesn't need to enter an infinite
loop at all, and just does so for consistency.

Usage::

    $ python to_sphinx.py MODE BF_FILE [INPUT [DATA_SIZE]] > SPHINX_FILE

Where MODE is either ``runner`` or ``forecaster``, BF_FILE is the
brainfuck source file, INPUT is the fixed input string read by ``,``
(default: empty string) and DATA_SIZE is the number of bytes of data
(default 1000).


Translation
-----------

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
In the case where there is always a path to an infinite loop, eg in
``runner`` mode, the ``[`` and ``]`` could be rewritten so that the
label comes after the halt, which would slightly reduce the number of
cycles.  By putting the labels before the condition, a halt is forced if
sphinx jumps for the "wrong" reason due to a future halt (as in
``forecaster`` mode).  This allows halts to be propagated upward.

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
