import pandas as pd
import matplotlib.pyplot as plt


class TheMovieDatabase(object):
    def __init__(self, path):
        self.req_index = ['id', 'original_title', 'popularity', 'release_year',
                          'revenue_adj', 'vote_average', 'vote_count']
        self.df_orig = pd.read_csv(path, index_col=self.req_index)
        self.df_exploded = self.__explode_cast()
        # These are from Tableau's color palette
        self.chart_colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
        # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
        for i in range(len(self.chart_colors)):
            r, g, b = self.chart_colors[i]
            self.chart_colors[i] = (r / 255., g / 255., b / 255.)
        self.chart_style = 'seaborn'

    def __explode_cast(self):
        """
        Explode each actor in the 'cast' column into separate rows. This function will split actors in the cast column
        by '|'.
        :return: Dataframe where each actor in a movie has their own row.
        """
        columns_to_explode = ['cast']
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
        self.df_exploded['release_year_dup'] = self.df_exploded['release_year']
        actor_stats_df = self.df_exploded.groupby(['actor'], as_index=False)\
            .agg(agg_functions).rename(columns=rename_col).sort_values('number_of_movies', ascending=False)
        return actor_stats_df

    def get_data_grouped_by_career_len(self):
        df = self.get_actor_metrics()
        # Create actor career length column
        df['career_length'] = df['last_year'] - df['first_year']
        # Create bins for actor career length
        bin_edges = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 100]
        bin_names = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45+']
        df['career_length_bin'] = pd.cut(df['career_length'], bin_edges, labels=bin_names)
        return df.groupby('career_length_bin', as_index=False)

    def get_avg_rating_by_career_len(self):
        return self.get_data_grouped_by_career_len()['vote_average'].mean()

    def plot_avg_rating_by_career_len(self, save=False):
        plt.style.use(self.chart_style)
        self.get_avg_rating_by_career_len().plot.bar(x='career_length_bin', y='vote_average', ylim=5,
                                            color=self.chart_colors[0], legend=False)
        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.title('Do actors/actresses with longer careers\n produce movies with higher ratings?', fontsize=14)
        plt.xlabel('Career Length (years)', fontsize=10, alpha=0.7)
        plt.ylabel('Average Movie Rating', fontsize=10, alpha=0.7)
        if save:
            plt.savefig("../figures/avg_rating_by_career_len.pdf", bbox_inches='tight')
        plt.show()

    def get_num_actors_by_career_len(self):
        return self.get_data_grouped_by_career_len().agg({'actor': pd.Series.nunique})

    def plot_num_actors_by_career_len(self, save=False):
        plt.style.use(self.chart_style)
        self.get_num_actors_by_career_len().plot.bar(x='career_length_bin', y='actor', ylim=5,
                                            color=self.chart_colors[0], legend=False)
        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.title('How many actors/actresses are in each career length bin?', fontsize=14)
        plt.xlabel('Career Length (years)', fontsize=10, alpha=0.7)
        plt.ylabel('Number of Actors', fontsize=10, alpha=0.7)
        if save:
            plt.savefig("../figures/num_actors_by_career_len.pdf", bbox_inches='tight')
        plt.show()

    def get_avg_rating_by_movie_exp(self):
        df = self.get_actor_metrics()
        # Create bins for movie experience
        bin_edges = [0, 5, 10, 15, 20, 25, 30, 35, 40, 100]
        bin_names = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40+']
        df['number_of_movies_bin'] = pd.cut(df['number_of_movies'], bin_edges, labels=bin_names)
        return df.groupby('number_of_movies_bin', as_index=False)['vote_average'].mean()

    def plot_avg_rating_by_movie_exp(self, save=False):
        plt.style.use(self.chart_style)
        self.get_avg_rating_by_movie_exp().plot.bar(x='number_of_movies_bin', y='vote_average', ylim=5,
                                            color=self.chart_colors[5], legend=False)
        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.title('Do experienced actors/actresses\n produce movies with higher ratings?', fontsize=14)
        plt.xlabel('Number of Movies Starred In', fontsize=10, alpha=0.7)
        plt.ylabel('Average Movie Rating', fontsize=10, alpha=0.7)
        if save:
            plt.savefig("../figures/avg_rating_by_movie_exp.pdf", bbox_inches='tight')
        plt.show()

    def get_an_actors_metrics_over_time(self, actor_name):
        rename_col = {
            'popularity': 'avg_popularity',
            'id': 'number_of_movies'
        }
        agg_functions = {
            'popularity': 'mean',
            'id': 'count',
            'vote_average': 'mean',
            'vote_count': 'sum',
            'revenue_adj': 'mean'
        }
        actor_stats_df = self.df_exploded.groupby(['release_year', 'actor'], as_index=False)\
            .agg(agg_functions).rename(columns=rename_col).sort_values('release_year', ascending=False)
        actor_stats_df = actor_stats_df[actor_stats_df.actor == actor_name]
        if not actor_stats_df.shape[0]:
            print('Warning: {} does not exist in table.'.format(actor_name))
        return actor_stats_df

    def plot_an_actors_avg_ratings_over_time(self, actor_name, save=False):
        plt.style.use(self.chart_style)
        self.get_an_actors_metrics_over_time(actor_name).plot.line(x='release_year', y='vote_average',
                                                                   color=self.chart_colors[8], legend=False)
        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.title("How has {}'s average movie ratings fared over time?".format(actor_name), fontsize=14)
        plt.xlabel('Release Year of Movie', fontsize=10, alpha=0.7)
        plt.ylabel('Average Movie Rating', fontsize=10, alpha=0.7)
        if save:
            plt.savefig("../figures/actor_career_over_time.pdf", bbox_inches='tight')
        plt.show()
