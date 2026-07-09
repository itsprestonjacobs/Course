# Databases with SQLite

JSON is great for small data. But when you have thousands of records, or need to ask
questions like "who are the top 10 richest members?", a **database** is the right tool.
**SQLite** is a database built right into Python — no server to install, just a file.

## What a database gives you

- **Tables** — like spreadsheets: rows and columns.
- **Speed** — it can search and sort huge amounts of data instantly.
- **Safety** — it handles many changes at once without corrupting the file.

We'll build the storage layer for an economy system: a table of users and their coins.

## The three things you'll do

Talking to SQLite is always the same shape: **connect**, run a **query**, **commit** if you
changed something.

```python
import sqlite3

conn = sqlite3.connect("economy.db")
cursor = conn.cursor()

# Create a table (only needs to happen once; "IF NOT EXISTS" makes it safe to re-run)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS balances (
        user_id INTEGER PRIMARY KEY,
        coins INTEGER DEFAULT 0
    )
""")
conn.commit()
```

`CREATE TABLE` defines the columns. `user_id` is the **primary key** (unique per user);
`coins` defaults to 0.

## The four core operations

SQL is the language you use. You only need four commands to start:

```python
# INSERT — add a new row
cursor.execute("INSERT OR IGNORE INTO balances (user_id) VALUES (?)", (user_id,))

# SELECT — read data
cursor.execute("SELECT coins FROM balances WHERE user_id = ?", (user_id,))
row = cursor.fetchone()          # one row, e.g. (100,)  — or None if not found

# UPDATE — change a row
cursor.execute("UPDATE balances SET coins = coins + ? WHERE user_id = ?", (50, user_id))

# ...and always commit changes:
conn.commit()
```

> 🔒 See the `?` placeholders? **Always** pass values as that second tuple, never by
> building the string yourself with f-strings. It's safer (prevents "SQL injection") and
> handles types for you. This is the one SQL habit to lock in early.

## A clean data layer

Wrap it in a small helper file, `db.py`, so your cogs stay tidy:

```python
import sqlite3

conn = sqlite3.connect("economy.db")
conn.execute("CREATE TABLE IF NOT EXISTS balances (user_id INTEGER PRIMARY KEY, coins INTEGER DEFAULT 0)")
conn.commit()

def get_coins(user_id):
    row = conn.execute("SELECT coins FROM balances WHERE user_id = ?", (user_id,)).fetchone()
    return row[0] if row else 0

def add_coins(user_id, amount):
    conn.execute("INSERT OR IGNORE INTO balances (user_id) VALUES (?)", (user_id,))
    conn.execute("UPDATE balances SET coins = coins + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()

def top_users(limit=10):
    return conn.execute(
        "SELECT user_id, coins FROM balances ORDER BY coins DESC LIMIT ?", (limit,)
    ).fetchall()
```

Now a cog just calls `db.get_coins(id)` or `db.add_coins(id, 50)` — no SQL in sight.

## Using it in a command

```python
import db

    @app_commands.command(description="Check your coins.")
    async def balance(self, interaction: discord.Interaction):
        coins = db.get_coins(interaction.user.id)
        await interaction.response.send_message(f"💰 You have **{coins}** coins.")
```

`top_users()` is the payoff — a leaderboard, sorted by coins, in one query. Try doing *that*
efficiently with a JSON file and you'll appreciate databases.

## JSON or SQLite — which should I use?

| Use JSON when… | Use SQLite when… |
|----------------|------------------|
| a few hundred records | thousands+ of records |
| simple settings/config | you need sorting/searching (leaderboards!) |
| you're just starting out | data changes constantly from many places |

Both are valid. Start with whichever feels comfortable; you can always migrate later.

## Practice

**Challenge:** add a `remove_coins(user_id, amount)` function to `db.py` that subtracts coins
(don't let it go below zero — hint: `MAX(0, coins - ?)` won't work simply; instead check the
balance first in Python).

<details><summary>Solution</summary>

```python
def remove_coins(user_id, amount):
    current = get_coins(user_id)
    new = max(0, current - amount)
    conn.execute("INSERT OR IGNORE INTO balances (user_id) VALUES (?)", (user_id,))
    conn.execute("UPDATE balances SET coins = ? WHERE user_id = ?", (new, user_id))
    conn.commit()
```
</details>

## Recap

- **SQLite** is a file-based database built into Python (`import sqlite3`).
- Pattern: **connect → execute a query → commit** (for changes).
- Use `?` placeholders for values — never f-strings — for safety.
- Wrap SQL in a `db.py` helper; databases shine for leaderboards and lots of data.

→ **Next: Per-Server Settings**
