# zzz80

An imaginary assembler language jitted with RPython.

## Architecture

### Registers

- Eight registers: r0, ..., r8.
- r0 is the program counter.
- By convention, r1 is the return register.

### Stack

- Bounded-size stack (for performance reasons).
- Every stack element is of size 1 regardless of contents.
- CALL/RET use the stack like most CPU architectures.
- By convention, function args go on the stack like in x86.
- The only way to read memory is to use POP or PICK. There are no
  addressing modes per se. Every memory read or write is relative to
  the stack top.

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
