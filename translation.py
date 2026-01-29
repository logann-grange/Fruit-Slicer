def translate(word, lang: int):
    with open('translation.txt', 'r', encoding='utf-8') as file:
        for ligne in file:
            parts = ligne.strip().split(":")
            if parts[0] == word:
                return parts[lang] if lang < len(parts) else word
    return word