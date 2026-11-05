# TODO

## Milestone plan (ordered)

### M0 — Baseline + safety net
**Goal:** freeze current behavior before refactor.

- Add/expand tests for current behavior in:
  - [Dice_test.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Dice_test.py)
  - [Alignment_test.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Alignment_test.py)
  - [Action_test.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Action_test.py) (currently minimal)
- Update runner in [runtests](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/runtests) to include all active tests.
- Add a “known limitations” section in [README.md](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/README.md).

- [x] **Done when:** tests pass and capture expected behavior.

---

### M1 — Package structure + clean imports
**Goal:** make project installable and modular.

Create package folders:

- `alchemy_py/models/`
- `alchemy_py/types/`
- `alchemy_py/client/`
- `alchemy_py/services/`
- `alchemy_py/schemas/`
- `alchemy_py/errors/`

Move/refactor current modules:
- [AbilityScore.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/AbilityScore.py) → `alchemy_py/models/ability_score.py`
- [Dice.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Dice.py) → `alchemy_py/models/dice.py`
- [Alignment.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Alignment.py) → `alchemy_py/models/alignment.py`
- [SavingThrow.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/SavingThrow.py) → `alchemy_py/models/saving_throw.py`
- [Action.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Action.py) → `alchemy_py/models/action.py`
- [Character.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Character.py) → `alchemy_py/models/character.py`

- [x] **Done when:** imports are package-relative and tests still pass.

---

### M2 — Domain model hardening
**Goal:** robust, typed, immutable-ish core models.

- Convert core models to dataclasses.
- Fix known model issues (duplicate constructors, tuple enum values, mutable class defaults).
- Keep models API-agnostic (no HTTP/JSON assumptions inside model logic).

- [x] **Done when:** model tests pass and constructors are consistent/typed.

---

### M3 — API schema mapping layer
**Goal:** isolate Alchemy JSON format from model internals.

Add:
- `alchemy_py/schemas/character_import.py` (to_api/from_api mapping)
- Optional schema validators for required payload fields.

Use docs payload shape as contract source (from the Character Import section you shared).

- [x] **Done when:** round-trip tests pass (`model -> json -> model` where applicable).

---

### M4 — Client + services layer
**Goal:** clean public API for users.

Add:
- `alchemy_py/client/http_client.py` (session/auth/timeout/retry hooks)
- `alchemy_py/services/character_service.py` (e.g. import payload helpers)
- `alchemy_py/errors/*.py` for typed exceptions.

Keep first release small: one stable service path (character import workflow).

- [x] **Done when:** user can call one high-level API entrypoint without touching raw JSON.

---

### M5 — Docs + public API stabilization
**Goal:** make library usable by others.

- Rewrite [README.md](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/README.md):
  - install
  - quickstart
  - model example
  - service usage
  - error handling
- Add `alchemy_py/__init__.py` exports for stable public surface.

- [ ] **Done when:** README quickstart works end-to-end.

---

## File-by-file migration checklist

- [Constants.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Constants.py)  
  - [ ] Move constants/enums into `alchemy_py/types/`  
  - [ ] Remove magic-string duplication across models

- [Dice.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Dice.py)  
  - [ ] Replace dual `__init__` with single validated constructor + parse classmethod  
  - [ ] Keep deterministic roll testability

- [Alignment.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Alignment.py)  
  - [ ] Fix enum values (remove accidental tuple values)  
  - [ ] Keep `__str__` contract tested

- [AbilityScore.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/AbilityScore.py)  
  - [ ] Convert to dataclass  
  - [ ] Add optional validation (name/value bounds)

- [SavingThrow.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/SavingThrow.py)  
  - [ ] Convert to dataclass  
  - [ ] Validate DC bounds/type

- [Action.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Action.py)  
  - [ ] Split into smaller model classes if needed (`action_step.py` etc.)  
  - [ ] Remove mutable defaults  
  - [ ] Replace fragile runtime type checks with dataclass typing + focused validators

- [Character.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Character.py)  
  - [ ] Implement real dataclass model (currently partial annotations)  
  - [ ] Normalize HP/trackers/actions composition

- [Action_test.py](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/Action_test.py)  
  - [ ] Add constructor/validation tests  
  - [ ] Add serialization contract tests

- [README.md](C:/Users/jaded/Documents/Workspace/Python3/Alchemy-py/README.md)  
  - [ ] Update architecture and usage docs after each milestone

---

## Suggested execution cadence

- **PR 1:** M0 + M1  
- **PR 2:** M2 (model hardening)  
- **PR 3:** M3 (schema mapping)  
- **PR 4:** M4 + M5 (client/services/docs)

This keeps each change reviewable and lowers regression risk.

If you want, next I can draft the **exact target folder tree and starter class signatures** so you can begin PR 1 immediately.

