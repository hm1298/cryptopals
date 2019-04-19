def pad(data, block_size):
    """
    Takes as input a bytes object and an int. Returns a bytes object with
    length a multiple of block_size, padded at the end with k bytes all of
    value k.
    """
    q, r = divmod(len(data), block_size)
    k = block_size - r
    return data + bytes([k] * k)

print(pad("YELLOW SUBMARINE".encode('utf-8'), 20))