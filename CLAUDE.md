# CLAUDE.md — feeling-map

AI assistant guidance for the `feeling-map` project.

---

## Project Overview

**feeling-map** is a pure-Python backend library that recommends nearby hobby and cultural facilities in Korean neighborhoods. It provides two core features:

1. **Shop recommendation** — filter and rank places by proximity, category, and franchise status
2. **Route recommendation** — build a sequential course through places by category type

> Korean README summary: *우리 동네의 취미,문화 생활 시설을 추천하고 기록을 남기는 서비스*

---

## Tech Stack

- **Language**: Python 3.11+
- **Dependencies**: None (pure standard library — `abc`, `enum`, `datetime`, `math`)
- **No framework**, no package manager config, no external services

---

## Repository Structure

```
feeling-map/
├── app.py                    # Main entry point (currently empty — future integration point)
├── map_facade.py             # Public API: the only class external code should call
├── domain/
│   ├── category.py           # Category enum (CAFE, FOOD, MARKET, CULTURE, LEISURE, HISTORY)
│   ├── place.py              # Abstract base class for all place types
│   └── shop_place.py         # Concrete implementation for shops, cafes, restaurants
├── recommend/
│   ├── shop_recommend.py     # Filter + rank places by distance, category, franchise
│   └── route_recommend.py    # Build a step-by-step course through place categories
├── infrastructure/           # Empty — reserved for future DB/API adapters
└── domain/test_place.py      # Manual integration test using Sejong City sample data
```

---

## Architecture

The project follows a layered Domain-Driven Design:

```
External code (app.py, tests)
        ↓
   MapFacade          ← single public entry point (facade pattern)
    /       \
ShopRecommend   RouteRecommend    ← recommendation strategies
        \       /
      Place (ABC)                 ← domain model
        ↓
    ShopPlace                     ← concrete entity
```

**Key patterns:**
- **Facade** (`MapFacade`): hides internal complexity; external code only calls `recommend_shops()` and `recommend_route()`
- **Abstract Base Class** (`Place`): enforces `get_description()` and `get_place_type()` on all concrete place types
- **Strategy** (`ShopRecommend`, `RouteRecommend`): swappable recommendation algorithms
- **Enum** (`Category`): type-safe place categorization with Korean display values

---

## Domain Model

### `Category` (enum)

| Member    | Display Value |
|-----------|--------------|
| `CAFE`    | 카페          |
| `MARKET`  | 시장          |
| `CULTURE` | 문화/예술      |
| `LEISURE` | 여가          |
| `FOOD`    | 음식점        |
| `HISTORY` | 역사/관광      |

### `Place` (abstract)

Common fields (all `_`-prefixed, exposed via `@property`):

| Property    | Type       | Notes                              |
|-------------|------------|------------------------------------|
| `place_id`  | `str`      | Unique identifier                  |
| `name`      | `str`      |                                    |
| `lat`/`lng` | `float`    | WGS-84 coordinates                 |
| `category`  | `Category` |                                    |
| `address`   | `str`      |                                    |
| `rating`    | `float`    | Mutable; validated 0.0–5.0         |

Key methods:
- `distance_to(lat, lng) -> float` — Haversine distance in km
- `get_summary() -> str` — one-line display string
- `get_description() -> str` — **abstract**, must be implemented by subclass
- `get_place_type() -> str` — **abstract**, must be implemented by subclass

### `ShopPlace(Place)`

Additional fields:

| Property       | Type       | Notes                        |
|----------------|------------|------------------------------|
| `open_time`    | `time`     |                              |
| `close_time`   | `time`     |                              |
| `phone`        | `str`      | Optional, defaults to `""`   |
| `is_franchise` | `bool`     | Used to filter local-only    |

Key method: `is_open() -> bool` — compares `datetime.now().time()` against open/close range

---

## Public API (`MapFacade`)

```python
from map_facade import MapFacade
from domain.category import Category

facade = MapFacade(places)  # pass a list[Place]

# Recommend shops sorted by rating descending
facade.recommend_shops(
    user_lat: float,
    user_lng: float,
    radius_km: float = 2.0,      # search radius
    category: Category = None,   # None = all categories
    local_only: bool = True,     # True = exclude franchises
) -> list[Place]

# Recommend a sequential route
facade.recommend_route(
    start_lat: float,
    start_lng: float,
    course: list[Category] = None,   # defaults to [FOOD, CAFE, LEISURE]
    max_step_km: float = 1.5,        # skip step if nearest place is farther than this
    local_only: bool = True,
) -> list[Place]
```

---

## Conventions

### Code Style
- Private attributes are `_`-prefixed; always expose via `@property`
- No attribute mutation from outside the class except through defined setters
- Type hints required on all method signatures (Python 3.9+ style: `list[Place]`, not `List[Place]`)
- Docstrings in Korean (domain terms) are acceptable and expected — do not translate to English
- Comments explaining non-obvious algorithms (e.g., Haversine) should be preserved

### Adding New Place Types
1. Create a new file in `domain/` (e.g., `domain/cultural_place.py`)
2. Subclass `Place` and implement `get_description()` and `get_place_type()`
3. No changes to `MapFacade` needed unless new recommendation logic is required

### Adding New Recommendation Strategies
1. Create a new file in `recommend/` implementing a `.recommend(...)` method
2. Instantiate it in `MapFacade.__init__()` and expose via a new public method

### Infrastructure Layer
`infrastructure/` is intentionally empty. Future DB adapters, API clients, or repository implementations go here. Do not put business logic there.

---

## Running the Code

```bash
# Run the manual integration test (sample data in Sejong City)
python3 -m domain.test_place
```

No build step, no install step, no test framework. All execution is direct Python.

---

## Testing

There is currently **no automated test suite**. `domain/test_place.py` is a manual integration script that:
- Creates 5 `ShopPlace` objects in Sejong City (조치원)
- Sets ratings
- Calls both `recommend_shops()` and `recommend_route()` with different parameters
- Prints results to stdout

When adding tests, prefer `pytest` placed in a `tests/` directory mirroring the module structure.

---

## Git Workflow

- Branch strategy: feature branches from `main`
- Current development branch pattern: `claude/<description>-<id>`
- Commit messages should be descriptive (see existing commits for style reference)
- Do not push directly to `main`

---

## What `app.py` Is For

`app.py` is the intended future entry point — likely a web framework integration (Flask, FastAPI, Django) or CLI. It is currently empty. When developing `app.py`, use `MapFacade` as the sole interface to domain logic.
