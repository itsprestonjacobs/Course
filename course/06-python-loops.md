# Python: Loops

A **loop** repeats code. Instead of writing the same line 100 times, you write it once and
tell Python to run it for each item. Bots loop constantly — over every member, every
message in a channel, every option in a menu.

## The for loop

`for` runs a block once for each item in a collection:

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I like {fruit}")
```

`fruit` is a temporary variable that becomes each item in turn. Like `if`, the body is
**indented**.

## Looping a set number of times: range()

`range(n)` gives you the numbers `0` to `n-1`:

```python
for i in range(5):
    print(i)        # 0 1 2 3 4

for i in range(1, 4):
    print(i)        # 1 2 3
```

## Looping through a dictionary

```python
scores = {"Sam": 10, "Alex": 25}

for name, points in scores.items():
    print(f"{name} has {points} points")
```

## Building up a result

A common pattern: start empty, add to it each loop:

```python
names = ["Sam", "Alex", "Jordan"]
total_letters = 0

for name in names:
    total_letters += len(name)

print(total_letters)    # 13
```

That's exactly how a ticket **transcript** is built — loop through each message and glue
them together into one big string.

## The while loop

`while` repeats *as long as* a condition stays true:

```python
count = 3
while count > 0:
    print(count)
    count -= 1
print("Go!")
```

> ⚠️ Make sure the condition eventually becomes false (here, `count` keeps shrinking). If it
> never does, you get an **infinite loop** and the program hangs. `for` loops don't have
> this risk, so prefer them when you can.

## break and continue

```python
for number in range(10):
    if number == 5:
        break        # stop the loop entirely
    if number % 2 == 0:
        continue     # skip to the next item
    print(number)    # 1 3
```

## Practice

```python
banned = ["spam", "scam", "free nitro"]
message = "click here for free nitro"

for word in banned:
    if word in message:
        print(f"Blocked because of: {word}")
        break
```

**Challenge:** loop through `range(1, 11)` and print only the even numbers. (Hint: `% 2`.)

<details><summary>Solution</summary>

```python
for n in range(1, 11):
    if n % 2 == 0:
        print(n)
```
</details>

## Recap

- `for item in collection:` repeats once per item.
- `range(n)` loops a fixed number of times.
- `.items()` loops a dictionary's keys and values.
- `while` loops until a condition is false; watch for infinite loops.
- `break` stops; `continue` skips.

→ **Next: Python — Functions**
