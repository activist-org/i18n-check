import os
import json

def is_ordered(d: dict) -> bool:
    """Check if dictionary keys are sorted alphabetically."""
    return list(d.keys()) == sorted(d.keys())

def check_ordered_keys(fix: bool = False, src_dir: str = "i18n-src") -> None:
    """
    Check all JSON files in the given directory for alphabetical ordering of keys.
    Optionally fix unordered files by rewriting them with sorted keys.

    Parameters
    ----------
    fix : bool, optional
        If True, reorder keys in JSON files and overwrite them (default is False).
    src_dir : str, optional
        Directory path containing JSON files (default is "i18n-src").
    """
    if not os.path.exists(src_dir):
        print(f"  Directory not found: {src_dir}")
        return

    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".json"):
                path = os.path.join(root, file)

                # Read JSON data
                try:
                    with open(path, encoding="utf-8") as f:
                        data = json.load(f)
                except Exception as e:
                    print(f"  Failed to read {path}: {e}")
                    continue

                # Check ordering
                if not is_ordered(data):
                    print(f"  Unordered keys found in: {path}")

                    if fix:
                        # Create new ordered dict and overwrite file
                        ordered_data = {k: data[k] for k in sorted(data.keys())}
                        try:
                            with open(path, "w", encoding="utf-8") as f:
                                json.dump(ordered_data, f, ensure_ascii=False, indent=2)
                            print(f"  Fixed ordering in: {path}")
                        except Exception as e:
                            print(f" Failed to write {path}: {e}")
                else:
                    print(f"Keys ordered in: {path}")
