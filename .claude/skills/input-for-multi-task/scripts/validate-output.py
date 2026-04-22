#!/usr/bin/env python3
"""
Validate YAML task list output for batch-spawner.

Checks:
- Valid YAML syntax
- All required fields present: id, description, target_area, instructions
- No duplicate IDs
"""

import sys
import yaml


def validate_task_list(yaml_path: str) -> bool:
    errors: list[str] = []

    # Read file
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[FAIL] File not found: {yaml_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"[FAIL] Invalid YAML syntax: {e}")
        sys.exit(1)

    # Check top-level structure
    if not isinstance(data, dict):
        errors.append("Root must be a YAML object (dict)")
        print_errors(errors)
        sys.exit(1)

    tasks = data.get("tasks")
    if tasks is None:
        errors.append("Missing top-level key: 'tasks'")
        print_errors(errors)
        sys.exit(1)

    if not isinstance(tasks, list):
        errors.append("'tasks' must be a list")
        print_errors(errors)
        sys.exit(1)

    if len(tasks) == 0:
        errors.append("'tasks' list is empty — no tasks to process")
        print_errors(errors)
        sys.exit(1)

    # Validate each task
    required_fields = ["id", "description", "target_area", "instructions"]
    seen_ids: set[int] = set()

    for i, task in enumerate(tasks):
        task_num = i + 1

        if not isinstance(task, dict):
            errors.append(f"Task {task_num}: must be an object (dict)")
            continue

        # Check required fields
        for field in required_fields:
            if field not in task:
                errors.append(f"Task {task_num}: missing required field '{field}'")
            elif task[field] is None or str(task[field]).strip() == "":
                errors.append(f"Task {task_num}: field '{field}' is empty")

        # Check ID
        if "id" in task:
            task_id = task["id"]
            if not isinstance(task_id, int):
                errors.append(f"Task {task_num}: 'id' must be an integer, got {type(task_id).__name__}")
            elif task_id in seen_ids:
                errors.append(f"Task {task_num}: duplicate ID '{task_id}'")
            elif task_id < 1:
                errors.append(f"Task {task_num}: 'id' must be >= 1")
            else:
                seen_ids.add(task_id)

    # Print results
    if errors:
        print(f"[FAIL] Validation failed with {len(errors)} error(s):")
        print_errors(errors)
        sys.exit(1)
    else:
        print(f"[PASS] Validation passed. {len(tasks)} task(s) OK.")
        sys.exit(0)


def print_errors(errors: list[str]):
    for e in errors:
        print(f"  - {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_output.py <path-to-yaml-file>")
        sys.exit(1)

    yaml_path = sys.argv[1]
    validate_task_list(yaml_path)
