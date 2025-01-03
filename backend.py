import heapq
from collections import Counter
import struct
import os

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
def calculate_frequency(input_file):
    """
    Calculate the frequency of each character in the file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
        if not text:
            raise ValueError("Input file is empty.")
        return Counter(text)
    except Exception as e:
        return e

def build_huffman_tree(freq_table):
    """
    Build the Huffman tree from the frequency table.
    """
    try:
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
    except Exception as e:
        return e

def generate_codes(huffman_tree):
    """
    Generate Huffman codes for characters from the Huffman tree.
    """
    try:
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
    except Exception as e:
        return e

def encode_file_huffman(file_path, codes):
    """
    Encode the file's content using the Huffman codes.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        if not text:
            raise ValueError("Input file is empty.")
        return ''.join(codes[char] for char in text)
    except Exception as e:
        return e

def write_compressed_file_huffman(output_path, freq_table, encoded_data):
    """
    Write the compressed data to a binary file.
    """
    try:
        with open(output_path, 'wb') as file:
            # Write frequency table
            file.write(struct.pack('>I', len(freq_table)))  # Number of entries
            for char, freq in freq_table.items():
                file.write(struct.pack('>cI', char.encode(), freq))

            # Write padding and encoded data
            padding = (8 - len(encoded_data) % 8) % 8
            encoded_data += '0' * padding
            file.write(struct.pack('>B', padding))  # Write padding length

            # Write encoded data in bytes
            for i in range(0, len(encoded_data), 8):
                byte = encoded_data[i:i + 8]
                file.write(struct.pack('>B', int(byte, 2)))
    except Exception as e:
        return e

# Huffman Decoding Functions
def decode_huffman_data(huffman_tree, binary_data, padding):
    """
    Decode the binary data using the Huffman tree.
    """
    try:
        decoded_text = []
        current_node = huffman_tree

        # Remove padding bits
        binary_data = binary_data[:-padding] if padding else binary_data

        for bit in binary_data:
            current_node = current_node.left if bit == '0' else current_node.right
            if current_node.char is not None:  # Leaf node
                decoded_text.append(current_node.char)
                current_node = huffman_tree

        return ''.join(decoded_text)
    except Exception as e:
        return e

def decode_file(input_file):
    """
    Decode the compressed file and save the decompressed content to a file.
    """
    try:
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

        output_file = os.path.join(os.path.dirname(input_file), 'Huffman decompressed ' + os.path.basename(input_file))
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(decoded_text)
        return False
    except Exception as e:
        return e

# Run-Length Encoding Functions
def run_length_encode(input_file):
    """
    Perform Run-Length Encoding on the input file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
        if not text:
            raise ValueError("Input file is empty.")

        encoded = []
        count = 1
        for i in range(1, len(text)):
            if text[i] == text[i - 1]:
                count += 1
            else:
                encoded.append(f"{text[i - 1]}{count}")
                count = 1
        encoded.append(f"{text[-1]}{count}")
        output_file = os.path.join(os.path.dirname(input_file), 'run-length compressed ' + os.path.basename(input_file))
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(''.join(encoded))

        return False
    except Exception as e:
        return e

def run_length_decode(input_file):
    """
    Decode a Run-Length Encoded file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
        if not text:
            raise ValueError("Input file is empty.")

        decoded = []
        i = 0
        while i < len(text):
            char = text[i]
            count = ''
            i += 1
            while i < len(text) and text[i].isdigit():
                count += text[i]
                i += 1
            decoded.append(char * int(count))

        output_file = os.path.join(os.path.dirname(input_file), 'run-length decompressed ' + os.path.basename(input_file))
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(''.join(decoded))

        return False
    except Exception as e:
        return e

def huff_encoder(input_file):
    try:
        freq_table = calculate_frequency(input_file)
        huffman_tree = build_huffman_tree(freq_table)
        codes = generate_codes(huffman_tree)
        encoded_data = encode_file_huffman(input_file, codes)
        compressed_file = os.path.join(os.path.dirname(input_file), 'Huffman compressed ' + os.path.basename(input_file))
        write_compressed_file_huffman(compressed_file, freq_table, encoded_data)
        return False
    except Exception as e:
        return e