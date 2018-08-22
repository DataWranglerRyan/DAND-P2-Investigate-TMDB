from models.the_movie_database import TheMovieDatabase

save = True
tmdb = TheMovieDatabase('../data/tmdb-movies.csv')
tmdb.plot_avg_rating_by_career_len(save=save)
tmdb.plot_avg_rating_by_movie_exp(save=save)
tmdb.plot_an_actors_avg_ratings_over_time('Robert De Niro', save=save)
print('Complete')
