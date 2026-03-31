# 配置文件

import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 知识库目录
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, 'knowledge_base')
if not os.path.exists(KNOWLEDGE_BASE_DIR):
    os.makedirs(KNOWLEDGE_BASE_DIR)

# 缓存目录
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# 数据库配置
DATABASE = os.path.join(BASE_DIR, 'quiz.db')

# 大模型配置
# Hugging Face Inference API 配置
HUGGING_FACE_API_KEY = ''  # 可选，某些模型需要API密钥
HUGGING_FACE_MODEL = 'google/flan-t5-base'  # 可以根据需要选择其他模型

# 豆包 API 配置（免费额度）
MODEL_PROVIDER = 'doubao'  # 可选：huggingface, doubao, deepseek, qwen
DOUBAO_API_KEY = ''  # 请在这里填入您的豆包API Key
DOUBAO_API_URL = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
DOUBAO_MODEL = 'ep-20260331122832-78s7h'

# OpenAI API 配置（用于 LangChain）
OPENAI_API_KEY = ''  # 请在这里填入您的 OpenAI API Key
OPENAI_MODEL = 'gpt-3.5-turbo'

# 本地模型配置
LOCAL_MODEL_PATH = ''  # 如果使用本地模型，设置模型路径

# 题目生成配置
QUESTION_TYPES = ['question', 'judgment', 'multiple_choice']  # 问答题、判断题、选择题

# 评分配置
SCORE_THRESHOLD = 0.6  # 及格分数阈值

# 推荐算法配置
FEYNMAN_LEARNING_PARAMS = {
    'initial_interval': 1,  # 初始复习间隔（天）
    'interval_multiplier': 2,  # 间隔倍增系数
    'difficulty_weight': 0.7,  # 难度权重
    'error_weight': 0.8,  # 错误权重
    'importance_weight': 0.5  # 重要性权重
}

# 应用配置
DEBUG = True
SECRET_KEY = 'dev'  # 生产环境应使用更复杂的密钥
