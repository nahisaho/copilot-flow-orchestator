#!/usr/bin/env python3
"""
Force files under 8000 by removing least critical content.
"""

import re
from pathlib import Path

def force_under_8000(content: str, target: int = 7950) -> str:
    """Force content under target by removing least important sections."""

    current_size = len(content)
    if current_size <= 8000:
        return content

    excess = current_size - target
    print(f"  Need to remove {excess} chars")

    # Strategy 1: Remove entire example sections
    content = re.sub(r'###\s*例[:：].*?(?=\n###|\n##|\Z)', '', content, flags=re.DOTALL)
    content = re.sub(r'###\s*活用例.*?(?=\n###|\n##|\Z)', '', content, flags=re.DOTALL)
    content = re.sub(r'###\s*使用例.*?(?=\n###|\n##|\Z)', '', content, flags=re.DOTALL)
    content = re.sub(r'\n\n\n+', '\n\n', content)

    if len(content) <= target:
        print(f"  After removing examples: {len(content)} chars")
        return content

    # Strategy 2: Shorten framework descriptions - keep only first 2 items per framework
    lines = content.split('\n')
    new_lines = []
    in_framework_section = False
    framework_item_count = 0

    for line in lines:
        if '主要' in line and 'フレームワーク' in line:
            in_framework_section = True
            new_lines.append(line)
        elif in_framework_section and line.startswith('##') and 'フレームワーク' not in line:
            in_framework_section = False
            framework_item_count = 0
            new_lines.append(line)
        elif in_framework_section:
            if line.startswith('**') and line.endswith('**'):
                # Framework name
                framework_item_count = 0
                new_lines.append(line)
            elif line.strip().startswith('-'):
                if framework_item_count < 2:  # Keep only first 2 items
                    new_lines.append(line)
                    framework_item_count += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    content = '\n'.join(new_lines)
    content = re.sub(r'\n\n\n+', '\n\n', content)

    if len(content) <= target:
        print(f"  After trimming frameworks: {len(content)} chars")
        return content

    # Strategy 3: Reduce guideline items to max 4 each
    lines = content.split('\n')
    new_lines = []
    in_guideline = False
    guideline_count = 0

    for line in lines:
        if '行動指針' in line or '重要な原則' in line:
            in_guideline = True
            guideline_count = 0
            new_lines.append(line)
        elif in_guideline and line.startswith('##') and '行動' not in line and '原則' not in line:
            in_guideline = False
            guideline_count = 0
            new_lines.append(line)
        elif in_guideline:
            if line.startswith('###'):
                guideline_count = 0
                new_lines.append(line)
            elif line.strip().startswith('-') or line.strip().startswith('1.'):
                if guideline_count < 4:
                    new_lines.append(line)
                    guideline_count += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    content = '\n'.join(new_lines)
    content = re.sub(r'\n\n\n+', '\n\n', content)

    if len(content) <= target:
        print(f"  After trimming guidelines: {len(content)} chars")
        return content

    # Strategy 4: Reduce dialogue phases to minimal description
    content = re.sub(
        r'(###\s*フェーズ\d+.*?\n)(?:.*?\n){3,}(?=###|##)',
        r'\1\n',
        content,
        flags=re.DOTALL
    )

    if len(content) <= target:
        print(f"  After trimming phases: {len(content)} chars")
        return content

    # Strategy 5: Nuclear option - trim from end
    if len(content) > target:
        # Find last section header
        sections = re.split(r'(^##\s+.*$)', content, flags=re.MULTILINE)
        while len('\n'.join(sections)) > target and len(sections) > 3:
            sections = sections[:-2]  # Remove last section

        content = '\n'.join(sections)

    print(f"  Final size: {len(content)} chars")
    return content.strip()

def process_file(filepath: Path):
    """Process a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_size = len(content)

    if original_size <= 8000:
        print(f"✓ {filepath.name}: {original_size} chars (OK)")
        return original_size

    print(f"Processing {filepath.name} ({original_size} chars):")

    optimized = force_under_8000(content)
    final_size = len(optimized)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(optimized)

    status = "✓" if final_size <= 8000 else "✗"
    reduction = original_size - final_size
    print(f"{status} {filepath.name}: {original_size} → {final_size} chars (-{reduction})\n")

    return final_size

def main():
    prompts_dir = Path('/home/nahisaho/GitHub/specialist-agent-mode/prompts')

    files = []
    for filepath in prompts_dir.glob('*_Japanese.md'):
        size = filepath.stat().st_size
        if size > 8000:
            files.append((filepath, size))

    files.sort(key=lambda x: x[1])

    print(f"Found {len(files)} files over 8000 chars\n")
    print("=" * 80 + "\n")

    results = []
    for filepath, _ in files:
        final_size = process_file(filepath)
        results.append((filepath.name, final_size))

    print("=" * 80)
    print("\nFINAL RESULTS:")
    print("=" * 80)

    success = sum(1 for _, size in results if size <= 8000)
    print(f"\n✓ Success: {success}/{len(results)} files under 8000 chars\n")

    failures = [(name, size) for name, size in results if size > 8000]
    if failures:
        print("Still over 8000:")
        for name, size in failures:
            print(f"  ✗ {name}: {size} chars (excess: {size - 8000})")
    else:
        print("All files successfully optimized!")

    print("\n" + "=" * 80)

if __name__ == '__main__':
    main()
