import unittest
from appeal_data_script import *

#unit tests for the appeal_data_script
class appealstests(unittest.TestCase):
    #tests if value counts are correctly displayed
    def test_valuecountsdisplayedcorrectly(self):

        
        datas = {'AppealStatus': [1, 2,2, 3], 'perc': [3, 4,6, 5]}
        df = pd.DataFrame(data=datas)
        counts = appealperc(df)
        test = counts[2]

        self.assertEqual(test, .5)

    #tests if appealsuccchart function has any output
    def test_nooutputcharts(self):
        datas = {'AppealStatus': [1, 2,2, 3], 'perc': [3, 4,6, 5], 0: [500,100,600, 300]}
        df = pd.DataFrame(data=datas)
        test = appealsuccchart(df)
        
        self.assertEqual(test, None)

if __name__ == '__main__':
    unittest.main()   