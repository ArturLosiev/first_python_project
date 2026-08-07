print("Hello, ČVUT FEL!")

def check_environment():
    import sys
    return sys.version

print(f"Python version inside WSL: {check_environment()}")