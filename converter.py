#!/usr/bin/env python3
import sys
from pathlib import Path

# 直接硬编码文件名（匹配您的仓库）
INPUT_FILE = "domain.txt"
OUTPUT_FILE = "rules.yaml"

def main():
    input_path = Path(INPUT_FILE)
    
    # 严格验证文件存在
    if not input_path.exists():
        print(f"❌ FATAL: {INPUT_FILE} 不存在!", file=sys.stderr)
        print(f"当前目录: {Path.cwd()}", file=sys.stderr)
        print(f"目录文件: {[f.name for f in Path.cwd().iterdir() if f.is_file()]}", file=sys.stderr)
        sys.exit(1)
    
    # 读取并转换
    try:
        domains = []
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                d = line.strip()
                if d and not d.startswith('#') and '.' in d:
                    domains.append(f"  - '+.{d.lstrip('*.')}'")
        
        if not domains:
            print("❌ FATAL: 未找到有效域名", file=sys.stderr)
            sys.exit(1)
        
        # 写入标准YAML
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("payload:\n" + "\n".join(domains) + "\n")
        
        print(f"✅ SUCCESS: {len(domains)} domains → {OUTPUT_FILE}", file=sys.stderr)
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ FATAL: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
