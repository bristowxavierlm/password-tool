# wordlist_generator.py
import itertools

def leetspeak(word):
    substitutions = {'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 's': ['5', '$']}
    variations = [word]
    for char, subs in substitutions.items():
        new_variations = []
        for variation in variations:
            if char in variation:
                for sub in subs:
                    new_variations.append(variation.replace(char, sub))
        variations.extend(new_variations)
    return list(set(variations))

def generate_wordlist(info: dict) -> list:
    base_words = list(filter(None, [
        info.get("name"),
        info.get("pet"),
        info.get("dob"),
        info.get("phone"),
        info.get("idol"),
        info.get("parent"),
        info.get("child"),
        info.get("spouse"),
        info.get("hometown")
    ]))

    patterns = []
    for word in base_words:
        leet_words = leetspeak(word.lower())
        patterns.extend(leet_words)
        for year in ['123', '1234', '2020', '2024']:
            patterns.extend([w + year for w in leet_words])

    return list(set(patterns))

def export_wordlist(words: list, filename="custom_wordlist.txt"):
    with open(filename, "w") as f:
        for word in words:
            f.write(word + "\n")
