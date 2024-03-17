from pymatgen.core import Composition
import pandas as pd
import numpy as np
import re


def comp(x, places=2):
    '''
    Make sure to standardize the composition.
    '''

    x = Composition(x)
    x = x.fractional_composition*100

    # Round compositions to two sig figs
    y = ''
    for i, j in x.items():

        i = str(i)
        i = ''.join(re.findall('[a-zA-Z]+', i))
        j = round(j, places)

        y += str(i)+str(j)

    # Make sure formula is in alphabetical order
    x = Composition(y)
    x = x.alphabetical_formula

    return x


df = './MDF_DMREF_Metallic_Glasses_v7.csv'
cut = -4

df = pd.read_csv(df)
df.rename(columns={'Composition': 'comp'}, inplace=True)
df.rename(columns={'Rc_[K/s]': 'Rc'}, inplace=True)

df = df[['comp', 'Rc']]

df.dropna(inplace=True)
df = df.groupby('comp').mean().reset_index()

df['log10(Rc)'] = df['Rc'].apply(np.log10)
df.drop('Rc', axis=1, inplace=True)

df['system'] = df['comp'].apply(lambda x: ''.join(sorted([str(i) for i in Composition(x).elements])))

df = df[df['log10(Rc)'] > cut]

df.to_csv('./target.csv', index=False)

print(df)
