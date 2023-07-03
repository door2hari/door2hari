# libraries to be imported
# https://towardsdatascience.com/keyword-extraction-with-bert-724efca412ea - ref of keyword extraction

from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import itertools
import json
import re
import openai
from transformers import pipeline

title = list()
summaries = list()
def max_sum_sim(doc_embedding, word_embeddings, words, top_n, nr_candidates):
    # Calculate distances and extract keywords
    distances = cosine_similarity(doc_embedding, word_embeddings)
    distances_candidates = cosine_similarity(word_embeddings,
                                            word_embeddings)

    # Get top_n words as candidates based on cosine similarity
    words_idx = list(distances.argsort()[0][-nr_candidates:])
    words_vals = [words[index] for index in words_idx]
    distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

    # Calculate the combination of words that are the least similar to each other
    min_sim = np.inf
    candidate = None
    for combination in itertools.combinations(range(len(words_idx)), top_n):
        sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
        if sim < min_sim:
            candidate = combination
            min_sim = sim

    return [words_vals[idx] for idx in candidate]



def Processing(a):
    global title,summaries
    title = list()
    summaries = list()
    doc = str(a)
    n_gram_range = (1, 1)
    stop_words = "english"
    # Extract candidate words/phrases
    count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([doc])
    candidates = count.get_feature_names_out()
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    doc_embedding = model.encode([doc])
    candidate_embeddings = model.encode(candidates)
    keys = max_sum_sim(doc_embedding, candidate_embeddings, candidates, top_n=3, nr_candidates=20)


    with open('MVA.json', encoding='utf-8') as fh:
        data = json.load(fh)
    #title = list()
    for j in keys:
        for i in data:
            temp = i
            flag = list()
            if (j in temp['title']):
                flag.append(temp['section'])
                flag.append(temp['title'])
                flag.append(temp['description'])
            if (len(flag) != 0):
                title.append(flag)
    print(title)
    summaries = list()
    # summarizer = pipeline('summarization')
    # for i in range(len(title)):
    #
    #     text = title[i][2]
    #     text = re.sub(r'\n', '', text)
    #     text = re.sub(r'[\[\]]', '', text)
    #
    #     length = len(text.split())
    #     sum = summarizer(text, max_length=length//2, min_length=length//3, do_sample=False, truncation=True)
    #     summaries.append(str(sum[0]['summary_text']))


        # openai.api_key = "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"
        # Set the string that will contain the summary

        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful research assistant."},
        #         {"role": "user", "content": f"Summarize this: {text} to about 50 words"},
        #     ],
        # )
        # page_summary = response["choices"][0]["message"]["content"]
        # summaries.append(page_summary)
    return len(title)

def all():
    return title

def sums(text):
    openai.api_key = "Your API KEY"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": f"Summarize this: {text} to about 50 words"},
        ],
    )
    page_summary = response["choices"][0]["message"]["content"]
    return page_summary

# input = "my husband is not giving me freedom. i want to get out from him" //No MVA
# input = "A car hit a pedestrian and did not stop" //Long - 12
# input = "Vehicle was on the zebra crossing when the traffic signal was red" // Medium - 8 --> Many Summarizations
#input = "A speeding car hit a pedestrian and did not stop" //Fast - 1
#input = "we were hit by a car eventhough we used signal indications."
#Processing(input)
