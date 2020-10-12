import networkx as nx
from node2vec import Node2Vec

# FILES
EMBEDDING_FILENAME = './embeddings.txt'
EMBEDDING_MODEL_FILENAME = './embeddings.model'

# Create a graph
#graph = nx.fast_gnp_random_graph(n=100, p=0.5)
graph = nx.karate_club_graph()
# Precompute probabilities and generate walks
node2vec = Node2Vec(graph, dimensions=300, walk_length=30, num_walks=200, workers=4)
# Embed
model = node2vec.fit(window=10, min_count=1, batch_words=4)  # Any keywords acceptable by gensim.Word2Vec can be passed, `diemnsions` and `workers` are automatically passed (from the Node2Vec constructor)
# Save embeddings for later use
model.wv.save_word2vec_format(EMBEDDING_FILENAME)
s = model.wv.syn0
print(type(s))
# Save model for later use
model.save(EMBEDDING_MODEL_FILENAME)
