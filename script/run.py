import pandas as pd

req_index = ['id', 'original_title', 'popularity', 'release_year']
req_cols = ['original_title', 'cast', 'popularity', 'release_year']
df = pd.read_csv('../data/tmdb-movies.csv', index_col=req_index)
# print(df)


df2 = df.loc[[135397, 76341, 291270], req_cols]
df2['cast'] = df2.cast.apply(lambda x: x.split('|'))
v = pd.melt(df2.cast.apply(pd.Series).reset_index())
print(v)
df_final = pd.melt(df2.cast.apply(pd.Series).reset_index(),
        id_vars=req_index,
        value_name='actor').set_index('id')
df_final = df_final.drop('variable', axis=1).dropna().sort_index()
print(df_final)
print('done')

# df = (pd.DataFrame({'name': ['A.J. Price'] * 3,
#                     'opponent': ['76ers', 'blazers', 'bobcats'],
#                     'nearest_neighbors': [['Zach LaVine', 'Jeremy Lin', 'Nate Robinson', 'Isaia']] * 3})
#       .set_index(['name', 'opponent']))
# print(pd.melt(df.nearest_neighbors.apply(pd.Series).reset_index(),
#              id_vars=['name', 'opponent'],
#              value_name='nearest_neighbors')
#      .set_index(['name', 'opponent'])
#      .drop('variable', axis=1)
#      .dropna()
#      .sort_index()
#      )

# print(df.nearest_neighbors.apply(pd.Series))