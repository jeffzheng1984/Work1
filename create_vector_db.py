import chromadb
from chromadb.config import Settings
import pandas as pd
import numpy as np

# 创建ChromDB客户端
#client = chromadb.Client(Settings(
#    chroma_db_impl="duckdb+parquet",
#    persist_directory=".chroma_db"  # 指定持久化目录
#))

client = chromadb.PersistentClient(path="db/")

# 创建或获取集合
collection = client.create_collection(name="test_cases")

# 加载处理后的测试案例
test_cases_df = pd.read_pickle('processed_test_cases.pkl')

# 准备数据
ids = [f"case_{i}" for i in range(len(test_cases_df))]
embeddings = [embedding.tolist() for embedding in test_cases_df['embedding']]
documents = test_cases_df['combined_text'].tolist()
metadatas = [{
    'title': row['title'],
    'source': 'manual_test_cases'
} for _, row in test_cases_df.iterrows()]

# 添加到集合
collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=documents,
    metadatas=metadatas
)

print("向量数据库创建完成")