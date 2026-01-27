#!/usr/bin/env python3
"""
Clash 规则集转换器 - 专为 .mrs 二进制编译设计
输入: 纯域名列表 (domain.txt)
输出: 符合 Clash.Meta 编译规范的 YAML 规则集
"""
import argparse
import sys
from pathlib import Path
import re

def is_valid_domain(line: str) -> bool:
    """验证是否为有效域名（跳过注释/空行/无效字符）"""
    line = line.strip()
    if not line or line.startswith('#') or line.startswith('//'):
        return False
    # 基础域名验证（允许通配符开头）
    pattern = r'^(\*\.)?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,} $ '
    return bool(re.match(pattern, line))

def convert_domains(input_path: Path, output_path: Path, exact: bool = False):
    """转换域名列表为 Clash 规则集 YAML"""
    if not input_path.exists():
        print(f"❌ 错误：输入文件不存在: {input_path}", file=sys.stderr)
        print(f"💡 当前目录: {Path.cwd()}", file=sys.stderr)
        print(f"📁 目录内容: {', '.join(f.name for f in Path.cwd().iterdir() if f.is_file())}", file=sys.stderr)
        sys.exit(1)
    
    domains = []
    skipped = 0
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('//'):
                    continue
                
                # 清理常见问题：移除末尾逗号/分号/空格
                line = re.sub(r'[,\s;]+ $ ', '', line)
                
                if is_valid_domain(line):
                    # 标准化：移除已有通配符，统一处理
                    clean_domain = line.lstrip('*.')
                    prefix = '' if exact else '+.'
                    domains.append(f"{prefix}{clean_domain}")
                else:
                    skipped += 1
                    if skipped <= 5:  # 仅显示前5条警告
                        print(f"⚠️  跳过无效行 #{line_num}: {line[:50]}", file=sys.stderr)
        
        if skipped > 5:
            print(f"⚠️  共跳过 {skipped} 条无效行（仅显示前5条）", file=sys.stderr)
        
        if not domains:
            print("❌ 错误：未找到有效域名！请检查输入文件格式", file=sys.stderr)
            sys.exit(1)
        
        # 生成标准 Clash 规则集 YAML
        yaml_content = "payload:\n" + "\n".join(f"  - '{d}'" for d in sorted(set(domains)))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content + '\n')
        
        print(f"✅ 转换成功: {len(domains)} 个有效域名 → {output_path.name}", file=sys.stderr)
        print(f"💡 首条规则示例: {domains[0]}", file=sys.stderr)
        return True
        
    except Exception as e:
        print(f"❌ 转换失败: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="域名列表 → Clash 规则集 YAML (专为 .mrs 二进制编译设计)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
用法示例:
  python converter.py -i domain.txt -o rules.yaml
  python converter.py -i domains.txt -o rules.yaml --exact
        """
    )
    parser.add_argument('-i', '--input', required=True, type=Path, 
                        help='输入文件路径 (纯域名列表，每行一个)')
    parser.add_argument('-o', '--output', required=True, type=Path,
                        help='输出 YAML 文件路径 (供 Clash.Meta 编译)')
    parser.add_argument('--exact', action='store_true',
                        help='精确匹配模式 (不添加 "+." 前缀，仅匹配主域)')
    parser.add_argument('--version', action='version', version='converter.py v1.2 (Clash.Meta 专用)')
    
    args = parser.parse_args()
    
    # 执行转换
    convert_domains(args.input, args.output, args.exact)

if __name__ == "__main__":
    main()
