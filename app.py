# 主应用入口

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import sqlite3
import webbrowser
import threading
import time
import sys
from config import DATABASE, DEBUG, SECRET_KEY, KNOWLEDGE_BASE_DIR
from models.question import Question

app = Flask(__name__)
app.config['DEBUG'] = DEBUG
app.config['SECRET_KEY'] = SECRET_KEY

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # 创建知识库表
    c.execute('''
    CREATE TABLE IF NOT EXISTS knowledge_base (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建题目表
    c.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        question_type TEXT NOT NULL,
        options TEXT,
        correct_answer TEXT NOT NULL,
        knowledge_id INTEGER,
        difficulty INTEGER DEFAULT 1,
        importance INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (knowledge_id) REFERENCES knowledge_base (id)
    )
    ''')
    
    # 创建答案表
    c.execute('''
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER NOT NULL,
        user_answer TEXT NOT NULL,
        score REAL NOT NULL,
        feedback TEXT,
        is_correct INTEGER DEFAULT 0,
        answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# 主页
@app.route('/')
def index():
    return render_template('index.html')

# 文档上传页面
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # 处理文件上传
        files = request.files.getlist('files')
        from services.document_processor import DocumentProcessor
        processor = DocumentProcessor()
        
        for file in files:
            if file and (file.filename.endswith('.md') or file.filename.endswith('.txt')):
                # 保存文件
                filepath = os.path.join(KNOWLEDGE_BASE_DIR, file.filename)
                file.save(filepath)
                
                # 使用文档处理器处理文件
                try:
                    processor.process_file(filepath)
                except Exception as e:
                    print(f"处理文件失败: {e}")
        return redirect(url_for('index'))
    return render_template('upload.html')

# 答题页面
@app.route('/quiz')
def quiz():
    # 这里将实现题目推荐和显示逻辑
    return render_template('quiz.html')

# API: 获取题目
@app.route('/api/get_question', methods=['GET'])
def get_question():
    # 使用推荐服务获取推荐题目
    from services.recommendation import RecommendationService
    from services.question_generator import QuestionGenerator
    from models.knowledge_base import KnowledgeBase
    from models.question import Question
    
    recommendation_service = RecommendationService()
    question_generator = QuestionGenerator()
    knowledge_base = KnowledgeBase()
    question_model = Question()
    
    # 1. 尝试获取推荐题目（排除已答题目）
    recommended_question = recommendation_service.get_recommended_question()
    if recommended_question:
        return jsonify(recommended_question)
    
    # 2. 如果没有推荐题目，尝试获取未答过的题目
    # 获取所有题目
    all_questions = question_model.get_all()
    if all_questions:
        # 随机选择一个题目
        import random
        question = random.choice(all_questions)
        return jsonify(question)
    
    # 3. 如果没有题目，从知识库生成新题目
    knowledge_docs = knowledge_base.get_all()
    if knowledge_docs:
        # 随机选择一个文档
        import random
        doc = random.choice(knowledge_docs)
        # 生成题目
        question_type = random.choice(['question', 'judgment', 'multiple_choice'])
        question_id = question_generator.generate_question(doc['content'], question_type)
        # 获取生成的题目
        question = question_model.get_by_id(question_id)
        if question:
            return jsonify(question)
    
    # 4. 如果没有知识库，返回随机示例题目
    sample_questions = [
        {
            'id': 1,
            'content': '什么是TCP/IP协议栈？',
            'question_type': 'question',
            'options': None,
            'correct_answer': 'TCP/IP协议栈是一组网络协议的集合，包括TCP、IP等协议，用于实现网络通信'
        },
        {
            'id': 2,
            'content': 'HTTP协议是无状态的吗？',
            'question_type': 'judgment',
            'options': None,
            'correct_answer': '是'
        },
        {
            'id': 3,
            'content': '下列哪种协议是传输层协议？',
            'question_type': 'multiple_choice',
            'options': {
                'A': 'HTTP',
                'B': 'TCP',
                'C': 'IP',
                'D': 'DNS'
            },
            'correct_answer': 'B'
        },
        {
            'id': 4,
            'content': '什么是DNS？',
            'question_type': 'question',
            'options': None,
            'correct_answer': 'DNS是域名系统，用于将域名解析为IP地址'
        },
        {
            'id': 5,
            'content': 'MAC地址是网络层地址吗？',
            'question_type': 'judgment',
            'options': None,
            'correct_answer': '否'
        }
    ]
    import random
    question = random.choice(sample_questions)
    return jsonify(question)

# API: 提交答案
@app.route('/api/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    question_id = data.get('question_id')
    user_answer = data.get('user_answer')
    
    # 使用答案判分服务
    from services.answer_judger import AnswerJudger
    judger = AnswerJudger()
    
    # 判分答案
    judgment_result = judger.judge_answer(question_id, user_answer)
    if judgment_result:
        # 更新题目难度
        from services.recommendation import RecommendationService
        recommendation_service = RecommendationService()
        recommendation_service.update_question_difficulty(question_id, judgment_result['score'])
        
        return jsonify({
            'score': judgment_result['score'],
            'feedback': judgment_result['feedback'],
            'is_correct': judgment_result['is_correct'],
            'user_answer': user_answer
        })
    
    # 如果判分失败，返回默认结果
    result = {
        'score': 0,
        'feedback': '判分失败，请稍后重试',
        'is_correct': 0,
        'user_answer': user_answer
    }
    
    # 保存答案到数据库
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO answers (question_id, user_answer, score, feedback, is_correct) VALUES (?, ?, ?, ?, ?)', 
              (question_id, user_answer, result['score'], result['feedback'], result['is_correct']))
    conn.commit()
    conn.close()
    
    return jsonify(result)

# API: 删除题目
@app.route('/api/delete_question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    # 删除题目及其相关答案
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM answers WHERE question_id = ?', (question_id,))
    c.execute('DELETE FROM questions WHERE id = ?', (question_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

# API: 生成详细答案解析
@app.route('/api/generate_explanation', methods=['POST'])
def generate_explanation():
    data = request.get_json()
    question_id = data.get('question_id')
    selected_option = data.get('selected_option')
    
    if not question_id or not selected_option:
        return jsonify({'status': 'error', 'message': '缺少题目ID或选择的选项'}), 400
    
    try:
        # 获取题目信息
        print(f"获取题目信息，question_id: {question_id}, type: {type(question_id)}")
        # 确保 question_id 是整数
        try:
            question_id = int(question_id)
            print(f"转换后的 question_id: {question_id}, type: {type(question_id)}")
        except ValueError as e:
            print(f"question_id 转换失败: {e}")
            return jsonify({'status': 'error', 'message': f'题目ID格式错误: {question_id}'}), 400
        
        question_model = Question()
        question = question_model.get_by_id(question_id)
        print(f"获取到的题目: {question}")
        
        if not question:
            # 尝试获取所有题目，看看数据库中是否有题目
            all_questions = question_model.get_all()
            print(f"数据库中的所有题目数量: {len(all_questions)}")
            if all_questions:
                print(f"第一个题目: {all_questions[0]}")
            return jsonify({'status': 'error', 'message': f'题目不存在，question_id: {question_id}'}), 404
        
        # 生成详细解析
        from services.answer_judger import AnswerJudger
        judger = AnswerJudger()
        explanation = judger.generate_detailed_explanation(question, selected_option)
        
        return jsonify({'status': 'success', 'explanation': explanation})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# API: 获取知识库内容
@app.route('/api/get_knowledge_base', methods=['GET'])
def get_knowledge_base():
    try:
        from services.knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        knowledge_base = kb.get_all_content()
        return jsonify({'status': 'success', 'knowledge_base': knowledge_base})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # 检查是否是主进程（避免debug模式下子进程重复打开）
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        # 检查是否已经打开过浏览器
        browser_opened_file = os.path.join(os.path.dirname(__file__), 'browser_opened.txt')
        
        if not os.path.exists(browser_opened_file):
            # 启动浏览器的函数
            def open_browser():
                print("准备打开浏览器...")
                time.sleep(2)  # 等待2秒，确保服务器已经完全启动
                try:
                    print("正在打开浏览器...")
                    # 尝试使用系统默认命令打开浏览器
                    import subprocess
                    import sys
                    
                    if sys.platform == 'win32':
                        # Windows系统
                        print("使用Windows命令打开浏览器...")
                        subprocess.run(['start', 'http://127.0.0.1:5000'], shell=True)
                    elif sys.platform == 'darwin':
                        # macOS系统
                        print("使用macOS命令打开浏览器...")
                        subprocess.run(['open', 'http://127.0.0.1:5000'])
                    else:
                        # Linux系统
                        print("使用Linux命令打开浏览器...")
                        subprocess.run(['xdg-open', 'http://127.0.0.1:5000'])
                    
                    print("浏览器已打开，请访问: http://127.0.0.1:5000")
                    # 创建标记文件
                    with open(browser_opened_file, 'w') as f:
                        f.write('1')
                    print(f"已创建浏览器打开标记文件: {browser_opened_file}")
                except Exception as e:
                    print(f"打开浏览器失败: {e}")
                    import traceback
                    traceback.print_exc()
                    print("请手动打开浏览器，访问: http://127.0.0.1:5000")
            
            # 在后台线程中打开浏览器
            print("启动浏览器线程...")
            threading.Thread(target=open_browser).start()
        else:
            print("浏览器已经打开过，跳过...")
    else:
        print("子进程，跳过打开浏览器...")
    
    # 启动Flask应用
    app.run(debug=DEBUG)
