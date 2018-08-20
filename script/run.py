import matplotlib.pyplot as plt
from models.the_movie_database import TheMovieDatabase

tmdb = TheMovieDatabase('../data/tmdb-movies.csv')
actor_df = tmdb.get_actor_metrics()
print(actor_df)
actor_df.plot.scatter(x='career_length', y='vote_average')
plt.show()

# locations = [1, 2, 3, 4]
# height = [10, 20, 30, 40]
# labels = ['High', 'Moderately High', 'Medium', 'Low']
# f = plt.figure()
# plt.plot(locations, height, 'go-', label='line 1')
# plt.show()
# f.savefig("../figures/foo.pdf", bbox_inches='tight')

print('done')
