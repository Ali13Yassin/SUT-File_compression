import heapq
from collections import Counter


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


def add_parity_bits(encoded_data):
    # Break data into 8-bit chunks and calculate parity
    data_with_parity = []
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i + 8]
        parity = byte.count('1') % 2  # Even parity: add a '0' if count is even, '1' if odd
        data_with_parity.append(byte + str(parity))
    return ''.join(data_with_parity)


def write_compressed_file_huffman(output_path, freq_table, encoded_data):
    with open(output_path, 'wb') as file:
        file.write(str(freq_table).encode() + b'\n')
        byte_array = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i + 8]
            byte_array.append(int(byte, 2))
        file.write(byte_array)


# Run-Length Encoding Functions
def run_length_encode(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    encoded_data = []
    i = 0
    while i < len(text):
        count = 1
        while i + 1 < len(text) and text[i] == text[i + 1]:
            count += 1
            i += 1
        encoded_data.append((text[i], count))
        i += 1

    return encoded_data


def write_compressed_file_rle(output_path, encoded_data):
    with open(output_path, 'w') as file:
        for char, count in encoded_data:
            file.write(f"{char}{count}")


# Function to choose compression algorithm
def compress_file(file_path, output_file):
    print("Choose a compression algorithm:")
    print("1. Huffman Encoding")
    print("2. Run-Length Encoding (RLE)")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        freq_table = calculate_frequency(file_path)
        huffman_tree = build_huffman_tree(freq_table)
        huffman_codes = generate_codes(huffman_tree)
        encoded_data = encode_file_huffman(file_path, huffman_codes)
        
        # Add parity bits
        encoded_data_with_parity = add_parity_bits(encoded_data)
        
        write_compressed_file_huffman(output_file, freq_table, encoded_data_with_parity)
        print(f"File compressed successfully with Huffman Encoding and Parity: {output_file}")
    elif choice == "2":
        encoded_data = run_length_encode(file_path)
        write_compressed_file_rle(output_file, encoded_data)
        print(f"File compressed successfully with Run-Length Encoding: {output_file}")
    else:
        print("Invalid choice. Please restart and select a valid option.")


# Example usage
file_path = "C:/Users/User/Desktop/se.txt"
output_file = "C:/Users/User/Desktop/compressed_output.txt"

compress_file(file_path, output_file)
