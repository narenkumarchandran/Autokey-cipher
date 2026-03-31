def prepare_string(text):
    """Removes spaces and converts text to uppercase."""
    return "".join([char.upper() for char in text if char.isalpha()])

def custom_hash(text):
    """
    A simple custom hash function (DJB2 variant) that returns 
    a fixed-length 8-character hexadecimal string. 
    Requires no external libraries.
    """
    hash_val = 5381
    for char in text:
        # hash_val * 33 + ord(char)
        hash_val = ((hash_val << 5) + hash_val) + ord(char)
        # Force to a 32-bit integer to keep a consistent length
        hash_val &= 0xFFFFFFFF
    
    # Return as an 8-character uppercase hex string
    return f"{hash_val:08X}"

def autokey_encrypt(plaintext, key):
    """Encrypts a plaintext string using the Autokey cipher."""
    plaintext = prepare_string(plaintext)
    key = prepare_string(key)
    
    keystream = key + plaintext
    keystream = keystream[:len(plaintext)]
    
    ciphertext = ""
    for i in range(len(plaintext)):
        p_val = ord(plaintext[i]) - ord('A')
        k_val = ord(keystream[i]) - ord('A')
        
        c_val = (p_val + k_val) % 26
        ciphertext += chr(c_val + ord('A'))
        
    return ciphertext

def autokey_decrypt(ciphertext, key):
    """Decrypts a ciphertext string using the Autokey cipher."""
    ciphertext = prepare_string(ciphertext)
    key = prepare_string(key)
    
    plaintext = ""
    keystream = key
    
    for i in range(len(ciphertext)):
        c_val = ord(ciphertext[i]) - ord('A')
        k_val = ord(keystream[i]) - ord('A')
        
        # P_i = (C_i - K_i + 26) mod 26
        p_val = (c_val - k_val + 26) % 26
        p_char = chr(p_val + ord('A'))
        
        plaintext += p_char
        keystream += p_char
        
    return plaintext

# ==========================================
# Example Execution
# ==========================================
if __name__ == "__main__":
    original_text = input("\nEnter the plain text: ")
    secret_key = input("Enter the Key: ")
    
    prepared_text = prepare_string(original_text)
    
    print(f"\nPrepared Text: {prepared_text}")
    print(f"Key:           {prepare_string(secret_key)}")
    print("-" * 45)
    
    # --- ENCRYPTION PHASE ---
    
    # 1. Generate a Hash of the plaintext
    text_hash = custom_hash(prepared_text)
    print(f"Generated Hash: {text_hash}")
    
    # 2. Encrypt the plaintext
    encrypted_text = autokey_encrypt(original_text, secret_key)
    
    # 3. Append the fixed-length hash to the ciphertext
    final_payload = encrypted_text + text_hash
    print(f"Encrypted (+ Hash Payload): {final_payload}")
    print("-" * 45)
    
    # --- DECRYPTION & VERIFICATION PHASE ---
    
    # 4. Extract the 8-character hash and the actual ciphertext
    extracted_hash = final_payload[-8:]
    actual_ciphertext = final_payload[:-8]
    
    # 5. Decrypt the ciphertext back to plaintext
    decrypted_text = autokey_decrypt(actual_ciphertext, secret_key)
    print(f"Decrypted:      {decrypted_text}")
    
    # 6. Verify data integrity by re-hashing the decrypted text
    new_hash = custom_hash(decrypted_text)
    print(f"Verified Hash:  {new_hash}")
    
    if new_hash == extracted_hash:
        print("\nIntegrity Check: SUCCESS (Hashes match!)")
    else:
        print("\nIntegrity Check: FAILED (Data tampered or corrupted!)")