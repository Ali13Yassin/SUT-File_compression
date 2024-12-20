import heapq
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        heapq.heappush(heap, merged)
    
    return heap[0]

def generate_codes(root, current_code="", codes={}):
    if root is None:
        return codes
    if root.char is not None:
        codes[root.char] = current_code
    generate_codes(root.left, current_code + "0", codes)
    generate_codes(root.right, current_code + "1", codes)
    return codes

def compress_file(file_path, output_path):
    with open(file_path, 'New', encoding='utf-8') as file:
        text = file.read()
    
    frequencies = Counter(text)
    root = build_huffman_tree(frequencies)
    huffman_codes = generate_codes(root)
    
    encoded_text = ''.join(huffman_codes[char] for char in text)
    padded_encoded_text = encoded_text + '0' * (8 - len(encoded_text) % 8)
    
    byte_array = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte_array.append(int(padded_encoded_text[i:i+8], 2))
    
    with open(output_path, 'wb') as output_file:
        for char, code in huffman_codes.items():
            output_file.write(f"{char}:{code}\n".encode())  # Save Huffman codes
        output_file.write(b'\n')  # Separate the codes from the encoded text
        output_file.write(byte_array)  # Write the encoded content
    
    print("File compressed successfully!")

def decompress_file(input_path, output_path):
    with open(input_path, 'rb') as input_file:
        lines = input_file.readlines()
    
    huffman_codes = {}
    for line in lines:
        line = line.decode().strip()
        if not line:
            break
        char, code = line.split(':')
        huffman_codes[char] = code
    
    reverse_huffman_codes = {v: k for k, v in huffman_codes.items()}
    
    byte_array = b''.join(lines[len(huffman_codes)+1:])
    bit_string = ''.join(format(byte, '08b') for byte in byte_array)
    
    decoded_text = ''
    current_code = ''
    for bit in bit_string:
        current_code += bit
        if current_code in reverse_huffman_codes:
            decoded_text += reverse_huffman_codes[current_code]
            current_code = ''
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(decoded_text)
    
    print("File decompressed successfully!")

# Example usage
file_path = 'example.txt'
output_path_compressed = 'compressed_output.bin'
output_path_decompressed = 'decompressed_output.txt'

compress_file(file_path, output_path_compressed)
decompress_file(output_path_compressed, output_path_decompressed)
