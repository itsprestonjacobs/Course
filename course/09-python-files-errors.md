# Python: Files & Errors

Two practical skills before Discord: reading/writing **files** (so your bot can remember
things between restarts) and handling **errors** (so one bad input doesn't crash everything).

## Reading and writing files

The safe way to work with a file is the `with` block — it opens the file and closes it for
you automatically:

```python
# Write text to a file
with open("notes.txt", "w") as f:
    f.write("Hello from Python!")

# Read it back
with open("notes.txt", "r") as f:
    content = f.read()

print(content)     # Hello from Python!
```

- `"w"` = write (overwrites the file).
- `"r"` = read.
- `"a"` = append (adds to the end).

You'll use this for ticket transcripts and simple logs.

## Saving structured data with JSON

Plain text is fine for notes, but for data like `{user: coins}` you want **JSON** — a
format that saves dictionaries and lists exactly. Python has it built in:

```python
import json

data = {"Sam": 100, "Alex": 250}

# Save
with open("coins.json", "w") as f:
    json.dump(data, f)

# Load
with open("coins.json", "r") as f:
    loaded = json.load(f)

print(loaded["Alex"])    # 250
```

This is the foundation of the data lessons later — an economy system is basically a JSON
file of everyone's coins.

## Errors — when things go wrong

When Python hits a problem it **raises an error** and stops. Try this:

```python
number = int("not a number")   # ValueError!
```

The program crashes with a `ValueError`. In a bot, one user typing something weird
shouldn't take the whole bot down. That's what `try` / `except` is for.

## try / except

```python
try:
    number = int("not a number")
    print(number)
except ValueError:
    print("That wasn't a valid number!")
```

- The code in `try` runs normally.
- If it raises the named error, the `except` block runs *instead of* crashing.

## A real bot example

Sending a DM can fail if the user has DMs turned off. We catch that specific error so the
command keeps working:

```python
try:
    await member.send("You've been warned.")
except discord.Forbidden:
    print("Couldn't DM them — their DMs are closed.")
```

`discord.Forbidden` is the error discord.py raises when the bot isn't allowed to do
something. Catching the *specific* error (not just any error) is good practice.

## Practice

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Can't divide by zero!"

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # Can't divide by zero!
```

**Challenge:** write code that tries to open a file `missing.txt` for reading and, if it
doesn't exist (`FileNotFoundError`), prints `"No file yet."`

<details><summary>Solution</summary>

```python
try:
    with open("missing.txt", "r") as f:
        print(f.read())
except FileNotFoundError:
    print("No file yet.")
```
</details>

## Recap

- `with open(path, mode) as f:` reads/writes files (`"r"`, `"w"`, `"a"`).
- **JSON** (`json.dump` / `json.load`) saves dictionaries and lists.
- `try / except SomeError:` handles errors so the bot doesn't crash.

→ **Next: Async & Await**
