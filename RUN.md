# 每日问答小工具运行指南

## 运行步骤

### 1. 检查Python环境
确保您的系统已安装Python 3.8或更高版本。可以通过以下命令检查：
```bash
python --version
```

### 2. 安装依赖
进入项目目录并安装所需依赖：
```bash
# 进入答题目录
cd 技能树/答题

# 安装依赖
pip install -r requirements.txt
```

### 3. 启动应用
在答题目录中运行Flask应用：
```bash
python app.py
```

### 4. 访问应用
启动成功后，在浏览器中访问以下地址：
```
http://127.0.0.1:5000
```

## 运行状态检查

当您运行`python app.py`后，应该会看到类似以下的输出：
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 129-385-409
```

这表示应用已经成功启动，并且在本地5000端口运行。

## 常见问题解决

### 1. 依赖安装失败
- 确保使用的是Python 3.8或更高版本
- 尝试使用`pip install --user`来安装依赖
- 检查网络连接是否正常

### 2. 端口被占用
- 尝试修改`app.py`中的端口号
- 或者关闭占用5000端口的其他应用

### 3. 大模型API调用失败
- 检查网络连接
- 可以在`config.py`中配置本地模型，避免依赖外部API

### 4. 文档上传失败
- 确保上传的文件格式正确（支持md、txt格式）
- 检查文件大小是否合理
- 查看服务器日志了解具体错误信息

## 使用流程

1. **导入知识库**：点击"导入知识库"按钮，上传您的学习资料
2. **开始答题**：点击"开始答题"按钮，系统会基于知识库生成题目
3. **提交答案**：输入答案后点击"提交答案"，系统会判分并生成解析
4. **查看解析**：点击"查看详细解析"展开详细的答案分析
5. **继续答题**：点击"下一题"继续答题

祝您使用愉快！