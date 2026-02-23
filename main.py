import sys

def main():
    if len(sys.argv) > 1:
        print(f"Hello {sys.argv[1]}", file=sys.stderr)
    else:
        print("Hello", file=sys.stderr)

if __name__ == "__main__":
    main()
