import pandas as pd
import re
from sentence_transformers import SentenceTransformer

# 1. 加载数据
def load_test_cases(file_path):
    """根据文件类型加载测试案例"""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        # 如果是文本文件，需要自定义解析逻辑
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # 这里需要根据你的文本格式编写解析逻辑
        # 假设每行是一个测试用例，用制表符分隔字段
        cases = []
        for line in content.split('\n'):
            if line.strip():
                parts = line.split('\t')
                cases.append({
                    'id': parts[0],
                    'title': parts[1],
                    'steps': parts[2],
                    'expected_result': parts[3]
                })
        return pd.DataFrame(cases)

# 2. 清理和预处理文本
def preprocess_text(text):
    """清理和标准化文本"""
    if pd.isna(text):
        return ""
    # 移除非字母数字字符（保留中文）
    text = re.sub(r'[^\w\u4e00-\u9fff\s]', ' ', str(text))
    # 转换为小写
    text = text.lower()
    # 移除多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 3. 准备嵌入模型
def load_embedding_model():
    """加载句子转换模型"""
    # 使用一个轻量级模型进行概念验证
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    # 使用清华镜像站下载
    # model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./models', mirrors=['https://mirrors.tuna.tsinghua.edu.cn/huggingface-models'])
    return model

# 4. 生成嵌入向量
def generate_embeddings(model, texts):
    """为文本列表生成嵌入向量"""
    return model.encode(texts)

# 主函数
def main():
    # 加载测试案例
    test_cases_df = load_test_cases('sample_test_cases.csv')
    
    # 预处理文本 - 合并所有相关信息到一个字段
    test_cases_df['combined_text'] = (
        test_cases_df['title'].apply(preprocess_text) + " " +
        test_cases_df['steps'].apply(preprocess_text) + " " +
        test_cases_df['expected_result'].apply(preprocess_text)
    )
    
    # 加载嵌入模型
    model = load_embedding_model()
    
    # 生成嵌入向量
    embeddings = generate_embeddings(model, test_cases_df['combined_text'].tolist())
    
    # 将嵌入向量添加回DataFrame
    test_cases_df['embedding'] = list(embeddings)
    
    # 保存处理后的数据
    test_cases_df.to_pickle('processed_test_cases.pkl')
    print(f"处理完成，共{len(test_cases_df)}个测试案例")

if __name__ == "__main__":
    main()