import pandas as pd
import numpy as np
def load_embeddings():
    a_datamatrix = pd.read_csv("embeddings.txt", delimiter=' ', skiprows = 1, header=None)
    sorted_a_datamatrix = a_datamatrix.sort_values(a_datamatrix.columns[0], ascending = True).to_numpy()
    data = np.delete(sorted_a_datamatrix, 0, axis = 1)
    n_nodes, embedding_dim = data.shape
    print('number of nodes', n_nodes )
    print('embedding dimensions', embedding_dim)
    return data, n_nodes, embedding_dim
