from gensim.models import KeyedVectors
import time


# Get the time at the beginning of the load
start_time = time.time()
print(time.ctime(start_time))

# Load the model file
loaded_model = KeyedVectors.load_word2vec_format('~/Documents/glove_word2vec/word2vec.840B.300d.txt')

# Get the time at the end of the load and calculate how long it took
end_time = time.time()
print(time.ctime(end_time))
elapsed_time = end_time - start_time

print('Loaded model file in '+str(elapsed_time/60.0)+' minutes')

# Get most similar words to "day"
word1 = loaded_model.get_vector('day')
# print(word1)
print(loaded_model.most_similar(positive=['day']))
