def task(array: str or list) -> int or None:
    for idx, i in enumerate(array):
        if i == '0':
            return idx
    return None


# Сложность O(n)

if __name__ == '__main__':
    print(task("111111111111111111111111100000000"))