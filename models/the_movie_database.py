import pandas as pd
import matplotlib.pyplot as plt


class TheMovieDatabase(object):
    def __init__(self, path):
        self.req_index = ['id', 'original_title', 'popularity', 'release_year',
                          'revenue_adj', 'vote_average', 'vote_count']
        self.df_orig = pd.read_csv(path, index_col=self.req_index)
        self.df = self.__explode_cast()
        self.chart_colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
        # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
        for i in range(len(self.chart_colors)):
            r, g, b = self.chart_colors[i]
            self.chart_colors[i] = (r / 255., g / 255., b / 255.)

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
        self.df['release_year_dup'] = self.df['release_year']
        # ['release_year', 'actor']
        actor_stats_df = self.df.groupby(['actor'], as_index=False)\
            .agg(agg_functions).rename(columns=rename_col).sort_values('number_of_movies', ascending=False)
        return actor_stats_df

    def get_career_len_mean(self):
        df = self.get_actor_metrics()
        # Create actor career length column
        df['career_length'] = df['last_year'] - df['first_year']
        # Create bins for actor career length
        bin_edges = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 100]
        bin_names = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45+']
        df['career_length_bin'] = pd.cut(df['career_length'], bin_edges, labels=bin_names)
        return df.groupby('career_length_bin', as_index=False)['vote_average'].mean()

    def plot_career_len_mean(self):
        self.get_career_len_mean().plot.bar(x='career_length_bin', y='vote_average', ylim=5, color=self.chart_colors[0])
        plt.savefig("../figures/foo.pdf", bbox_inches='tight')
        plt.show()


