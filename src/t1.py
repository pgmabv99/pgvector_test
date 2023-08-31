print("ddd")


import openai
import os
import pandas as pd
import numpy as np
from numpy.linalg import norm
from sklearn.metrics.pairwise import cosine_similarity
import json
import tiktoken
import psycopg2
import ast
import pgvector
import math
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector

# Helper functions to help us create the embeddings

# Helper func: calculate number of tokens
def num_tokens_from_string(string: str, encoding_name = "cl100k_base") -> int:
    if not string:
        return 0
    # Returns the number of tokens in a text string
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# Helper function: calculate length of essay
def get_essay_length(essay):
    word_list = essay.split()
    num_words = len(word_list)
    return num_words

# Helper function: calculate cost of embedding num_tokens
# Assumes we're using the text-embedding-ada-002 model
# See https://openai.com/pricing
def get_embedding_cost(num_tokens):
    return num_tokens/1000*0.0001

# Helper function: calculate total cost of embedding all content in the dataframe
def get_total_embeddings_cost():
    total_tokens = 0
    for i in range(len(df.index)):
        text = df['content'][i]
        token_len = num_tokens_from_string(text)
        total_tokens = total_tokens + token_len
    total_cost = get_embedding_cost(total_tokens)
    return total_cost




openai.organization = "org-ahAnBcJ8PEbntuLXhBT35PIe"
openai.api_key = os.getenv("OPEN_API_KEY")
# print(openai.Model.list())
m_list=openai.Model.list()




# Load your CSV file into a pandas DataFrame
df = pd.read_csv('/postgres/pgvector_test/vector-cookbook/intro_langchain_pgvector/blog_posts_data.csv')
# print(df.head())

# quick check on total token amount for price estimation
# total_cost = get_total_embeddings_cost()
# print("estimated price to embed this content = $" + str(total_cost))



# Create new list with small content chunks to not hit max token limits
# Note: the maximum number of tokens for a single request is 8191
# https://openai.com/docs/api-reference/requests

# list for chunked content and embeddings
new_list = []
# Split up the text into token sizes of around 512 tokens
for i in range(len(df.index)):
    text = df['content'][i]
    token_len = num_tokens_from_string(text)
    if token_len <= 512:
        new_list.append([df['title'][i], df['content'][i], df['url'][i], token_len])
    else:
        # add content to the new list in chunks
        start = 0
        ideal_token_size = 512
        # 1 token ~ 3/4 of a word
        ideal_size = int(ideal_token_size // (4/3))
        end = ideal_size
        #split text by spaces into words
        words = text.split()

        #remove empty spaces
        words = [x for x in words if x != ' ']

        total_words = len(words)

        #calculate iterations
        chunks = total_words // ideal_size
        if total_words % ideal_size != 0:
            chunks += 1

        new_content = []
        for j in range(chunks):
            if end > total_words:
                end = total_words
            new_content = words[start:end]
            new_content_string = ' '.join(new_content)
            new_content_token_len = num_tokens_from_string(new_content_string)
            if new_content_token_len > 0:
                new_list.append([df['title'][i], new_content_string, df['url'][i], new_content_token_len])
            start += ideal_size
            end += ideal_size

# print(new_list)

# Helper function: get embeddings for a text
def get_embeddings(text):
   response = openai.Embedding.create(
       model="text-embedding-ada-002",
       input = text.replace("\n"," ")
   )
   embedding = response['data'][0]['embedding']
   return embedding


def av_comp(tx1:str , tx2:str ):
    ar1=np.array(get_embeddings(tx1))
    ar2=np.array(get_embeddings(tx2))
    cosine_sim=np.dot(ar1,ar2)/(norm(ar1)*norm(ar2))
    print("cosine_sim : " ,"{:.3f}".format(cosine_sim), tx1," <> ", tx2)





def av_test():
    tx_list=[]
    tx_list.append(" go home  ")
    tx_list.append(" go home  ")
    tx_list.append(" do not go home  ")
    tx_list.append(" go home now ")
    tx_list.append(" go home you dumb fuck ")
    tx_list.append(" lenin lived, lenin lives, lenin will live ")
    tx_list.append(" Ленин жил, Ленин живет, Ленин будет жить ")
    tx_list.append(" The value 1.3801640726581374e-05 represents a small decimal number in scientific notation. In scientific notation, e represents the exponent of 10 by which the preceding value")
    tx_list.append(" CI ocassionaly stuck running test001 b/c PP threadpool endlessly reschedules meta jobs, e.g. BATCH_PRIMITIVE_CREATE, which ByteStreams were somehow damaged or read out.JFYI this is a backport of the patch that resolves the issue for develop in CI.  ")

    for i in range (1, len(tx_list)):
        av_comp(tx_list[0],tx_list[i])

av_test()