import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import re

# 加载嵌入模型
# model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 连接向量数据库
#client = chromadb.Client(Settings(
#    chroma_db_impl="duckdb+parquet",
#    persist_directory=".chroma_db"  # 指定持久化目录
#))

client = chromadb.PersistentClient(path="db/")

collection = client.get_collection(name="test_cases")

def preprocess_query(query):
    """预处理查询文本"""
    query = re.sub(r'[^\w\u4e00-\u9fff\s]', ' ', query)
    query = query.lower()
    query = re.sub(r'\s+', ' ', query).strip()
    return query

def retrieve_similar_cases(query, n_results=5):
    """检索相似测试案例"""
    # 预处理查询
    processed_query = preprocess_query(query)
    
    # 生成查询嵌入
    query_embedding = model.encode([processed_query]).tolist()
    
    # 执行查询
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    return results

# 示例查询
if __name__ == "__main__":
    query = "信用卡功能，包括成功和失败情况"
    results = retrieve_similar_cases(query)
    
    print(f"查询: {query}")
    print("\n最相关的测试案例:")
    for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        print(f"\n{i+1}. {meta['title']}")
        print(f"   内容: {doc[:1000]}...")  # 只显示前1000个字符

    # 保存结果到 Markdown 文件
    with open("query_results.md", "w", encoding="utf-8") as f:
        f.write(f"# 查询: {query}\n\n")
        f.write("## 最相关的测试案例:\n")
        for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
            f.write(f"\n### {i+1}. {meta['title']}\n")
            f.write(f"**内容:**\n\n{doc}\n")