'''
Created on May 21, 2013

@author: fsharon
'''

import sqlite3
import unittest

from HW6.run import * 
from HW6.make_tables import alphaVals

class HW6Test(unittest.TestCase):
  def testParents(self): 
    
    
  def testDB(self):
    conn = sqlite3.connect('HW6.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ALPHA")
    
    alphaVals = c.fetchall()
    print alphaVals

    self.assertEqual(alphaVals, second, msg)

    
    conn.close()
    
  
