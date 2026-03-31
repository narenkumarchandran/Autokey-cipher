# Autokey-cipher & Custom Hash Generator
### 1. The Cipher
The Autokey cipher is a polyalphabetic substitution cipher similar to the Vigenère cipher. However, instead of repeating the keyword over and over, the Autokey cipher starts with the keyword and then appends the plaintext itself to generate the rest of the keystream.The MathFor a plaintext letter $P_i$, a keystream letter $K_i$, and a ciphertext letter $C_i$:

 * Encryption: $C_i = (P_i + K_i) \pmod{26}$
 * Decryption: $P_i = (C_i - K_i + 26) \pmod{26}$

### 2. The Hash (DJB2)
Once the text is encrypted, it is passed through a custom hash function. 
* It initializes with a prime "magic number" (`5381`).
* It iterates through every character of the encrypted text, applying a bitwise left shift (`<< 5`) and addition to multiply by 33, then adds the character's ASCII value.
* Finally, it applies a 32-bit mask to keep the number bounded and formats it as an 8-character uppercase Hex string (e.g., `0A3F1B9C`).
