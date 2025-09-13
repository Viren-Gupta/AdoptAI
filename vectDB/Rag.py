import VectorStore as vs
import numpy as np

class Rag:

    def __init__(self):
        self.vocabulary = set()
        self.word_to_index = {}
        self.vector_store = vs.VectorStore()

    def initRag(self):
        # Establish a VectorStore instance

        dataFile = []

        for i in range(1, 4):
            fileName = "code snippets/snippet_" + str(i) + ".txt"
            with open(fileName, 'r') as file:
                content = file.read()
                dataFile.append(content)


        for data in dataFile:  #
            tokens = data.lower().split()  # Tokenizing the sentence by splitting on whitespace and converting to lowercase
            self.vocabulary.update(tokens)

        # Assign unique indices to vocabulary words
        self.word_to_index = {word: i for i, word in enumerate(self.vocabulary)}

        # Vectorization
        total_vectors = {}
        for data in dataFile:
            tokens = data.lower().split()
            vector = np.zeros(len(self.vocabulary))
            for token in tokens:
                vector[self.word_to_index[token]] += 1
            total_vectors[data] = vector  # Storing the vector for the data in the dictionary

        # Store in VectorStore
        for data, vector in total_vectors.items():
            self.vector_store.add_vector(data, vector)

    def getSimilarContent(self, query):
        # Similarity Search
        query_vector = np.zeros(len(self.vocabulary))
        query_tokens = query.lower().split()
        for token in query_tokens:
            if token in self.word_to_index:
                query_vector[self.word_to_index[token]] += 1

        similar_data = self.vector_store.find_similar_vectors(query_vector, num_results=3)

        # Display similar sentences
        print("Query data:", query)
        print("Similar data:")
        for sentence, similarity in similar_data:
            print(f"{sentence}: Similarity = {similarity:.4f}")
        return similar_data[0]

