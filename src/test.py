# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:11:54 2016

@author: sebastian
"""

print a.mean()
print a.std()

m_std = 0
print a.mean()[0]
for i in range(len(a[0])):
    print a[0][i]
    m_std += np.square(a[0][i] - a.mean()[0])
    
m_std = m_std / (len(a[0])-1)

m_std = np.sqrt(m_std)
print m_std