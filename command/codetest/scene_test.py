import sys
import os

absPath = os.path.abspath(__file__)
absPath = absPath.split('\\')
absPath = "\\".join(absPath[:-2])

sys.path.append(absPath)
print(sys.path)

from scene import manageScenario 

# test build a new scenario by absolute path
path = r'E:\project\easyTester\easyTester\command\codetest'
name = "Absolute_path"
author = "absolut test"
note = "abssolut test"
manageScenario.buildScenario(path, name, author, note)
# test build a new scenario by a name
path = "chenchuan"
name = "chenchuan"