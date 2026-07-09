# Python: Making Decisions

Programs make choices: *if* the user is an admin, allow the command; *otherwise*, refuse.
That's the `if` statement, and it's the beating heart of every bot.

## if / else

```python
age = 20

if age >= 18:
    print("You're an adult.")
else:
    print("You're a minor.")
```

Two things to notice:
- The line ends with a colon `:`.
- The lines underneath are **indented** (4 spaces). Indentation is how Python knows what's
  "inside" the `if`. This matters — wrong indentation is the #1 beginner error.

## Comparisons

The tests you can put after `if`:

```python
==   # equal to            (note: TWO equals signs)
!=   # not equal to
>    # greater than
<    # less than
>=   # greater than or equal
<=   # less than or equal
```

```python
score = 75
if score >= 50:
    print("Pass!")
```

> ⚠️ `=` assigns a value; `==` **compares**. `if x = 5` is an error; you want `if x == 5`.

## elif — more than two options

Use `elif` ("else if") to check several cases in order:

```python
score = 82

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")
```

Python checks top to bottom and stops at the first match.

## Combining conditions: and / or / not

```python
is_admin = True
is_banned = False

if is_admin and not is_banned:
    print("Access granted.")

if score > 100 or is_admin:
    print("Special case!")
```

- `and` — both must be true.
- `or` — at least one must be true.
- `not` — flips true/false.

This is exactly how moderation checks read: "if the user *has* permission **and** the target
*isn't* ranked above them, do it."

## Real bot flavor

Here's the kind of decision you'll write later, in plain Python:

```python
banned_words = ["spam", "scam"]
message = "this is a scam link"

if any(word in message for word in banned_words):
    print("Delete this message!")
else:
    print("Message is fine.")
```

Don't worry about `any(...)` yet — just notice it's the same `if/else` idea.

## Practice

```python
coins = 120
price = 100

if coins >= price:
    coins -= price
    print(f"Purchased! You have {coins} left.")
else:
    print("Not enough coins.")
```

**Challenge:** write an `if/elif/else` that prints `"Owner"`, `"Staff"`, or `"Member"`
based on a variable `role` equal to `"owner"`, `"staff"`, or anything else.

<details><summary>Solution</summary>

```python
role = "staff"
if role == "owner":
    print("Owner")
elif role == "staff":
    print("Staff")
else:
    print("Member")
```
</details>

## Recap

- `if / elif / else` chooses between paths; end lines with `:` and **indent** the body.
- Compare with `== != > < >= <=`.
- Combine with `and`, `or`, `not`.

→ **Next: Python — Loops**
