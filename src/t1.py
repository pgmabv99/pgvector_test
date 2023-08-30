print("ddd")


import openai
import os
import pandas as pd
import numpy as np
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
print(df.head())

# quick check on total token amount for price estimation
total_cost = get_total_embeddings_cost()
print("estimated price to embed this content = $" + str(total_cost))
