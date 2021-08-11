import pandas as pd
import numpy as np
def dataset_creator():
    df = pd.DataFrame(np.random.randint(1,8,size=(100, 1)), columns=list('A'))
    df2 = pd.DataFrame(np.random.randint(0,7, size=(100,1)), columns=list('B'))
    df3 = pd.DataFrame(np.random.randint(0, 4, size = (100,1)), columns=list('C'))
    df2 = df2/2
    df2.loc[df2['B'] == 1.5 , 'B'] = 2
    df2.loc[df2['B'] == 2.5,  'B'] = 3
    df = df.join(df2)
    df = df.join(df3)
    df.to_csv('alz_data.csv')