import pandas as pd
from pinecone import Pinecone
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
import os

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("goodpen")
tfidf = TfidfVectorizer()
svd = TruncatedSVD(n_components=50)
df = pd.read_csv("src/utils/data.csv", dtype=str)
titles = df["title"].str.lower().tolist()
tfidf_vectors = tfidf.fit_transform(titles)
svd.fit_transform(tfidf_vectors)

def recommend_references(input_title, top_k):
    input_vector = list(svd.transform(tfidf.transform([input_title]))[0])
    recommended_indices = index.query(
        vector=input_vector,
        top_k=top_k
    )
    indices = []
    for idx in recommended_indices["matches"]:
        indices.append(int(idx["id"]))
    result = df.loc[indices][["id", "title", "update_date", "authors_parsed"]].to_dict(orient='records')
    return result