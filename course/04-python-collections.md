# Python: Lists & Dictionaries

Single variables hold one value. Real programs juggle *collections* of values — a list of
members, a mapping of user → score. These two structures show up constantly in bot code.

## Lists — an ordered row of values

A **list** holds many values in order, written with square brackets:

```python
fruits = ["apple", "banana", "cherry"]
print(fruits[0])     # apple  (counting starts at 0!)
print(fruits[1])     # banana
print(len(fruits))   # 3
```

The `[0]` is an **index**. The first item is `0`, the second is `1`, and so on.

### Changing a list

```python
fruits.append("orange")    # add to the end
fruits.remove("banana")    # remove by value
print(fruits)              # ['apple', 'cherry', 'orange']
print("apple" in fruits)   # True  — is it in there?
```

`in` is super handy — we'll use it for things like "is this word in the banned-words list?"

## Dictionaries — labeled values (key → value)

A **dictionary** stores values under names (keys) instead of positions. Written with curly
braces:

```python
user = {
    "name": "Robin",
    "level": 5,
    "coins": 200,
}

print(user["name"])    # Robin
print(user["level"])   # 5
```

### Changing a dictionary

```python
user["coins"] = 250          # update a value
user["badge"] = "VIP"        # add a new key
print(user)
print("badge" in user)       # True
```

Dictionaries are how bots remember things: `warnings = {user_id: 3}` means "this user has 3
warnings." An economy system is basically one big dictionary of `user → coins`.

## Looping through collections (preview)

You'll learn loops properly soon, but here's the shape:

```python
for fruit in fruits:
    print(fruit)

for key, value in user.items():
    print(f"{key} = {value}")
```

## Getting a value safely

If you ask a dictionary for a missing key, it errors. `.get()` avoids that by giving a
fallback:

```python
print(user.get("coins", 0))    # 250
print(user.get("gems", 0))     # 0  — "gems" doesn't exist, so we get the default
```

We'll lean on `.get()` a lot so the bot doesn't crash on new users.

## Practice

```python
scores = {"Sam": 10, "Alex": 25}
scores["Jordan"] = 15
scores["Sam"] += 5
print(scores)
print(scores.get("Taylor", 0))
```

**Challenge:** make a list called `staff` with three names, add a fourth with `.append()`,
and print `True`/`False` for whether `"Admin"` is in the list.

<details><summary>Solution</summary>

```python
staff = ["Sam", "Alex", "Jordan"]
staff.append("Taylor")
print("Admin" in staff)   # False
```
</details>

## Recap

- **Lists** `[...]` hold ordered values; access by index `[0]`; `.append()`, `.remove()`,
  and `in`.
- **Dictionaries** `{key: value}` map names to values; `.get(key, default)` is the safe way
  to read.
- Both are how a bot **remembers** data.

→ **Next: Python — Making Decisions**
