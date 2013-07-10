'''
Created on May 20, 2013

@author: fsharon
'''

import sqlite3

conn = sqlite3.connect('HW6.db')
c = conn.cursor()

# Alpha 
c.execute('''CREATE TABLE Alpha (a INTEGER, pa REAL)''')
alphaVals = [(0, 0.99),
             (1, 0.01)]
c.executemany('INSERT INTO Alpha VALUES (?, ?)', alphaVals)

# Sigma
c.execute('''CREATE TABLE Sigma (s INTEGER, ps REAL)''')
sigmaVals = [(0, 0.50),
             (1, 0.50)]
c.executemany('INSERT INTO Sigma VALUES (?, ?)', sigmaVals)

# Beta
c.execute('''CREATE TABLE Beta (b INTEGER, s INTEGER, pb REAL)''')
betaVals = [(0, 0, 0.70),
            (0, 1, 0.40),
            (1, 0, 0.30),
            (1, 1, 0.60)]
c.executemany('INSERT INTO Beta VALUES (?, ?, ?)', betaVals)

# Lambda
c.execute('''CREATE TABLE Lambda (l INTEGER, s INTEGER, pl REAL)''')
lambdaVals = [(0, 0, 0.99),
              (0, 1, 0.90),
              (1, 0, 0.01),
              (1, 1, 0.10)]
c.executemany('INSERT INTO Lambda VALUES (?, ?, ?)', lambdaVals)

# Tao
c.execute('''CREATE TABLE Tao (t INTEGER, a INTEGER, pt REAL)''')
taoVals = [(0, 0, 0.99),
           (0, 1, 0.95),
           (1, 0, 0.01),
           (1, 1, 0.05)]
c.executemany('INSERT INTO Tao VALUES (?, ?, ?)', taoVals)

# Xi
c.execute('''CREATE TABLE Xi (x INTEGER, e INTEGER, px REAL)''')
xiVals = [(0, 0, 0.95),
          (0, 1, 0.02),
          (1, 0, 0.05),
          (1, 1, 0.98)]
c.executemany('INSERT INTO Xi VALUES (?, ?, ?)', xiVals)

# Epsilon
c.execute('''CREATE TABLE Epsilon (e INTEGER, l INTEGER, t INTEGER, pe REAL)''')
epsilonVals = [(0, 0, 0, 1.00),
               (0, 0, 1, 0.00),
               (0, 1, 0, 0.00),
               (0, 1, 1, 0.00),
               (1, 0, 0, 0.00),
               (1, 0, 1, 1.00),
               (1, 1, 0, 1.00),
               (1, 1, 1, 1.00)]
c.executemany('INSERT INTO Epsilon VALUES (?, ?, ?, ?)', epsilonVals)

# Delta
c.execute('''CREATE TABLE Delta (d INTEGER, e INTEGER, b INTEGER, pd REAL)''')
deltaVals = [(0, 0, 0, 0.90),
             (0, 0, 1, 0.20),
             (0, 1, 0, 0.30),
             (0, 1, 1, 0.10),
             (1, 0, 0, 0.10),
             (1, 0, 1, 0.80),
             (1, 1, 0, 0.70),
             (1, 1, 1, 0.90)]
c.executemany('INSERT INTO Delta VALUES (?, ?, ?, ?)', deltaVals)

c.execute('CREATE VIEW Bayes AS SELECT A.a,S.s,E.e,X.x,D.d,T.t,L.l,B.b,pa,ps,pe,px,pd,pt,pl,pb FROM ' +
          'Alpha A, Sigma S, Tao T, Lambda L, Beta B, Epsilon E, Xi X, Delta D WHERE ' + 
          'T.a = A.a AND L.s = S.s AND B.s = S.s AND X.e = E.e AND E.t = T.t AND E.l = L.l AND D.e = E.e and D.b = B.b')

conn.commit()
conn.close()

if __name__ == '__main__':
    pass