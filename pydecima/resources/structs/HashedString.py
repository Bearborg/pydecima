class HashedString:
    def __init__(self, text_hash, text):
        self.text_hash = text_hash
        self.text = text

    def __str__(self):
        return self.text
