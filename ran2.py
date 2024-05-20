import random
import string
import hashlib

def generate_random_string(length=25):
    characters = string.ascii_letters + string.digits  # a-zA-Z0-9
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

def generate_salt(length=6):
    characters = string.ascii_letters + string.digits  # a-zA-Z0-9
    salt = ''.join(random.choices(characters, k=length))
    return salt

def hash_with_salt(input_string):
    sha512_hash = hashlib.sha512(input_string.encode()).hexdigest()
    front_salt = generate_salt()
    back_salt = generate_salt()
    salted_hash = front_salt + sha512_hash + back_salt
    return salted_hash

def double_hash_base64(input_string):
    sha512_hash = hashlib.sha512(input_string.encode()).hexdigest()
    return sha512_hash

def char_to_number_mapping():
    mapping = {}
    for idx, char in enumerate(string.ascii_lowercase, start=1):
        mapping[char] = idx
    for idx, char in enumerate(string.ascii_uppercase, start=28):
        mapping[char] = idx
    for idx, char in enumerate(string.digits, start=55):
        mapping[char] = idx
    return mapping

def calculate_character_sum(input_string):
    mapping = char_to_number_mapping()
    total_sum = 0
    for char in input_string:
        if char in mapping:
            total_sum += mapping[char]
        else:
            total_sum += ord(char) + 66  # Adding 66 for special characters
    return total_sum

def reduce_to_ten_digits(character_sum):
    hashed_number = hashlib.sha256(str(character_sum).encode()).hexdigest()[:10]
    ten_digit_number = int(hashed_number, 16)  # Convert the hexadecimal hash to an integer
    return ten_digit_number % 10000000000

# Generate random string
random_string = generate_random_string()

# Generate SHA-512 hash with salt
hashed_string = hash_with_salt(random_string)

# Double hash the string
double_hashed_string = double_hash_base64(hashed_string)

# Calculate the character sum
character_sum = calculate_character_sum(double_hashed_string)

# Reduce to a ten-digit number
ten_digit_number = reduce_to_ten_digits(character_sum)

# Print the ten-digit number
print(f"Ten Digit Number: {ten_digit_number:010}")  # Ensure it's printed with leading zeros if necessary
