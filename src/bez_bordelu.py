def bez_bordelu(text):
    if not text:  # Check if string is empty
        return text
        
    if not text[-1].isalnum():  # Check if last character is not a letter
        return text[:-1].strip()
    
    return text