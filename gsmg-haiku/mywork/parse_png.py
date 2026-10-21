import struct, zlib

data = open(r'c:\gsmg-puzzle-clean\files\follow_the_white_rabbit.png', 'rb').read()
assert data[:8] == b'\x89PNG\r\n\x1a\n'

pos = 8
while pos < len(data):
    length, chunk_type = struct.unpack('>I4s', data[pos:pos+8])
    chunk_data = data[pos+8:pos+8+length]
    crc = data[pos+8+length:pos+12+length]
    pos += 12 + length
    print(f"Chunk: {chunk_type.decode()} len={length}")
    if chunk_type == b'IHDR':
        w, h, depth, color_type, comp, filt, inter = struct.unpack('>IIBBBBB', chunk_data)
        print(f"  IHDR: {w}x{h}, depth={depth}, color_type={color_type}")
    elif chunk_type == b'tEXt':
        print(f"  tEXt: {chunk_data}")
