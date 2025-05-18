import nltk
# import os
#
# proxy = 'http://127.0.0.1:1080'
# os.environ['http_proxy'] = proxy
# os.environ['HTTP_PROXY'] = proxy
# os.environ['https_proxy'] = proxy
# os.environ['HTTPS_PROXY'] = proxy

# noinspection PyUnresolvedReferences
from pattern.en import conjugate

pronoun = {
    'me': 'I',
    'him': 'he',
    'her': 'she',
    'us': 'we',
    'them': 'they'
}

errata = {
    'Juliet': 'NNP',
    'loves': 'VBZ',
    'Romeo': 'NNP',
    'eats': 'VBZ',
    'beret': 'NN',
    'girl': 'NN',
    'legs': 'NNS',
    'hobby': 'NN'
}


def std_rel_str(rel):
    rel = conjugate(rel, '3sg')
    return rel


def std_node_str(node):
    if node.lower() in pronoun:
        return pronoun[node.lower()]
    return node


def merge_matcher(result):
    a = None
    b = None
    c = None
    matched = None
    if len(result) == 3:
        for i in range(len(result)):
            result[i] = list(result[i])
            if result[i][0] in errata:
                result[i][1] = errata[result[i][0]]
        if result[0][1].startswith('NN') or result[0][1] in ['PRP', 'VBG']:
            if result[1][1].startswith('VB'):
                if result[2][1].startswith('NN') or result[2][1] in ['PRP', 'VBG']:
                    matched = 'MERGE'
                    print('Matched:', matched)
                    a = result[0][0]
                    b = result[1][0]
                    c = result[2][0]
                else:
                    print('Target Node Mismatch!')
            else:
                print('Relationship Mismatch!')
        else:
            print('Source Node Mismatch!')
    else:
        print('Length Mismatch!')
    return matched, a, b, c


def delete_matcher(result):
    a = None
    b = None
    c = None
    matched = None
    if len(result) == 5:
        if result[0][1].startswith('NN') or result[0][1] == 'PRP':
            if result[1][1].startswith('VB') or result[1][1] == 'MD':
                if result[2][1] == 'RB':
                    if result[3][1].startswith('VB'):
                        if result[4][1].startswith('NN') or result[4][1] == 'PRP':
                            matched = 'DELETE'
                            print('Matched:', matched)
                            a = result[0][0]
                            b = result[3][0]
                            c = result[4][0]
                        else:
                            print('Target Node Mismatch!')
                    else:
                        print('Relationship Mismatch!')
                else:
                    print('Negator Mismatch!')
            else:
                print('Modal Verb Mismatch!')
        else:
            print('Source Node Mismatch!')
    else:
        print('Length Mismatch!')
    return matched, a, b, c


def verify_format(text):
    result = nltk.pos_tag(nltk.word_tokenize(text))
    print(result)
    matched, a, b, c = merge_matcher(result)
    if matched is None:
        matched, a, b, c = delete_matcher(result)
    if matched is None:
        pass
    return matched, a, b, c


if __name__ == "__main__":
    std_rel_str('loved')
