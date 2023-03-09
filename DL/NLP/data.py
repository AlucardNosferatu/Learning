import re

import unicodedata

sentences = [
    ("Do you want a cup of coffee?", "I've had coffee already."),
    ("I've had coffee already.", "Would you like to have another one?"),
    ("Can I get you a coffee?", "No, please no."),
    ("Please give me some coffee.", "How about make it by yourself?"),
    ("Would you like me to make coffee?", "Sure, but not for me."),
    ("Two coffees, please.", "You've drunk too much!"),
    ("How about a cup of coffee?", "Thanks, that's all I need!"),
    ("I drank two cups of coffee.", "I drank two more cups than you."),
    ("Would you like to have a cup of coffee?", "I've had two cups of coffee already."),
    ("There'll be coffee and cake at five.", "The cake is a lie!"),
    ("Another coffee, please.", "Ask your mother for it!"),
    ("I made coffee.", "Tasted like shit."),
    ("I would like to have a cup of coffee.", "Why ask me?"),
    ("Do you want me to make coffee?", "All I need is your love"),
    ("It is hard to wake up without a strong cup of coffee.", "And it is hard to fall asleep without your kiss."),
    ("All I drank was coffee.", "Won't you throw up?"),
    ("I've drunk way too much coffee today.", "You smell like coffee."),
    ("Which do you prefer, tea or coffee?", "Only kids make choices!"),
    ("There are many kinds of coffee.", "But only few of them are tasty."),
    ("I will make some coffee.", "You make, you drink.")
]


# noinspection RegExpDuplicateCharacterInClass
def preprocess(s):
    # for details, see https://www.tensorflow.org/alpha/tutorials/sequences/nmt_with_attention
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r"([?.!¡,¿])", r" \1 ", s)  # Add spaces around punctuations
    s = re.sub(r"[\" \"]+", " ", s)  # Remove extra space
    s = re.sub(r"[^a-zA-Z?.!¡,¿áéíóú¡üñ]+", " ", s)  # Remove other characters
    s = s.strip()
    s = '<start> ' + s + ' <end>'
    return s


sentences = [(preprocess(en), preprocess(es)) for (en, es) in sentences]
source_sentences, target_sentences = list(zip(*sentences))
