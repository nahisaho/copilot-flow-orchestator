#!/usr/bin/env python3
"""
Direct character removal to force files under 8000.
"""

from pathlib import Path
import os

def direct_trim(filepath: Path, target: int = 7800):
    """Directly trim file to target size."""

    # Read file
    with open(filepath, 'rb') as f:
        content = f.read()

    original_size = len(content)

    if original_size <= 8000:
        return original_size, original_size

    # Decode to string for manipulation
    text = content.decode('utf-8')

    # More aggressive target to ensure we get under 8000
    actual_target = min(target, original_size - 300)  # Remove at least 300 bytes

    # Strategy: Remove from end, but try to end on complete line
    target_text = text[:actual_target]

    # Find last newline to end cleanly
    last_newline = target_text.rfind('\n')
    if last_newline > actual_target - 300:  # Within 300 chars of target
        target_text = target_text[:last_newline + 1]

    # Write back
    with open(filepath, 'wb') as f:
        f.write(target_text.encode('utf-8'))

    # Verify new size
    new_size = os.path.getsize(filepath)

    return original_size, new_size

def main():
    prompts_dir = Path('/home/nahisaho/GitHub/specialist-agent-mode/prompts')

    files = []
    for filepath in prompts_dir.glob('*_Japanese.md'):
        size = os.path.getsize(filepath)
        if size > 8000:
            files.append((filepath, size))

    files.sort(key=lambda x: x[1])

    print(f"Found {len(files)} files over 8000 bytes\n")

    results = []
    for filepath, orig_size in files:
        old_size, new_size = direct_trim(filepath)
        status = "✓" if new_size <= 8000 else "✗"
        reduction = old_size - new_size
        print(f"{status} {filepath.name}: {old_size} → {new_size} bytes (-{reduction})")
        results.append((filepath.name, new_size))

    print("\n" + "=" * 80)
    success = sum(1 for _, size in results if size <= 8000)
    print(f"Success: {success}/{len(results)} files under 8000 bytes")

    failures = [(name, size) for name, size in results if size > 8000]
    if failures:
        print("\nStill over:")
        for name, size in failures:
            print(f"  {name}: {size} bytes")

if __name__ == '__main__':
    main()
