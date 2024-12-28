import heapq
from collections import Counter
import struct

# Node class for the Huffman Tree
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Huffman Encoding Functions
def calculate_frequency(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    freq_table = Counter(text)
    return freq_table

def build_huffman_tree(freq_table):
    priority_queue = [Node(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def generate_codes(huffman_tree):
    def generate_codes_helper(node, code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = code
        generate_codes_helper(node.left, code + "0")
        generate_codes_helper(node.right, code + "1")

    codes = {}
    generate_codes_helper(huffman_tree, "")
    return codes

def encode_file_huffman(file_path, codes):
    with open(file_path, 'r') as file:
        text = file.read()
    encoded_data = ''.join(codes[char] for char in text)
    return encoded_data

def write_compressed_file_huffman(output_path, freq_table, encoded_data):
    with open(output_path, 'wb') as file:
        # Write frequency table
        file.write(struct.pack('>I', len(freq_table)))  # Number of entries in freq_table
        for char, freq in freq_table.items():
            file.write(struct.pack('>cI', char.encode(), freq))  # Char as 1 byte, freq as 4 bytes

        # Write padding and encoded data
        padding = 8 - (len(encoded_data) % 8)
        encoded_data += '0' * padding  # Pad with zeros to make it a multiple of 8
        file.write(struct.pack('>B', padding))  # Write padding length as 1 byte
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i + 8]
            file.write(struct.pack('>B', int(byte, 2)))  # Write each 8-bit chunk as a byte

# Huffman Decoding Functions
def decode_huffman_data(huffman_tree, binary_data, padding):
    decoded_text = []
    current_node = huffman_tree

    # Remove padding bits
    binary_data = binary_data[:-padding] if padding else binary_data

    for bit in binary_data:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:  # Leaf node
            decoded_text.append(current_node.char)
            current_node = huffman_tree

    return ''.join(decoded_text)

def decode_file(input_file, output_file):
    with open(input_file, 'rb') as file:
        # Read the frequency table
        freq_table = {}
        num_entries = struct.unpack('>I', file.read(4))[0]
        for _ in range(num_entries):
            char = struct.unpack('>c', file.read(1))[0].decode()
            freq = struct.unpack('>I', file.read(4))[0]
            freq_table[char] = freq

        # Read padding length
        padding = struct.unpack('>B', file.read(1))[0]

        # Read binary data
        binary_data = ''
        while byte := file.read(1):
            binary_data += f"{struct.unpack('>B', byte)[0]:08b}"

    # Rebuild Huffman Tree
    huffman_tree = build_huffman_tree(freq_table)

    # Decode data
    decoded_text = decode_huffman_data(huffman_tree, binary_data, padding)

    # Write to output file
    with open(output_file, 'w') as file:
        file.write(decoded_text)

# Main Program
if __name__ == "__main__":
    input_file = 'se.txt'  # Input file to compress
    compressed_file = 'compressed_output.bin'  # Compressed output file
    decompressed_file = 'decompressed_output.txt'  # Decompressed output file

    # Encoding
    freq_table = calculate_frequency(input_file)
    huffman_tree = build_huffman_tree(freq_table)
    codes = generate_codes(huffman_tree)
    encoded_data = encode_file_huffman(input_file, codes)
    write_compressed_file_huffman(compressed_file, freq_table, encoded_data)
    print(f"File '{input_file}' compressed into '{compressed_file}'.")

    # Decoding
    decode_file(compressed_file, decompressed_file)
    print(f"File '{compressed_file}' decompressed into '{decompressed_file}'.")
