from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class Utility:
    def __init__(self):
        pass


    def tokenize(self, text):
        tokens = word_tokenize(text)
        lemmatizer = WordNetLemmatizer()

        clean_tokens = []
        for tok in tokens:
            clean_tok = lemmatizer.lemmatize(tok).lower().strip()
            clean_tokens.append(clean_tok)

        return clean_tokens
