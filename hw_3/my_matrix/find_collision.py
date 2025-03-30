import numpy as np
from src.matrix import Matrix

def generate_collision():
    while True:
        A = Matrix(np.random.randint(0, 10, (2, 2)).tolist())
        C = Matrix(np.random.randint(0, 10, (2, 2)).tolist())
        
        if hash(A) == hash(C) and A != C:
            B = D = Matrix(np.random.randint(0, 10, (2, 2)).tolist())
            
            AB = A @ B
            CD = C @ D
            
            if AB != CD:
                return A, B, C, D, AB, CD

A, B, C, D, AB, CD = generate_collision()

A.to_file('A.txt')
B.to_file('B.txt')
C.to_file('C.txt')
D.to_file('D.txt')
AB.to_file('AB.txt')
CD.to_file('CD.txt')

with open('hash.txt', 'w') as f:
    f.write(f'Hash of AB: {hash(AB)}\n')
    f.write(f'Hash of CD: {hash(CD)}\n')
