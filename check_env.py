#!/usr/bin/env python3
# 环境检查脚本

import sys
import importlib
import os

print("=== 每日问答小工具环境检查 ===")

# 检查Python版本
print("\n1. 检查Python版本...")
python_version = sys.version_info
print(f"当前Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")

if python_version.major < 3 or python_version.minor < 8:
    print("⚠️  警告: Python版本低于3.8，可能会导致功能异常")
else:
    print("✅ Python版本满足要求")

# 检查依赖
print("\n2. 检查依赖安装情况...")
dependencies = [
    'Flask',
    'requests',
    'markdown'
]

missing_deps = []
for dep in dependencies:
    try:
        importlib.import_module(dep)
        print(f"✅ {dep} 已安装")
    except ImportError:
        print(f"❌ {dep} 未安装")
        missing_deps.append(dep)

# 检查目录结构
print("\n3. 检查目录结构...")
required_dirs = [
    'knowledge_base',
    'cache',
    'static',
    'static/css',
    'static/js',
    'templates'
]

for dir_path in required_dirs:
    if os.path.exists(dir_path):
        print(f"✅ 目录 {dir_path} 存在")
    else:
        print(f"⚠️  目录 {dir_path} 不存在，将自动创建")
        os.makedirs(dir_path, exist_ok=True)

# 检查配置文件
print("\n4. 检查配置文件...")
if os.path.exists('config.py'):
    print("✅ 配置文件存在")
else:
    print("❌ 配置文件不存在")

# 检查数据库
print("\n5. 检查数据库...")
if os.path.exists('quiz.db'):
    print("✅ 数据库文件存在")
else:
    print("⚠️  数据库文件不存在，启动时将自动创建")

# 输出检查结果
print("\n=== 检查结果 ===")
if missing_deps:
    print(f"❌ 缺少依赖: {', '.join(missing_deps)}")
    print("请运行以下命令安装依赖:")
    print("pip install -r requirements.txt")
else:
    print("✅ 所有依赖都已安装")

print("\n=== 运行说明 ===")
print("1. 安装依赖: pip install -r requirements.txt")
print("2. 启动应用: python app.py")
print("3. 访问应用: http://127.0.0.1:5000")

print("\n环境检查完成！")
