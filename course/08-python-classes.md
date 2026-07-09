# Python: Classes & Objects

This is the last big Python idea before we touch Discord — and it's the one that makes
discord.py click. Don't worry if it feels abstract; you'll see it pay off immediately.

## Objects — values that carry data *and* actions

You've already used objects without knowing it. A string is an object:

```python
name = "derpy"
print(name.upper())     # DERPY
```

`name` holds data ("derpy") **and** knows how to do things (`.upper()`). Those attached
actions are called **methods** (functions that belong to an object).

In discord.py, *everything* is an object: a `member` object has `.name` and `.kick()`, a
`channel` object has `.send()`. Learning classes is learning how those are built.

## A class is a blueprint

A **class** describes what a kind of object looks like. Here's a simple one:

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name} says woof!")
```

- `__init__` runs when you **create** an object — it sets up its data.
- `self` means "this particular object." `self.name` is *this dog's* name.
- `bark` is a **method** — a function that belongs to the dog.

## Creating and using objects

```python
rex = Dog("Rex", 3)
buddy = Dog("Buddy", 5)

print(rex.name)     # Rex
print(buddy.age)    # 5
rex.bark()          # Rex says woof!
```

Each `Dog(...)` makes a separate object with its own data. `rex` and `buddy` don't
interfere.

## Why this matters: cogs and views are classes

You will write two kinds of classes in this course, and now you'll recognize them:

```python
class Moderation(commands.Cog):     # a "cog" — groups related commands
    def __init__(self, bot):
        self.bot = bot

class CloseButton(discord.ui.View):  # a "view" — holds buttons
    ...
```

`commands.Cog` and `discord.ui.View` are classes made by discord.py. When you write
`class Moderation(commands.Cog)`, you're saying "make a new class that **builds on** theirs"
— that's called **inheritance**, and it's how you get all their powers for free.

You don't need to master classes to use them. You mostly fill in the blanks: an
`__init__`, a few methods, and `self` to reach your object's data.

## Practice

```python
class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def show(self):
        print(f"{self.owner} has {self.balance} coins")

acc = BankAccount("Sam")
acc.deposit(100)
acc.deposit(50)
acc.show()      # Sam has 150 coins
```

**Challenge:** add a `withdraw(amount)` method that subtracts from the balance, then
withdraw 30 and show the result.

<details><summary>Solution</summary>

```python
    def withdraw(self, amount):
        self.balance -= amount

acc.withdraw(30)
acc.show()      # Sam has 120 coins
```
</details>

## Recap

- An **object** bundles data (attributes) with actions (**methods**).
- A **class** is the blueprint; `__init__` sets up each new object; `self` is "this object."
- **Inheritance** (`class X(Base)`) builds on an existing class — exactly how cogs and views
  work in discord.py.

→ **Next: Python — Files & Errors**
