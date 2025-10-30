#!/usr/bin/env python3
"""
Ultra-aggressive optimizer to reduce Japanese markdown files to under 8000 characters.
Maintains core functionality while aggressively cutting content.
"""

import re
import os
from pathlib import Path

def ultra_compress(content: str, target: int = 7800) -> str:
    """Apply ultra-aggressive compression strategies."""

    # Remove all emojis
    content = re.sub(r'[\U0001F300-\U0001F9FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U00002600-\U000027BF]', '', content)

    # Remove excessive whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r' {2,}', ' ', content)

    # Compress framework sections - ultra aggressive
    # Change multi-line framework descriptions to single lines
    def compress_framework_section(text):
        # Find framework sections
        lines = text.split('\n')
        compressed_lines = []
        in_framework_section = False
        current_framework = None
        framework_content = []

        for line in lines:
            # Check if we're entering a framework section
            if re.match(r'^#{2,3}\s+.*フレームワーク', line):
                in_framework_section = True
                compressed_lines.append(line)
                continue

            # Check if we're leaving framework section
            if in_framework_section and re.match(r'^#{2,3}\s+(?!.*フレームワーク)', line):
                in_framework_section = False

            if in_framework_section:
                # Ultra-compress framework items
                if line.startswith('**') and line.endswith('**'):
                    # Framework name
                    if framework_content:
                        # Flush previous framework as single line
                        compressed_lines.append(' '.join(framework_content))
                        framework_content = []
                    current_framework = line.strip()
                    framework_content.append(current_framework)
                elif line.strip().startswith('-'):
                    # Framework detail - compress to single line
                    detail = line.strip().lstrip('-').strip()
                    if detail and not detail.startswith('**'):
                        # Remove label prefixes
                        detail = re.sub(r'^(目的|活用|構成|適用|定義|要素|使用|テンプレート)[:：]\s*', '', detail)
                        if detail:
                            framework_content.append(detail[:50])  # Max 50 chars per detail
            else:
                # Flush any pending framework
                if framework_content:
                    compressed_lines.append(' '.join(framework_content))
                    framework_content = []
                compressed_lines.append(line)

        # Flush final framework
        if framework_content:
            compressed_lines.append(' '.join(framework_content))

        return '\n'.join(compressed_lines)

    content = compress_framework_section(content)

    # Ultra-compress dialogue process section
    def compress_dialogue_process(text):
        lines = text.split('\n')
        compressed = []
        in_dialogue_section = False
        skip_until_next_header = False

        for line in lines:
            if '対話の進め方' in line or '対話プロセス' in line:
                in_dialogue_section = True
                compressed.append(line)
                continue

            if in_dialogue_section and re.match(r'^#{2,3}\s+', line) and '対話' not in line:
                in_dialogue_section = False

            if in_dialogue_section:
                # Keep phase headers but compress content
                if line.startswith('###') or line.startswith('**フェーズ'):
                    compressed.append(line)
                    skip_until_next_header = False
                elif line.strip() and not skip_until_next_header:
                    # Keep only first 2 lines of content per phase
                    if line.strip().startswith('-') or line.strip().startswith('1.'):
                        compressed.append(line)
                    elif len(line.strip()) > 20:  # Meaningful content
                        compressed.append(line)
                        skip_until_next_header = True
            else:
                compressed.append(line)

        return '\n'.join(compressed)

    content = compress_dialogue_process(content)

    # Compress guideline sections aggressively
    def compress_guidelines(text):
        lines = text.split('\n')
        compressed = []
        in_guideline_section = False
        guideline_type = None
        item_count = 0
        max_items = 5  # Max 5 items per guideline type

        for line in lines:
            if '行動指針' in line or '重要な原則' in line:
                in_guideline_section = True
                compressed.append(line)
                continue

            if in_guideline_section and re.match(r'^#{2,3}\s+', line) and '行動' not in line and '原則' not in line:
                in_guideline_section = False
                item_count = 0

            if in_guideline_section:
                if line.startswith('###') or line.startswith('**'):
                    compressed.append(line)
                    guideline_type = line
                    item_count = 0
                elif line.strip().startswith('-') or line.strip().startswith('1.'):
                    if item_count < max_items:
                        # Compress line content
                        compressed_line = re.sub(r'\*\*.*?\*\*[:：]\s*', '', line)
                        compressed_line = compressed_line[:80]  # Max 80 chars
                        compressed.append(compressed_line)
                        item_count += 1
            else:
                compressed.append(line)

        return '\n'.join(compressed)

    content = compress_guidelines(content)

    # Remove example sections entirely
    content = re.sub(r'###\s*例[:：].*?(?=###|\n##|\Z)', '', content, flags=re.DOTALL)
    content = re.sub(r'###\s*活用例.*?(?=###|\n##|\Z)', '', content, flags=re.DOTALL)
    content = re.sub(r'###\s*使用例.*?(?=###|\n##|\Z)', '', content, flags=re.DOTALL)

    # Remove template code blocks if still over target
    if len(content) > target:
        content = re.sub(r'```[\s\S]*?```', '', content)

    # Compress tables
    def compress_tables(text):
        # Remove table formatting, keep only essential info
        lines = text.split('\n')
        compressed = []
        in_table = False

        for line in lines:
            if '|' in line and line.strip().startswith('|'):
                if not in_table:
                    in_table = True
                    # Keep header
                    compressed.append(line)
                else:
                    # Skip separator and compress rows
                    if not re.match(r'\|\s*[-:]+\s*\|', line):
                        # Compress table cells
                        cells = [cell.strip() for cell in line.split('|')]
                        cells = [cell[:30] for cell in cells if cell]  # Max 30 chars per cell
                        if cells:
                            compressed.append('| ' + ' | '.join(cells) + ' |')
            else:
                if in_table and line.strip():
                    in_table = False
                compressed.append(line)

        return '\n'.join(compressed)

    content = compress_tables(content)

    # Final cleanup
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()

    return content

def optimize_file(filepath: Path, target: int = 7800):
    """Optimize a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()

    original_size = len(original_content)

    if original_size <= 8000:
        print(f"✓ {filepath.name}: {original_size} chars (already under limit)")
        return original_size

    optimized_content = ultra_compress(original_content, target)
    optimized_size = len(optimized_content)

    # If still over, apply emergency measures
    if optimized_size > 8000:
        # Remove entire advanced sections
        optimized_content = re.sub(r'##\s*高度な活用.*?(?=\n##|\Z)', '', optimized_content, flags=re.DOTALL)
        optimized_content = re.sub(r'##\s*応用.*?(?=\n##|\Z)', '', optimized_content, flags=re.DOTALL)
        optimized_content = re.sub(r'##\s*詳細.*?(?=\n##|\Z)', '', optimized_content, flags=re.DOTALL)
        optimized_size = len(optimized_content)

    # Emergency: truncate frameworks if still over
    if optimized_size > 8000:
        lines = optimized_content.split('\n')
        in_framework = False
        kept_lines = []
        framework_count = 0
        max_frameworks = 6

        for line in lines:
            if 'フレームワーク' in line and line.startswith('##'):
                in_framework = True
                kept_lines.append(line)
            elif in_framework and line.startswith('**'):
                framework_count += 1
                if framework_count <= max_frameworks:
                    kept_lines.append(line)
            elif in_framework and line.startswith('##'):
                in_framework = False
                framework_count = 0
                kept_lines.append(line)
            elif not in_framework or framework_count <= max_frameworks:
                kept_lines.append(line)

        optimized_content = '\n'.join(kept_lines)
        optimized_size = len(optimized_content)

    # Final safety truncation
    if optimized_size > 8000:
        optimized_content = optimized_content[:7900] + '\n\n---'
        optimized_size = len(optimized_content)

    # Write optimized content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(optimized_content)

    reduction = original_size - optimized_size
    percentage = (reduction / original_size) * 100

    status = "✓" if optimized_size <= 8000 else "✗"
    print(f"{status} {filepath.name}: {original_size} → {optimized_size} chars (-{reduction}, -{percentage:.1f}%)")

    return optimized_size

def main():
    prompts_dir = Path('/home/nahisaho/GitHub/specialist-agent-mode/prompts')

    # Get all Japanese files over 8000 chars
    files_to_optimize = []
    for filepath in prompts_dir.glob('*_Japanese.md'):
        size = filepath.stat().st_size
        if size > 8000:
            files_to_optimize.append((filepath, size))

    # Sort by size (smallest first for easier debugging)
    files_to_optimize.sort(key=lambda x: x[1])

    print(f"Found {len(files_to_optimize)} files to optimize\n")
    print("=" * 80)

    results = []
    for filepath, original_size in files_to_optimize:
        final_size = optimize_file(filepath)
        results.append((filepath.name, original_size, final_size))

    print("\n" + "=" * 80)
    print("\nSUMMARY:")
    print("=" * 80)

    success_count = sum(1 for _, _, size in results if size <= 8000)
    print(f"\nSuccessfully optimized: {success_count}/{len(results)} files\n")

    if success_count < len(results):
        print("Files still over 8000 chars:")
        for name, orig, final in results:
            if final > 8000:
                print(f"  - {name}: {final} chars (need to cut {final - 8000} more)")
    else:
        print("All files now under 8000 characters! ✓")

    print("\n" + "=" * 80)

if __name__ == '__main__':
    main()
