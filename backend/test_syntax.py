import py_compile
import sys

try:
    py_compile.compile(r'd:\桌面\abc\backend\app.py', doraise=True)
    print("✓ app.py 语法正确")
except py_compile.PyCompileError as e:
    print(f"✗ app.py 语法错误: {e}")

try:
    py_compile.compile(r'd:\桌面\abc\backend\models.py', doraise=True)
    print("✓ models.py 语法正确")
except py_compile.PyCompileError as e:
    print(f"✗ models.py 语法错误: {e}")
