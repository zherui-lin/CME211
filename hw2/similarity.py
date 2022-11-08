import math, sys, time

# check command line arguments
if len(sys.argv) < 3:
	print("Usage:")
	print("  $ python3 similarity.py <data_file> <output_file> [user_thresh (default = 5)]")
	sys.exit()

# extract command line arguments
data_file = sys.argv[1]
output_file = sys.argv[2]
user_thresh = 5
if len(sys.argv) > 3:
	user_thresh = int(sys.argv[3])

# read movie ratings from file
data = []
with open(data_file, "r") as f:
	data = [line.strip().split()[:-1] for line in f.readlines()]
n_data = len(data)

# transfer rating records into data structure
users = set()
movies = dict()
# map from movie to user and then map user to rating
for d in data:
	u = int(d[0])
	m = int(d[1])
	r = int(d[2])
	users.add(u)
	# initialize nested dict if current movie not in the dict
	if m not in movies:
		movies[m] = dict()
	movies[m][u] = r
n_users = len(users)
n_movies = len(movies)

# record starting time
start_time = time.time()

# get the mean among all ratings of a movie
def cal_mean(movies, m):
	# declare a list and store all ratings
	rating = []
	for u in movies[m]:
		rating.append(movies[m][u])
	return sum(rating) / len(rating)

# calculate mean rating for each movie and store it in dict
means = dict()
for m in movies:
	means[m] = cal_mean(movies, m)

# declare dict to store similarity mapping from movie to another and similarity
similarity = dict()
for m in movies.keys():
	similarity[m] = dict()

# calculate similarity with movie1 and movie2 and number of common users
def cal_similarity(movies, means, m1, m2):
	# find the intersection set of users who have watched both movies
	common_users = set(movies[m1].keys()).intersection(set(movies[m2].keys()))
	# return -2 as a marker indicating no enough common users
	if len(common_users) < user_thresh:
		return -2, 0
	# extract ratings from common users
	rating1 = []
	rating2 = []
	for u in common_users:
		rating1.append(movies[m1][u])
		rating2.append(movies[m2][u])
	# split the expression into 3 parts of sum and calculate them
	diff_prod_sum = 0
	diff_sq_sum1 = 0
	diff_sq_sum2 = 0
	for r1, r2 in zip(rating1, rating2):
		diff_prod_sum += (r1 - means[m1]) * (r2 - means[m2])
		diff_sq_sum1 += (r1 - means[m1]) ** 2
		diff_sq_sum2 += (r2 - means[m2]) ** 2
	# return -2 if denominator is 0 which means the similarity is unreliable
	if diff_sq_sum1 * diff_sq_sum2 == 0:
		return -2, 0
	# return result by combining 3 parts and also return number of common users
	return diff_prod_sum / math.sqrt(diff_sq_sum1 * diff_sq_sum2), len(common_users)

# generate similarity results between each pair of movies
for m1 in movies:
	for m2 in movies:
		# skip pair if its similarity has been calculated
		if m1 == m2 or m1 in similarity[m2]:
			continue
		sim, n_com = cal_similarity(movies, means, m1, m2)
		similarity[m1][m2] = sim, n_com
		similarity[m2][m1] = sim, n_com

# get result record string for a movie
def most_similar(similarity, movie):
	# initialize the max similarity as -2 as a marker of no reliable similarity
	max_sim = -2
	sim_movie = 0
	com_user = 0
	for m in similarity[movie].keys():
		# update current result if finding a higher similarity
		if similarity[movie][m][0] > max_sim:
			max_sim = similarity[movie][m][0]
			sim_movie = m
			com_user = similarity[movie][m][1]
	# return only the movie id itself if there is no reliable similarity
	if max_sim == -2:
		return "{}\n".format(movie)
	return "{} ({},{:.2f},{})\n".format(movie, sim_movie, max_sim, com_user)

# generate result records in order
results = []
for m in sorted(similarity.keys()):
	results.append(most_similar(similarity, m))

# record ending time
end_time = time.time()

# write results to file
with open(output_file, "w") as f:
	f.writelines(results)

# print information of processing given dataset
print("Input MovieLens file: {}".format(data_file))
print("Output file for similarity data: {}".format(output_file))
print("Minimum number of common users: {}".format(user_thresh))
print("Read {} lines with total of {} movies and {} users".format(n_data, n_movies, n_users))
print("Computed similarities in {:6f} seconds".format(end_time - start_time))
