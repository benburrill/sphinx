==========
Sphinx ISA
==========
Sphinx is an instruction set architecture intended for low-power
embedded hypercomputers, which relies only on a Turing jump instruction
(along with an assortment of conditional halt instructions) for control
flow.

This repository houses a working Sphinx emulator written in Python and
aims also to provide an official specification for the architecture.

Emulator
========
``spasm``, the Sphinx assembler/emulator, requires a recent version of
Python, I think >= 3.10.  I use Python 3.11.

It has no other dependencies and can be run directly without
installation.  To run the countdown example:

.. code::

    $ python3 -m spasm examples/countdown.s

Alternatively, you may install the ``spasm`` executable:

.. code::

    $ pip3 install --editable .
    $ spasm examples/countdown.s

**NOTE:**
Due to the unfortunate limitations of traditional processors, the
emulator may require an exponential amount of memory and time to perform
jump instructions in some cases, based on the amount of state.  On a
true Sphinx architecture, the jump instruction is specified to take one
clock cycle.

Instructions
============

Arguments to most instructions in Sphinx can be any of the following
forms::

    ARG = IMMED | [IMMED] | {IMMED}

- IMMED - immediate values.  These can be any assembly-time expression
  using labels and numeric literals.  For example: ``8``, ``my_label``,
  or ``('B' + 3) * 2``.
- [IMMED] - state values.  The immediate value within the square
  brackets is used as an address to look up a value in the state section
  (main memory) at runtime.  State values take the place of registers in
  a normal assembly language, but are backed by memory.  For example:
  ``[my_label]``, or ``[arr + 5w]``
- {IMMED} - const values.  They are just like state values, but look up
  values in the (read-only) const section instead, which usually holds
  the inputs to the program.  For example: ``{input_number}``

Sphinx follows the convention of placing the destination first, eg
``mov [dest], [source]``

Instructions are allowed in the code section only.

===================================================== ======================= ==========================================================
Instructions                                          Syntax                  Description
===================================================== ======================= ==========================================================
halt                                                  halt                    Unconditional halt
heq, hne, hlt, hgt, hle, hge, hltu, hgtu, hleu, hgeu  heq ARG, ARG            Conditional halt.  Compares the arguments and halts if the
                                                                              condition is met.  Unsigned comparisons have the suffix u.
j                                                     j ARG                   `Turing jump <https://en.wikipedia.org/wiki/Turing_jump>`_.
                                                                              Jumps to the specified address if not jumping would lead to
                                                                              halting.
add, sub, mul, div, mod, and, or, xor, asl, asr       add [IMMED], ARG, ARG   Arithmetic instructions, outputting to the given address
                                                                              in state.
mov                                                   mov [IMMED], ARG        Set the word at the output address.
lws, lwc, lbs, lbc                                    lws [IMMED], ARG        Set the word at the output address to the value loaded
                                                                              from the word or byte at the address specified by the
                                                                              other argument.
lwso, lwco, lbso, lbco                                lwso [IMMED], ARG, ARG  Like the previous, but with an additional offset argument
sws, sbs                                              sws ARG, ARG            Store the value (word or byte) specified by the second
                                                                              argument into the word of state at address specified by
                                                                              the first.
swso, sbso                                            swso ARG, ARG, ARG      Again, adds an offset.  Note that the offset is given by
                                                                              the second argument, not the third one (since it is
                                                                              offsetting the first argument).
yield                                                 yield ARG               Outputs the argument to the output stream.  See also the 
                                                                              ``%format output`` preprocessor command.
sleep                                                 sleep ARG               Sleep for the given number of milliseconds.
flag                                                  flag IDENTIFIER         Indicates program status.  The identifier can be anything,
                                                                              though some identifiers have somewhat special meaning.
                                                                              ``flag done`` is typically used to indicate successful
                                                                              non-termination.
===================================================== ======================= ==========================================================


Data directives
===============
Allowed in the state and const sections

- ``.ascii "STRING"``
- ``.asciiz "STRING"`` - Null-terminated string
- ``.asciip "STRING"`` - String prefixed with a word holding length of string in bytes
- ``.word IMMED``
- ``.byte IMMED``
- ``.fill IMMED, IMMED`` - Fill given number of bytes with first value
- ``.zero IMMED`` - Fill given number of bytes with zeros
- ``.arg IDENT (ascii | asciiz | asciip | word | byte)`` - See section on command-line arguments

Preprocessor commands
=====================

- ``%section code | state | const`` - change the section
- ``%format word NUMBER | inf`` - set the word size in bytes, or ``inf``
  for infinite words which can represent any integer.  Default: 2
- ``%format output signed | unsigned | byte`` - set output format of the
  ``yield`` instruction.  ``byte`` mode will write the lower byte of the
  word to stdout.  Default: signed
- ``%argv`` -- See section on command-line arguments

How does it work?
=================
Time travel.  Oh you mean the emulator?  There's no magic to it.
Relevant code can be in `spasm/program.py <https://github.com/benburrill/sphinx/blob/24e80ef39aaae1f9aff020a275baea03b64285cc/spasm/program.py#L291-L367>`_.
It works kinda like a depth-first search in the tree of possible paths
of execution.  Since we have finitely bounded state, the *only* way not
to halt is for there to be a repeating loop.  So at a jump point, we're
recursively searching for a path with a repeated state.  Failing that,
ie when halting would be inevitable, we jump.

More theoretically, Sphinx's halting problem isn't undecidable because
it isn't Turing complete - it *requires* finitely bounded state in order
to work, and cannot be generalized to an unbounded version (though I
haven't let that stop me from adding ``%format word inf``).  Although
Sphinx's execution depends intimately on its own halting problem (which
is seemingly problematic regardless of the fact it has finite state),
Sphinx's freedom to act on this information for itself is limited.
Sphinx can't test if something will halt without committing to run it if
it won't.

SIGBOVIK
========
A paper introducing the Sphinx instruction set was accepted into the
proceedings of `The Association for Computational Heresy <https://sigbovik.org/>`_.

Burrill, Ben 2023.
"A Halt-Averse Instruction Set Architecture for Embedded Hypercomputers".
In *A Record of the Proceedings of SIGBOVIK 2023*.
The Association for Computational Heresy, p. 150.

Command-line arguments
======================
Sphinx assembly has support for specifying the inputs that an assembly
program requires.  These may be passed on the command-line to ``spasm``.

There's no clear "correct" way for arguments to be treated (eg should
they be in ``state`` or ``const``, where, and with what format?), and
any specific way that would be convenient for me in implementing Halt is
Defeat seemed too specific, so Sphinx provides a lot of flexibility.

The arguments are defined using the ``%argv`` command in a manner
similar to (but only a tiny subset of) docopt:

- ``<IDENT>`` defines a named argument
- ``ARG...`` means 1 or more
- ``[ARG]`` means optional

For example: ``%argv <x> [<y>...]`` specifies that the program expects
an argument <x> followed by 0 or more arguments <y>.

Once the argument variables are defined with ``%argv``, you get to
choose where and how the arguments should be placed into memory using
the ``.arg`` data directive.

``.arg x asciiz`` directs <x> to placed into memory as a null-terminated
string.

``.arg y word`` directs <y> to be parsed as a decimal integer and placed
into memory as words.  Since we specified 0 or more arguments as <y>,
all of the arguments passed will be parsed and placed at increasing
addresses in memory.

If you want multiple strings associated with a single argument variable,
you may want to have an array of pointers to those strings.  This may be
done with the ``array`` specifier, eg ``.arg y asciiz array``.

If there were no arguments passed as y, this array will still include a
dummy entry pointing to the next address in memory.  This shouldn't be
considered as "part" of the array, but it may be useful for iterating
over it.

Additionally for plain ``ascii`` (not ``asciiz`` or ``asciip``):

- The ``array`` will always have an extra entry pointing to the end (so
  an empty array has 2 identical entries)
- If there's no ``array``, multiple arguments will be separated by
  single spaces.

There is no direct way to determine how many arguments were passed for
each argument variable.  However, there is a special assembly-time
variable ``$argc`` which gives the total number of arguments passed.
From this, you can infer the number of arguments associated with each
argument variable.  Alternatively, you may place a label at the end of
an argument directive and iterate through until the label is reached.
