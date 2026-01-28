#!/usr/bin/env python3
import sys
from pathlib import Path

INPUT_FILE = "domain.txt"
OUTPUT_FILE = "rules.yaml"

def main():
    input_path = Path(INPUT_FILE)
    if not input_path.exists():
        print(f"❌ FATAL: {INPUT_FILE} not found!", file=sys.stderr)
        print(f"PWD: {Path.cwd()}", file=sys.stderr)
        print(f"FILES: {[f.name for f in Path.cwd().iterdir()]}", file=sys.stderr)
        sys.exit(1)
    
    try:
        domains = []
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                d = line.strip().lower()
                if d and not d.startswith(('#', '//')) and len(d.split('.')) > 1:
                    clean = d.lstrip('*.')
                    if clean.count('.') >= 1:  # 至少一个点（example.com）
                        domains.append(f"+.{clean}")
        
        if not domains:
            print("❌ FATAL: No valid domains found", file=sys.stderr)
            sys.exit(1)
        
        # ✅ 关键修复：生成 Clash.Meta v1.13.0 严格要求的格式
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("payload:\n")
            for domain in sorted(set(domains)):
                # 注意：2个空格缩进 + 单引号 + 无尾随空格
                f.write(f"  - '{domain}'\n")
        
        print(f"✅ SUCCESS: {len(domains)} domains → {OUTPUT_FILE}", file=sys.stderr)
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ FATAL: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
