import secrets
import string
import hashlib
import logging
import unittest

# Setup logging for detailed tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_random_string(length=25):
    """
    Generate a cryptographically secure random string of specified length.
    
    Args:
        length (int): The length of the random string.
    
    Returns:
        str: A random string composed of uppercase, lowercase letters and digits.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_salt(length=6):
    """
    Generate a cryptographically secure salt.
    
    Args:
        length (int): The length of the salt.
    
    Returns:
        str: A salt string composed of uppercase, lowercase letters and digits.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def hash_with_salt(input_string):
    """
    Compute the SHA-512 hash of the input string and sandwich it with two salts.
    
    Args:
        input_string (str): The string to hash.
    
    Returns:
        str: A salted hash string with the format: front_salt + SHA512(input_string) + back_salt.
    """
    sha512_hash = hashlib.sha512(input_string.encode('utf-8')).hexdigest()
    front_salt = generate_salt()
    back_salt = generate_salt()
    return front_salt + sha512_hash + back_salt

def double_hash_base64(input_string):
    """
    Compute a second-level SHA-512 hash of the input string.
    
    Args:
        input_string (str): The string to hash.
    
    Returns:
        str: The SHA-512 hash (in hexadecimal format).
    """
    return hashlib.sha512(input_string.encode('utf-8')).hexdigest()

def char_to_number_mapping():
    """
    Create a mapping for characters to numbers:
      - Lowercase letters: a=1, b=2, …, z=26
      - Uppercase letters: A=28, B=29, … 
      - Digits: 0=55, 1=56, …, 9=64
    
    Returns:
        dict: Mapping for letters and digits.
    """
    mapping = {char: idx for idx, char in enumerate(string.ascii_lowercase, start=1)}
    mapping.update({char: idx for idx, char in enumerate(string.ascii_uppercase, start=28)})
    mapping.update({char: idx for idx, char in enumerate(string.digits, start=55)})
    return mapping

def calculate_character_sum(input_string):
    """
    Calculate the total sum of characters in the string based on a predefined mapping.
    For special characters not in the mapping, their ASCII value plus 66 is added.
    
    Args:
        input_string (str): The string whose characters are to be summed.
    
    Returns:
        int: The resulting total sum.
    """
    mapping = char_to_number_mapping()
    total_sum = 0
    for char in input_string:
        if char in mapping:
            total_sum += mapping[char]
        else:
            total_sum += ord(char) + 66  # For special characters
    return total_sum

def reduce_to_ten_digits(character_sum):
    """
    Reduce the numeric character sum to a ten-digit number by applying SHA-256 hashing
    and a modulus operation.
    
    Args:
        character_sum (int): The character sum to reduce.
    
    Returns:
        int: A ten-digit number.
    """
    hashed_number = hashlib.sha256(str(character_sum).encode('utf-8')).hexdigest()[:10]
    ten_digit_number = int(hashed_number, 16)
    return ten_digit_number % 10000000000

def main():
    try:
        # Step 1: Generate a cryptographically secure random string.
        random_string = generate_random_string()
        logger.info(f"Random string generated: {random_string}")
    
        # Step 2: Generate a salted SHA-512 hash from the random string.
        salted_hash = hash_with_salt(random_string)
        logger.info(f"Salted hash: {salted_hash}")
    
        # Step 3: Apply a second SHA-512 hash to the salted hash.
        double_hashed = double_hash_base64(salted_hash)
        logger.info(f"Double hashed value: {double_hashed}")
    
        # Step 4: Calculate a numeric sum from the double hash and reduce it to a ten-digit number.
        char_sum = calculate_character_sum(double_hashed)
        ten_digit_number = reduce_to_ten_digits(char_sum)
        logger.info(f"Final Ten Digit Number: {ten_digit_number:010}")
    
        # Output the final ten-digit number.
        print(f"Ten Digit Number: {ten_digit_number:010}")
    except Exception as e:
        logger.error("An error occurred during processing.", exc_info=True)
        raise

# Unit tests for verifying each component
class TestSecureHashFunctions(unittest.TestCase):
    def test_generate_random_string(self):
        rand_str = generate_random_string()
        self.assertEqual(len(rand_str), 25)
        self.assertTrue(all(c in (string.ascii_letters + string.digits) for c in rand_str))
    
    def test_generate_salt(self):
        salt = generate_salt()
        self.assertEqual(len(salt), 6)
        self.assertTrue(all(c in (string.ascii_letters + string.digits) for c in salt))
    
    def test_hash_with_salt(self):
        test_string = "test"
        result = hash_with_salt(test_string)
        # Expected format: 6-char salt + 128-char hash + 6-char salt = 140 characters
        self.assertEqual(len(result), 140)
    
    def test_double_hash_base64(self):
        test_string = "test"
        hash_result = double_hash_base64(test_string)
        self.assertEqual(len(hash_result), 128)
    
    def test_calculate_character_sum_and_reduce(self):
        test_hash = double_hash_base64("test")
        total = calculate_character_sum(test_hash)
        reduced = reduce_to_ten_digits(total)
        self.assertTrue(0 <= reduced < 10000000000)

if __name__ == "__main__":
    main()
    # Run unit tests to validate functionality
    unittest.main(argv=[''], exit=False)
