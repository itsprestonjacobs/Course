# Python: Variables & Types

Now we learn Python itself, from zero. Make a file called `practice.py` in your project and
run each snippet with `python practice.py`. Typing the examples yourself — not just reading
— is how this sticks.

## print() — showing things

`print()` displays text in the terminal:

```python
print("Hello, world!")
```

## Variables — labeled boxes

A **variable** stores a value under a name so you can use it later:

```python
name = "Derpy"
age = 3
print(name)
print(age)
```

Read `=` as "gets set to." `name` gets set to `"Derpy"`.

## The basic types

Python values come in a few flavors. The main ones:

```python
text = "hello"        # str  — text, always in quotes
number = 42           # int  — a whole number
price = 3.99          # float — a number with a decimal
is_online = True      # bool — either True or False
nothing = None        # None — "no value yet"
```

You can check a value's type with `type()`:

```python
print(type(42))       # <class 'int'>
print(type("hi"))     # <class 'str'>
```

## Working with text (strings)

Strings can be joined and measured:

```python
first = "Derpy"
last = "Designs"
print(first + " " + last)   # Derpy Designs
print(len(first))           # 5  (number of characters)
print(first.upper())        # DERPY
print(first.lower())        # derpy
```

## f-strings — the clean way to build text

Put an `f` before the quotes, then drop variables straight in with `{ }`:

```python
name = "Derpy"
age = 3
print(f"{name} is {age} years old")   # Derpy is 3 years old
```

f-strings are everywhere in bot code — for example naming a channel `f"ticket-{user_id}"`.
Get comfortable with them now.

## Numbers and math

```python
print(5 + 3)     # 8
print(10 - 4)    # 6
print(6 * 7)     # 42
print(10 / 3)    # 3.333...
print(10 // 3)   # 3   (whole-number division)
print(10 % 3)    # 1   (remainder — great for "every Nth time")
```

## Changing a variable

A variable can be updated:

```python
score = 10
score = score + 5
print(score)     # 15

score += 5       # shortcut for "score = score + 5"
print(score)     # 20
```

## Practice

Try to predict the output, then run it:

```python
xp = 100
level = 2
print(f"You have {xp} XP and are level {level}.")
xp += 50
print(f"After the boost: {xp} XP")
```

**Challenge:** make a variable `username`, then print
`Welcome, <username>! Your name is <N> letters long.` using an f-string and `len()`.

<details><summary>Solution</summary>

```python
username = "Sam"
print(f"Welcome, {username}! Your name is {len(username)} letters long.")
```
</details>

## Recap

- **Variables** store values; `=` assigns.
- Types: **str, int, float, bool, None**.
- **f-strings** (`f"{name}"`) build text cleanly.
- `+=` updates a variable in place.

→ **Next: Python — Lists & Dictionaries**
