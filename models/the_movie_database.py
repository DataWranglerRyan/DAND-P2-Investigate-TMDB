import pandas as pd


class TheMovieDatabase(object):
    def __init__(self, path):
        self.req_index = ['id', 'original_title', 'popularity', 'release_year',
                          'revenue_adj', 'vote_average', 'vote_count']
        self.df_orig = pd.read_csv(path, index_col=self.req_index)
        self.df = self.__explode_cast()

    def __explode_cast(self):
        """
        Explode each actor in the 'cast' column into separate rows. This function will split actors in the cast column
        by '|'.
        :return: Dataframe where each actor in a movie has their own row.
        """
        columns_to_explode = ['cast']
        # [135397, 118340, 76341, 291270, 97367, 109439]
        cast_df = self.df_orig.loc[:, columns_to_explode]
        cast_df['cast'] = cast_df.cast.apply(lambda x: str(x).split('|'))
        exploded_cast_df = pd.melt(cast_df.cast.apply(pd.Series).reset_index(),
                           id_vars=self.req_index,
                           value_name='actor').drop('variable', axis=1).dropna().sort_values('id').reset_index(drop=True)
        # Remove movies where there are no 'cast' values
        exploded_cast_df = exploded_cast_df[exploded_cast_df.actor != 'nan']
        return exploded_cast_df

    def get_actor_metrics(self):
        rename_col = {
            'popularity': 'avg_popularity',
            'id': 'number_of_movies',
            'release_year': 'first_year',
            'release_year_dup': 'last_year'
        }
        agg_functions = {
            'popularity': 'mean',
            'id': 'count',
            'vote_average': 'mean',
            'vote_count': 'sum',
            'revenue_adj': 'mean',
            'release_year': 'min',
            'release_year_dup': 'max'
        }
        # ['release_year', 'actor']
        self.df['release_year_dup'] = self.df['release_year']
        actor_stats_df = self.df.groupby(['actor'], as_index=False)\
            .agg(agg_functions).rename(columns=rename_col).sort_values('number_of_movies', ascending=False)
        # Create actor career length column
        actor_stats_df['career_length'] = actor_stats_df['last_year'] - actor_stats_df['first_year']
        # Create bins for actor career length
        bin_edges = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 100]
        bin_names = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45-50', '50+']
        actor_stats_df['career_length_bin'] = pd.cut(actor_stats_df['career_length'], bin_edges, labels=bin_names)
        return actor_stats_df

