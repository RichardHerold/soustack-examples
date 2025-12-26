![CI](https://github.com/soustack-examples/soustack-examples/actions/workflows/ci.yml/badge.svg)

# SouStack Recipe Corpus

This repository is a public corpus of SouStack recipes that are validated for multiple execution profiles. Each recipe is stored as a `.soustack.json` file under the `recipes/` directory and is verified in CI for consistency and conformance to the profile it claims to target.

## Profiles

Profiles describe the expectations and capabilities of the target environment. Recipes should be authored for one of the following profiles:

- **lite** – minimal dependencies and resource footprint; great for quick demos or constrained sandboxes.
- **base** – standard capabilities with typical network and file-system access enabled.
- **scalable** – horizontally scalable workloads that rely on idempotent steps and coordination-friendly patterns.
- **timed** – latency-sensitive recipes designed with explicit timing constraints or deadlines.

## Repository layout

```
recipes/
  lite/       # Lightweight recipes
  base/       # Standard profile recipes
  scalable/   # Recipes that scale horizontally
  timed/      # Latency-aware or deadline-driven recipes
scripts/
  validate_recipes.py  # Conformance checks run in CI
```

## Adding a new recipe

1. Choose the appropriate profile and place the file under `recipes/<profile>/`.
2. Name the file with a short slug and the `.soustack.json` extension (e.g., `my-task.soustack.json`).
3. Include the required top-level fields:
   - `name` (string): Human-readable title.
   - `profile` (string): One of `lite`, `base`, `scalable`, or `timed`. Must match its parent directory.
   - `version` (string): Semantic version of the recipe specification.
   - `description` (string): Brief summary of the recipe’s intent.
   - `steps` (array): Ordered list of step definitions. Each step needs an `id` and `uses` string.
   - Optional fields such as `inputs`, `outputs`, and `metadata` are welcome as long as they are valid JSON.
4. Run the validation script:
   ```bash
   python scripts/validate_recipes.py
   ```
   The script will check JSON validity, required fields, and profile-directory alignment.
5. Open a pull request describing the new recipe and ensure CI passes.

## Contributing

Contributions are welcome! Please keep recipes small, well-commented, and aligned with the intended profile. Use descriptive step names, prefer deterministic actions, and document any external dependencies in the recipe description. If you introduce a new pattern that might benefit other profiles, consider adding separate versions of the recipe under each profile directory.
