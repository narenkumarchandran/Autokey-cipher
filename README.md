# Autokey-cipher & Custom Hash Generator
## 1. The Cipher
The Autokey cipher is a polyalphabetic substitution cipher similar to the Vigenère cipher. However, instead of repeating the keyword over and over, the Autokey cipher starts with the keyword and then appends the plaintext itself to generate the rest of the keystream.The MathFor a plaintext letter $P_i$, a keystream letter $K_i$, and a ciphertext letter $C_i$:

 * Encryption: $C_i = (P_i + K_i) \pmod{26}$
 * Decryption: $P_i = (C_i - K_i + 26) \pmod{26}$

## 2. The Hash (DJB2)
Once the text is encrypted, it is passed through a custom hash function. 
* It initializes with a prime "magic number" (`5381`).
* It iterates through every character of the encrypted text, applying a bitwise left shift (`<< 5`) and addition to multiply by 33, then adds the character's ASCII value.
* Finally, it applies a 32-bit mask to keep the number bounded and formats it as an 8-character uppercase Hex string (e.g., `0A3F1B9C`).
## 3. Coding 
### How the Code Works:

This script is built around three core functions that handle text preparation, cryptography, and data hashing. Here is a step-by-step breakdown of how each component operates.

### a. Text Preparation: `prepare_string(text)`
Cryptographic algorithms like the Autokey cipher rely on a continuous stream of alphabetic characters to perform mathematical operations using the 26-letter alphabet. 

* **What it does:** This function iterates through the user's input, discarding any spaces, numbers, or punctuation marks. 
* **Conversion:** It forces all remaining characters into uppercase. This ensures that 'A' always maps cleanly to the same ASCII value, preventing casing mismatches from breaking the math.

### b. The Cryptography: `autokey_encrypt(plaintext, key)`
The Autokey cipher is a polyalphabetic substitution cipher. It maps the alphabet to numbers from 0 to 25 (where A=0, B=1, ... Z=25).

* **Keystream Generation:** Unlike the Vigenère cipher, which repeats the secret key, the Autokey cipher appends the `plaintext` directly to the `key`. 
  * *Code:* `keystream = (key + plaintext)[:len(plaintext)]`
  * This guarantees the keystream is exactly as long as the message and is highly unpredictable.
* **ASCII Math:** The function loops through the plaintext and keystream simultaneously. It uses Python's `ord()` function to get the ASCII integer of the character, then subtracts `ord('A')` (which is 65) to normalize the values to a 0–25 range.
* **The Formula:** It adds the plaintext value and the keystream value together, applying Modulo 26 (`% 26`) to ensure the result "wraps around" the alphabet.
* **Reassembly:** Finally, it adds `ord('A')` back to the result and converts it back to a character using `chr()`.

### c. The Hashing: `custom_hash(text)`
To verify data integrity or create a unique digital footprint of the ciphertext, the script uses a pure Python implementation of the **DJB2** hash algorithm.

* **Initialization:** It starts with a "magic" prime number: `5381`.
* **Bitwise Operations:** For every character in the encrypted text, the current hash value is multiplied by 33 and added to the character's ASCII value.
  * *Optimization:* Instead of standard multiplication (`* 33`), it uses a bitwise left shift `(hash_val << 5) + hash_val`. Shifting a binary number left by 5 places multiplies it by 32. Adding the original value back makes it 33. This is significantly faster at the CPU level.
* **32-Bit Masking:** To prevent the integer from growing infinitely large, `hash_val &= 0xFFFFFFFF` forces the number to stay within a 32-bit boundary.
* **Formatting:** It returns the final number formatted as an 8-character uppercase Hexadecimal string (`f"{hash_val:08X}"`).

### d. The Execution Flow
When you run the script, the `__main__` block orchestrates the process:
1. Prompts the user for a message and a secret key.
2. Passes both inputs through `prepare_string()` to sanitize them.
3. Feeds the sanitized text and key into `autokey_encrypt()` to generate the ciphertext.
4. Passes the resulting ciphertext into `custom_hash()` to generate the 8-character hex signature.
5. Prints the sanitized inputs, the encrypted payload, and the resulting hash to the console.

## AI Generation Prompts

This script and its documentation were developed iteratively with the help of an AI assistant. For transparency, here is the exact sequence of prompts used to generate the final code:

1. **Initial Concept:**
   > *"Explain auto key cipher logic in code"*

2. **Adding Interactivity:**
   > *"convert code into user input"*

3. **Introducing Custom Hashing:**
   > *"[Pasted previous code block] include custom hash function without using any library, add to encrypted text"*

4. **Refining the Logic (Simplification):**
   > *"I'm just using to generate a hash func using encrypt string and not doing anything with that"*

5. **Understanding the Mechanics:**
   > *"explain the hash function used"*

6. **Drafting this Documentation:**
   > *"give simple explain to put into github readme file"*
   > *"give me readme of working of the code"*
   > *"and give me section where it tells what are prompt used to achieve the code"*
