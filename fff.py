import sys

if len(sys.argv) > 2:
    try:
        print(format(int(sys.argv[1]) - int(sys.argv[2])))
    except ValueError:
        print(0)
else:
    print(0)
