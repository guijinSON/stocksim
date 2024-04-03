import re

def extract_dictionary_from_sentence(sentence):
    pattern = r'\{([^{}]*)\}'
    match = re.search(pattern, sentence)
    if match:
        dict_string = match.group(1)
        try:
            dictionary = dict(item.split(':') for item in dict_string.split(','))
            return dictionary
        except ValueError:
            print("Error: Dictionary string is not in the correct format.")
            return None
    else:
        print("Error: No dictionary found in the sentence.")
        return None