import struct

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def from_bytes(bytes):
    # Define the format string for the struct
    fmt = ">2s f i"  # > - big endian, 2s - 2 bytes as string, f - 4 bytes as float, i - 4 bytes as int
    # Unpack the bytes into variables
    name, x, y = struct.unpack(fmt, bytes)
    # Return a Struct instance with the unpacked values
    return Struct(name=name.decode(), x=x, y=y)

def to_bytes(struct):
    # Pack the values in the struct into a bytes object
    return struct.pack(">2s f i", struct.name.encode(), struct.x, struct.y)

# Example usage
bytes = b'\x00\x01\x00\x00\x80?'  # Little endian representation of a struct with name='\x00\x01', x=1.0, y=2
s = from_bytes(bytes)
print(s.name)  # Output: "\x00\x01"
print(s.x)  # Output: 1.0
print(s.y)  # Output: 2

bytes = to_bytes(s)
print(bytes)  # Output: b'\x00\x01\x00\x00\x80?'
