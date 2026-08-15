# ⚡ Async GitHub Profile Reporter CLI

A high-performance Python command-line tool that concurrently fetches, validates, and formats GitHub user profiles using asynchronous I/O and strict Pydantic schema validation.

---

## 🚀 Performance Benchmark

Tested against 5 GitHub profiles concurrently:

| Approach | Execution Time | Speedup |
| :--- | :--- | :--- |
| **Synchronous (`httpx.get`)** | ~2.77s | Baseline |
| **Asynchronous (`httpx.AsyncClient` + `asyncio.gather`)** | ~0.26s | **⚡ 10.7x Faster** |

---

## 🛠️ Architecture & Project Structure

Clean, modular separation of concerns:

```text
python-drills/
├── github_reporter/            # Core package
│   ├── __init__.py             # Package initializer
│   ├── models.py               # Pydantic schemas & field aliasing
│   ├── client.py               # Async HTTP connection pooling & error handling
│   └── printer.py              # Terminal card formatting
├── main.py                     # CLI entrypoint & argument parser
├── pyproject.toml              # Project dependencies & tool configuration
└── README.md
```

---

## ✨ Key Technical Highlights

* **Asynchronous Connection Pooling:** Reuses persistent TCP connections via `httpx.AsyncClient()` rather than creating a new client per request.
* **Concurrent Execution:** Uses `asyncio.gather(*tasks)` for parallel HTTP calls.
* **Schema Validation & Aliasing:** Implements Pydantic v2 `BaseModel` with `Field(alias="login")` and safe optional handling (`bio: str | None = None`).
* **Resilient Error Handling:** Gracefully handles `404 Not Found`, GitHub API rate limits (`403 Forbidden`), and network exceptions.
* **Strict Type Safety:** Fully typed signatures adhering to PEP 8 and `mypy` strict standards.

---

## 📦 Quickstart & Usage

### 1. Prerequisites
Ensure you have [`uv`](https://docs.astral.sh/uv/) installed (or standard Python 3.12+).

### 2. Run the CLI
Pass any number of GitHub usernames as arguments:

```bash
uv run main.py torvalds octocat tiangolo
```

### 3. Example Output

```text
Fetching Github reports for torvalds,octocat,tiangolo...

👤 torvalds (ID: 1024025)
   📦 Repos: 7 | 👥 Followers: 231400
   📝 Bio: Creator of Linux and Git
-------------------------------------------------------
👤 octocat (ID: 583231)
   📦 Repos: 8 | 👥 Followers: 17200
   📝 Bio: There once was a coder named Octocat...
-------------------------------------------------------
👤 tiangolo (ID: 1326112)
   📦 Repos: 28 | 👥 Followers: 82100
   📝 Bio: Creator of FastAPI, Typer, SQLModel
-------------------------------------------------------
```

---

## 🧰 Tech Stack

* **Language:** Python 3.12+
* **Async Engine:** `asyncio` + `httpx`
* **Data Validation:** `Pydantic v2`
* **Package Manager:** `uv`
