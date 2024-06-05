import nltk

try:
    _ = nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')