import matplotlib.pyplot as plt
import seaborn as sns
from models.the_movie_database import TheMovieDatabase

tmdb = TheMovieDatabase('../data/tmdb-movies.csv')
# actor_df = tmdb.get_actor_metrics()
# print(actor_df)
# actor_df.plot.scatter(x='career_length', y='vote_average')
# plt.show()

career_df = tmdb.get_career_len_mean()
tmdb.plot_career_len_mean()
print(career_df)
print('done')
