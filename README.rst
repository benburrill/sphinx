Sphinx ISA
==========

Emulator
--------
``spasm``, the Sphinx assembler/emulator, requires a recent version of
Python, I think >= 3.10.  I use Python 3.11.

To run the prime loop example: ``python3.11 -m spasm examples/prime_loop.s``

Alternatively, you may install the ``spasm`` executable:

.. code:: sh

    $ pip3.11 install --editable .
    $ spasm examples/prime_loop.s

**NOTE:**
Due to the unfortunate limitations of traditional processors, the
emulator may require an exponential amount of memory and time to perform
jump instructions in some cases, based on the amount of state.  On a
true Sphinx architecture, the jump instruction is specified to take one
clock cycle.

Instructions
------------

Arguments to most instructions in Sphinx can be any of the following
forms::

    ARG ::= IMMED | [IMMED] | {IMMED}

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

Instructions are allowed in the code section only.

================================================ ======================= ==========================================================
Instructions                                     Syntax                  Description
================================================ ======================= ==========================================================
halt                                             halt                    Unconditional halt
heq, hne, hlt, hgt, hle, hge                     heq ARG, ARG            Conditional halt.  Compares the arguments and halts if the
                                                                         condition is met.
j                                                j ARG                   Jump to the specified address if not jumping would lead to
                                                                         halting.
add, sub, mul, div, mod, and, or, xor, asl, asr  add [IMMED], ARG, ARG   Arithmetic instructions, outputting to the given address
                                                                         in state.
mov                                              mov [IMMED], ARG        Set the word at the output address.
lws, lwc, lbs, lbc                               lws [IMMED], ARG        Set the word at the output address to the value loaded
                                                                         from the word or byte at the address specified by the
                                                                         other argument.
lwso, lwco, lbso, lbco                           lwso [IMMED], ARG, ARG  Like the previous, but with an additional offset argument
sws, sbs                                         sws ARG, ARG            Store the value (word or byte) specified by the second
                                                                         argument into the word of state at address specified by
                                                                         the first.
swso, sbso                                       swso ARG, ARG, ARG      Again, adds an offset.  Note that the offset is given by
                                                                         the second argument, not the third one (since it is
                                                                         offsetting the first argument).
yield                                            yield ARG               Outputs the argument to the output stream.  See also the 
                                                                         ``%format output`` preprocessor command.
sleep                                            sleep ARG               Sleep for the given number of milliseconds.
flag                                             flag IDENTIFIER         Indicates program status.  The identifier can be anything,
                                                                         though some identifiers have somewhat special meaning.
                                                                         ``flag done`` is used to indicate to the user that the
                                                                         primary computational task is finished and that the
                                                                         program is about to enter terminal non-termination.
================================================ ======================= ==========================================================


Data directives
---------------
Allowed in the state and const sections

- ``.ascii "STRING"``
- ``.asciiz "STRING"``
- ``.word IMMED``
- ``.byte IMMED``
- ``.fill IMMED, IMMED`` - Fill given number of bytes with first value
- ``.zero IMMED`` - Fill given number of bytes with zeros


Preprocessor commands
---------------------

- ``%section code | state | const`` - change the section
- ``%format word NUMBER | inf`` - set the word size in bytes, or ``inf``
  for infinite words which can represent any integer.  Default: 2
- ``%format output signed | unsigned | byte`` - set output format of the
  ``yield`` instruction.  ``byte`` mode will write the lower byte of the
  word to stdout.  Default: signed
