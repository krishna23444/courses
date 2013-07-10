'''
Created on May 20, 2013

@author: fsharon
'''

import sqlite3
import orange

graph = [
          ("Alpha",   "Tao"),
          ("Tao",     "Epsilon"),
          ("Epsilon", "Xi"),
          ("Sigma",   "Lambda"),
          ("Sigma",   "Beta"),
          ("Beta",    "Delta"),
          ("Lambda",  "Epsilon"),
          ("Epsilon", "Delta")
        ]

parents = {}

# Evidence given - pair with parameter observed, sorted from leafs back to roots  
given = [
          ("Sigma", 1)
        ]

def param(node):
  return node[0].lower() 
 
def setup():
  global conn, c
  conn = sqlite3.connect('HW6.db')
  c = conn.cursor()
  calcParents()
  
def calcParents():
  for (parent, child) in graph:
    if child in parents:
      parents[child].append(parent)   
    else:
      parents[child] = [parent]  

def hasParent(node):
  return node in parents.values() 

def hasChild(node):
  return node in parents 

# T1 Parent Table, T2 Child       
def parentFromChildBayes(parent, child, evidence):
  p = param(parent)
  d = param(child)
  c.execute("SELECT %s, SUM(P%s*P%s) FROM Bayes WHERE %s=%d GROUP BY %s" % (p, p, d, d, evidence, p))
  return c.fetchall()

# SELECT T1.V, SUM(T1.P * T2.P) FROM <p> T1, <c> T2 WHERE T2.V=<e> AND T1.V = T2.V GROUP BY T1.V 
def parentFromChild(parent, child, evidence):
  p = param(parent)
  d = param(child)
  c.execute("SELECT T1.%s, SUM(T1.P%s*T2.P%s) FROM %s T1, %s T2 WHERE T2.%s=%d AND T1.%s=T2.%s GROUP BY T1.%s" 
            % (p, p, d, parent, child, d, evidence, p, d, p))
  return c.fetchall()

# P(Parent) when child has other parent w/o more evidence
# tricky if v1/v2 for other params which is v1 and which is v2 in respect to parent 
# SELECT T1.V, SUM(T1.P * T2.P) FROM <p> T1, <c> T2, <op> T3 WHERE T2.V=<e> AND T1.V = T2.V1 AND T3.V = T2.V2 GROUP BY T1.V 
def parentFromChildWO(parent, child, evidence, oparent):
  p = param(parent)
  d = param(child)
  op = param(oparent)
  c.execute("SELECT T1.%s, SUM(T1.P%s*T2.P%s) FROM %s T1, %s T2, %s T3 WHERE T2.%s=%d AND T1.%s=T2.%s AND T2.%s=T3.%s GROUP BY T1.%s" 
            % (p, p, d, parent, child, oparent, d, evidence, p, d, d, op, p))
  return c.fetchall()

# P(Parent) when child has other parent as well with evidence
def parentFromChildW(parent, child, evidence, oparent, oevidence):
  p = param(parent)
  d = param(child)
  op = param(oparent)
  c.execute("SELECT T1.%s, SUM(T1.P%s*T2.P%s) FROM %s T1, %s T2, %s T3 WHERE T2.%s=%d AND T3.%s=%d AND T1.%s=T2.%s AND T2.%s=T3.%s GROUP BY T1.%s" 
            % (p, p, d, parent, child, oparent, d, evidence, op, oevidence, p, d, d, op, p))
  return c.fetchall()

def p0(node):
  p = param(node)
  c.execute("SELECT %s, SUM(p%s) FROM Bayes GROUP BY %s" % (p, p, p))
  return c.fetchall()

    
def p1(node, by, val):
  p = param(node)
  o = param(by)
  c.execute("SELECT %s, SUM(p%s * p%s) FROM Bayes WHERE %s=%d GROUP BY %s" % (p, p, o, o, val, p))
  return c.fetchall()


def p2(node, by1, val1, by2, val2):
  p = param(node)
  o1 = param(by1)
  o2 = param(by2)
  c.execute("SELECT %s, SUM(p%s * p%s * p%s) FROM Bayes WHERE %s=%d AND %s=%d GROUP BY %s" % (p, p, o1, o2, o1, val1, o2, val2, p))

  return c.fetchall()

  
#select b,sum(pb*ps) from lbs group by b;
  
def q():
  c.execute("select t,sum(pt*pa*ps*px*pd) from bayes where a=1 and s=0 and x=1 and d=1 group by t")
  return c.fetchall()

  
def normalize(table):
  total = 0
  normalized = []
  for row in table:
    total += row[-1]
  for row in table:
    lrow = list(row)
    lrow[-1] /= total
    normalized.append(tuple(lrow))
  return normalized

'''
def backTrack():
  for (param, evidence) in given:
    if hasParent(param):
      print "<", param, ">"
      for parent in parents[param]:
        print 
'''    
    
if __name__ == '__main__':
  pass


def run():
  setup()
  
  '''
  table = p0("Beta")
  print table, normalize(table)

  table = p1("Beta", "Sigma", 0)
  print table, normalize(table)

  table = p2("Delta", "Beta", 1, "Epsilon", 1)
  print table, normalize(table)


  c.execute("SELECT %s, SUM(p%s * p%s * p%s) FROM Bayes WHERE %s=%d AND %s=%d GROUP BY %s" % (p, p, o1, o2, o1, val1, o2, val2, p))

  return c.fetchall()
'''
  
  table = q()
  print table, normalize(table)
  
  '''
  
  table = parentFromChild("Sigma", "Beta", 1)
  print table
  print normalize(table)

  table = parentFromChildWO("Beta", "Delta", 1, "Epsilon")
  print table
  print normalize(table)

  table = parentFromChildW("Beta", "Delta", 1, "Epsilon", 1)
  print table
  print normalize(table)
  
  param("Alpha")
  print ("Alpha", hasParent("Alpha"), hasChild("Alpha"))
  print ("Beta", hasParent("Beta"), hasChild("Beta"))
  print ("Delta", hasParent("Delta"), hasChild("Delta"))
  '''
  conn.close()

run()    