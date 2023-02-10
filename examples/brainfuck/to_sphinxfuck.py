if __name__ == '__main__':
    import sys
    # Includes terminal non-termination
    with open(sys.argv[1]) as file:
        print(file.read().translate(str.maketrans({
            '[': '[(!',
            ']': '])?'
        })).rstrip() + '@(]')
