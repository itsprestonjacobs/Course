# Python: Functions

A **function** is a named, reusable chunk of code. You write it once and "call" it whenever
you need it. Every command your bot runs is a function, so this lesson is a big one.

## Defining and calling

```python
def greet():
    print("Hello!")

greet()      # Hello!
greet()      # Hello!  — call it as many times as you want
```

- `def` starts a function definition.
- `greet` is the name.
- The indented body runs when you **call** it with `greet()`.

## Arguments — giving a function input

The values in the parentheses are **arguments** (or parameters). They let the same function
work with different data:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Sam")     # Hello, Sam!
greet("Alex")    # Hello, Alex!
```

Multiple arguments, separated by commas:

```python
def add(a, b):
    print(a + b)

add(3, 4)    # 7
```

## Returning a value

`print` shows something; `return` hands a value *back* so you can store or reuse it. Big
difference — this trips up beginners.

```python
def add(a, b):
    return a + b

result = add(3, 4)
print(result)          # 7
print(add(10, 5))      # 15
```

A function that `return`s can be used inside other expressions. A function that only
`print`s just shows text and gives back `None`.

## Default values

Give an argument a fallback so it's optional:

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Sam")                 # Hello, Sam!
greet("Sam", "Welcome")      # Welcome, Sam!
```

You'll see this in commands like `async def kick(member, reason=None)` — `reason` is
optional.

## Why functions matter for bots

A slash command *is* a function. When someone runs `/ban`, discord.py calls your `ban`
function and hands it the details (who, why) as arguments:

```python
def ban(member, reason):
    print(f"Banning {member} for: {reason}")

ban("Spammer#0001", "posting scams")
```

Helper functions also keep code DRY (Don't Repeat Yourself). Instead of building the same
embed in five commands, you write one `make_embed()` function and call it five times.

## Practice

```python
def price_after_tax(price, tax=0.1):
    return price + (price * tax)

print(price_after_tax(100))        # 110.0
print(price_after_tax(100, 0.2))   # 120.0
```

**Challenge:** write a function `is_rich(coins)` that returns `True` if `coins` is 1000 or
more, otherwise `False`. Then print `is_rich(1500)`.

<details><summary>Solution</summary>

```python
def is_rich(coins):
    return coins >= 1000

print(is_rich(1500))   # True
```
</details>

## Recap

- `def name(args):` defines a function; `name(...)` calls it.
- **Arguments** are inputs; **default values** make them optional.
- `return` hands a value back (different from `print`).
- Slash commands are just functions discord.py calls for you.

→ **Next: Python — Classes & Objects**
