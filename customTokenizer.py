def Encoder (text):
    tokens = []
    splittedText = text.split(" ")
    for word in splittedText:
        s = ""
        for c in word:
            s = s + str(ord(c)).zfill(3) # Filling with 0s to make it 3 digits
        tokens.append(s)
    return tokens
        
def Decoder (tokens):
    s = ""
    for tok in tokens:
        st = 0
        length = len(tok)
        while st < length:
            t = tok[st : st+3]
            code = int(t)
            s = s + chr(code)
            st += 3
        s = s + " "
    s = s[0:-1] # Removing last extra space
    return s

text = "Hello Mohit, How are   you?"
enc = Encoder(text)
print("Encoded: ", enc)
dec = Decoder(enc)
print ("Decoded: ", repr(dec))
        
