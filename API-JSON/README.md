# API JSON reference

These fixtures are local examples of the JSON payloads expected by the Alchemy Virtual Table Top import format.

Use these as contract fixtures for unit tests and for validating the canonical field names before refactoring into package modules.

Core contract:
- `abilityScores` uses objects shaped like `{ "name": "str", "value": 16 }`
- `savingThrow` uses `{ "abilityName": "CON", "difficultyClass": 15 }` when present
- `damageRolls` uses objects shaped like `{ "abilityName": "str", "dice": "1d8", "type": "Piercing" }`
- `alignment` is serialized as a display string such as `"Lawful Good"`
- `actions` and `steps` follow the nested Alchemy import structure shown in the API docs

Files in this folder:
- `ability-score.json`
- `alignment.json`
- `saving-throw.json`
- `action-damage.json`
- `action-attack.json`
- `action-step.json`
- `action.json`
- `character.json`
