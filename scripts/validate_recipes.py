import json
import sys
from pathlib import Path


REQUIRED_FIELDS = ["name", "profile", "version", "description", "steps"]
ALLOWED_PROFILES = {"lite", "base", "scalable", "timed"}


def validate_recipe(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: invalid JSON ({exc})"]

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{path}: missing required field '{field}'")

    profile = data.get("profile")
    if profile not in ALLOWED_PROFILES:
        errors.append(f"{path}: profile must be one of {sorted(ALLOWED_PROFILES)}")

    expected_parent = path.parent.name
    if profile and expected_parent != profile:
        errors.append(
            f"{path}: profile '{profile}' must match parent directory '{expected_parent}'"
        )

    steps = data.get("steps")
    if not isinstance(steps, list) or not steps:
        errors.append(f"{path}: steps must be a non-empty array")
    else:
        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                errors.append(f"{path}: step {idx} is not an object")
                continue
            if "id" not in step:
                errors.append(f"{path}: step {idx} missing 'id'")
            if "uses" not in step:
                errors.append(f"{path}: step {idx} missing 'uses'")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    recipe_paths = sorted(root.glob("recipes/**/*.soustack.json"))
    if not recipe_paths:
        print("No recipes found under recipes/")
        return 1

    all_errors: list[str] = []
    for recipe_path in recipe_paths:
        all_errors.extend(validate_recipe(recipe_path))

    if all_errors:
        print("Validation failed:")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(recipe_paths)} recipe(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
