#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path

def die(msg: str, code: int = 1) -> None:
    print(f"[sync_compile_commands] {msg}", file=sys.stderr)
    raise SystemExit(code)

def load_presets(presets_path: Path) -> dict:
    try:
        with presets_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        die(f"Failed to read {presets_path}: {e}")

def find_configure_preset(presets: dict, name: str) -> dict:
    for p in presets.get("configurePresets", []):
        if p.get("name") == name:
            return p
    die(f"configurePreset '{name}' not found in CMakePresets.json")

def merge_inherits(presets: dict, preset: dict) -> dict:
    """
    Implements a minimal inheritance merge:
    - If preset has "inherits": string or list[str], merge base -> derived
    - For dict fields, derived overrides base
    - For cacheVariables, merge dict with derived overriding base
    """
    def get_preset_by_name(n: str) -> dict:
        return find_configure_preset(presets, n)

    inherits = preset.get("inherits")
    if not inherits:
        return preset

    if isinstance(inherits, str):
        bases = [inherits]
    elif isinstance(inherits, list):
        bases = inherits
    else:
        die(f"Invalid inherits format in preset '{preset.get('name')}'")

    merged = {}
    merged_cache = {}

    # Merge all bases in order, then derived
    for bname in bases:
        bp = merge_inherits(presets, get_preset_by_name(bname))
        # merge top-level keys
        for k, v in bp.items():
            if k == "cacheVariables":
                continue
            merged[k] = v
        merged_cache.update(bp.get("cacheVariables", {}))

    # Apply derived
    for k, v in preset.items():
        if k == "cacheVariables":
            continue
        merged[k] = v
    merged_cache.update(preset.get("cacheVariables", {}))

    merged["cacheVariables"] = merged_cache
    return merged

def resolve_binary_dir(template: str, source_dir: Path, preset_name: str) -> Path:
    """
    Resolves only the placeholders you use:
      ${sourceDir}, ${hostSystemName}, ${presetName}
    Note: hostSystemName here uses platform.system(): Linux/Darwin/Windows
    """
    host = platform.system()  # "Linux", "Darwin", "Windows"
    s = template
    s = s.replace("${sourceDir}", str(source_dir))
    s = s.replace("${hostSystemName}", host)
    s = s.replace("${presetName}", preset_name)
    return Path(s)

def remove_existing(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    try:
        if path.is_symlink() or path.is_file():
            path.unlink()
        else:
            # If it's somehow a dir, don't delete it
            die(f"Refusing to remove non-file path: {path}")
    except Exception as e:
        die(f"Failed to remove existing {path}: {e}")

def try_symlink(src: Path, dst: Path) -> bool:
    try:
        # Use relative link when possible (nice for moving the repo)
        rel = os.path.relpath(src, start=dst.parent)
        os.symlink(rel, dst)
        return True
    except Exception:
        return False

def try_hardlink(src: Path, dst: Path) -> bool:
    try:
        os.link(src, dst)
        return True
    except Exception:
        return False

def try_copy(src: Path, dst: Path) -> bool:
    try:
        shutil.copy2(src, dst)
        return True
    except Exception:
        return False

def main():
    ap = argparse.ArgumentParser(
        description="Create/refresh a root compile_commands.json link to the selected CMake preset build directory."
    )
    ap.add_argument("--preset", required=True, help="configurePreset name, e.g. linux-clang-debug")
    ap.add_argument("--source-dir", default=".", help="Project root (default: .)")
    ap.add_argument("--presets", default="CMakePresets.json", help="Path to CMakePresets.json (default: ./CMakePresets.json)")
    ap.add_argument("--mode", default="auto", choices=["auto", "symlink", "hardlink", "copy"],
                    help="Link mode preference (default: auto)")
    args = ap.parse_args()

    source_dir = Path(args.source_dir).resolve()
    presets_path = (source_dir / args.presets).resolve()
    if not presets_path.exists():
        die(f"CMakePresets.json not found: {presets_path}")

    presets = load_presets(presets_path)
    raw = find_configure_preset(presets, args.preset)
    preset = merge_inherits(presets, raw)

    binary_dir_tmpl = preset.get("binaryDir")
    if not binary_dir_tmpl:
        die(f"Preset '{args.preset}' has no binaryDir")

    build_dir = resolve_binary_dir(binary_dir_tmpl, source_dir, args.preset)
    src_cc = build_dir / "compile_commands.json"
    if not src_cc.exists():
        die(
            f"compile_commands.json not found at:\n  {src_cc}\n"
            f"Did you configure/build this preset first?\n"
            f"Example:\n  cmake --preset {args.preset}"
        )

    dst_cc = source_dir / "compile_commands.json"
    remove_existing(dst_cc)

    is_windows = (platform.system() == "Windows")

    # Decide strategy
    mode = args.mode
    attempted = []

    def attempt(name, fn):
        attempted.append(name)
        ok = fn()
        return ok

    if mode == "symlink":
        ok = attempt("symlink", lambda: try_symlink(src_cc, dst_cc))
    elif mode == "hardlink":
        ok = attempt("hardlink", lambda: try_hardlink(src_cc, dst_cc))
    elif mode == "copy":
        ok = attempt("copy", lambda: try_copy(src_cc, dst_cc))
    else:
        # auto
        # Windows: symlink -> hardlink -> copy
        # POSIX: symlink -> copy (hardlink is okay too, but symlink is nicer)
        if is_windows:
            ok = (attempt("symlink", lambda: try_symlink(src_cc, dst_cc)) or
                  attempt("hardlink", lambda: try_hardlink(src_cc, dst_cc)) or
                  attempt("copy", lambda: try_copy(src_cc, dst_cc)))
        else:
            ok = (attempt("symlink", lambda: try_symlink(src_cc, dst_cc)) or
                  attempt("copy", lambda: try_copy(src_cc, dst_cc)))

    if not ok:
        die(
            "Failed to create link/copy.\n"
            f"Attempted: {', '.join(attempted)}\n"
            "On Windows, symlink may require Developer Mode or Administrator.\n"
            "Try --mode hardlink or --mode copy."
        )

    # Print result
    try:
        if dst_cc.is_symlink():
            target = os.readlink(dst_cc)
            print(f"[sync_compile_commands] OK: symlink {dst_cc} -> {target}")
        else:
            # Could be hardlink or copy
            print(f"[sync_compile_commands] OK: created {dst_cc} (mode={attempted[-1]})")
        print(f"[sync_compile_commands] Source: {src_cc}")
    except Exception:
        print(f"[sync_compile_commands] OK: created {dst_cc}")
        print(f"[sync_compile_commands] Source: {src_cc}")

if __name__ == "__main__":
    main()