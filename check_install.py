modules = ["streamlit", "textblob", "nltk"]

for m in modules:
    try:
        __import__(m)
        print(f"{m} is installed ✅")
    except ImportError:
        print(f"{m} is NOT installed ❌")