import os
import json
import tempfile
import pytest

from src.i18n_check.check.ordered_keys import check_ordered_keys, is_ordered

# Helper to create a temporary JSON file with given data
def create_temp_json_file(data):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8")
    json.dump(data, tmp_file, ensure_ascii=False, indent=2)
    tmp_file.close()
    return tmp_file.name

def test_is_ordered_true():
    ordered_dict = {"a": 1, "b": 2, "c": 3}
    assert is_ordered(ordered_dict) is True

def test_is_ordered_false():
    unordered_dict = {"b": 2, "a": 1, "c": 3}
    assert is_ordered(unordered_dict) is False

def test_check_ordered_keys_detects_unordered(monkeypatch):
    # Create unordered JSON file
    unordered_data = {"b": "second", "a": "first", "c": "third"}
    tmp_path = create_temp_json_file(unordered_data)

    # Patch src_dir argument by monkeypatching check_ordered_keys to use temp directory
    def patched_check_ordered_keys(fix=False, src_dir=None):
        return check_ordered_keys(fix=fix, src_dir=os.path.dirname(tmp_path))
    
    monkeypatch.setattr(
        "src.i18n_check.check.ordered_keys.check_ordered_keys",
        patched_check_ordered_keys
    )

    captured = []

    def fake_print(msg):
        captured.append(msg)

    monkeypatch.setattr("builtins.print", fake_print)

    # Run patched function without fix to detect unordered keys
    patched_check_ordered_keys(fix=False)

    assert any("Unordered keys" in message for message in captured)

    os.remove(tmp_path)

def test_check_ordered_keys_fixes_unordered():
    unordered_data = {"b": "second", "a": "first", "c": "third"}
    tmp_path = create_temp_json_file(unordered_data)

    # Run check_ordered_keys with fix=True on temp directory
    check_ordered_keys(fix=True, src_dir=os.path.dirname(tmp_path))

    with open(tmp_path, encoding="utf-8") as f:
        data = json.load(f)

    assert list(data.keys()) == sorted(data.keys())

    os.remove(tmp_path)
