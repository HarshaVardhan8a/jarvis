import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Subdirectory of venv: {'venv' in sys.executable}")
print("System Path:")
for p in sys.path:
    print(f"  {p}")

try:
    import langchain
    print(f"LangChain found at: {langchain.__file__}")
except ImportError as e:
    print(f"LangChain import failed: {e}")

try:
    import langchain_community
    print(f"LangChain Community found at: {langchain_community.__file__}")
except ImportError as e:
    print(f"LangChain Community import failed: {e}")
