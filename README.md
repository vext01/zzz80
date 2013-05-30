# zzz80

A slow interpreter for an simple imaginary CPU.

The end goal is to JIT this with pypy.

## Architecture

### Registers

- Eight registers: r0, ..., r8.
- r0 is the program counter.
- By convention, r1 is the return register.

### Stack

- Unbounded dynamically sized stack.
- Every stack element is of size 1 regardless of contents.
- CALL/RET use the stack like most CPU architectures.
- By convention, function args go on the stack like in x86.

Note that there is no memory other than the stack.

Note also that, unlike most CPU architectures, the program code is not
accessible from the user program.

### Instructions

See OPTAB in opcodes.py. The purpose of most should be obvious.  Not so
obvious are the following operations:

- DROP: simply POPs, discarding the value.
- PICK rx, const: An idea borrowed from reverse polish lisp. Loads rx
  with the stack item 'const' from the top of the stack. The stack is
  untouched.
- PT rx: Print the value held in rx.
- DUMP: Dumps the interpreter state to stderr.

## Tests

A [Fibonacci program](examples/fib.zzz) is provided as a test. Run
test.py to exercise this.

## Deliberately Questionable Design Choices

I have dropped in some clangers to see how PyPy responds. It will be
interesting to see how PyPy fares with the following obstacles:

- Operand types checked at runtime during interpretation. This widens the scope of possible traces.
- The stack is both dynamic (size) and unbounded. According to
  [this](http://tratt.net/laurie/tech_articles/articles/fast_enough_vms_in_fast_enough_time),
  PyPy may find this challenging.
- The majority of runtime is interpretation of calling convention. Args
  go on the stack, will PyPy be able to optimise this? If so, this is a
great result.
- Labels are held in a dictionary and resolved at runtime. This again,
  should diversify traces.
