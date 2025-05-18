import numpy as np
import random


def fake_results():
    ids = []
    rel_ids = []
    for i in range(5):
        a = np.random.randint(0, 9)
        while a in rel_ids:
            a = np.random.randint(0, 9)
        rel_ids.append(a)
    for i in range(10):
        a = np.random.randint(0, 200)
        while a in ids:
            a = np.random.randint(0, 200)
        ids.append(a)
    relationships = []
    for i in range(30):
        a = 0
        b = 0
        c = 0
        while [a, b, c] in relationships or a == c:
            a = random.choice(ids)
            b = random.choice(rel_ids)
            c = random.choice(ids)
        relationships.append([a, b, c])
    return relationships, ids, rel_ids


def get_matrix(relationships, ids, rel_ids):
    ids.sort()
    rel_ids.sort()
    matrix_3d = np.zeros((len(ids), len(ids), len(rel_ids)))
    matrix_2d = np.zeros((len(ids), len(ids)))
    for rel in relationships:
        a = ids.index(rel[0])
        b = rel_ids.index(rel[1])
        c = ids.index(rel[2])
        print(a, b, c)
        matrix_3d[a, c, b] = 1
        matrix_2d[a, c] = b + 1
    return matrix_3d, matrix_2d


if __name__ == "__main__":
    rels, ids, rel_ids = fake_results()
    m = get_matrix(rels, ids, rel_ids)
