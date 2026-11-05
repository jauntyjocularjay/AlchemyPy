# Alchemy.py

`Alchemy.py` is a client library for Alchemy's API for its Virtual Table Top (VTT). 

## `Constants`

Is a set of constants used to prevent the use of magic strings.

## `Ability Score`

Assigns an integer value to an ability. 

```json
 
```

## `Action`

## `Alignment`

## `Character`

## `SavingThrow`

## M1 package layout

The project now exposes a modular `alchemy_py` package with the expected split between model, type, client, service, schema, and error layers. Legacy top-level imports remain available during the transition so existing scripts and tests continue to work while the package structure is stabilized.

## M3 schema mapping layer

The schema package isolates the raw Alchemy import payload from the in-memory domain models. Use `alchemy_py.schemas.character_import.character_from_api(payload)`, `character_to_api(character)`, and `validate_character_payload(payload)` to round-trip between the documented JSON contract and the dataclass-backed model layer.

## M4 client + services layer

The project now includes a minimal HTTP client plus a stable character-import service entrypoint. Use `alchemy_py.client.AlchemyHTTPClient` for request configuration and `alchemy_py.services.CharacterService.import_character(...)` for the end-to-end import workflow.

## Known limitations

- The current model layer intentionally tracks the raw Alchemy character-import payload shape, including keys such as `abilityScores`, `damageRolls`, and `savingThrow`.
- `Dice` currently follows the canonical string form used by the API (`"4d6"`); the richer int-based constructor will be restored during the refactor in M2.
- The action-step wrappers are API-shaped convenience objects and are not yet a full dataclass-driven model layer.
- This project is still in the baseline/safety-net phase, so breaking API changes are deferred until the package reorganization and model hardening milestones.

