# 操作系统模拟程序

这是一个基于Web的操作系统模拟程序，用于模拟操作系统的基本功能，包括进程管理、内存管理和文件系统。

## 功能特点

- 进程管理：创建、终止、查看进程状态
- 内存管理：分配和回收内存
- 文件系统：创建、删除、查看文件信息
- 实时状态更新
- 交互式命令行界面

## 运行说明

### 1. 环境要求
- Python 3.8 或更高版本
- pip（Python包管理器）

### 2. 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone [项目地址]
   cd newOS3
   ```

2. **安装依赖包**
   ```bash
   # 使用默认pip源安装
   pip install -r requirements.txt
   
   # 如果安装速度慢，可以使用国内镜像源
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. **运行程序**
   ```bash
   python app.py
   ```

4. **访问程序**
   - 打开浏览器
   - 访问地址：`http://localhost:8080` 或 `http://127.0.0.1:8080`

### 3. 常见问题解决

1. **端口被占用**
   - 如果8080端口被占用，可以修改 `app.py` 中的端口号
   - 例如改为3000端口：
   ```python
   socketio.run(app, debug=True, host='0.0.0.0', port=3000)
   ```

2. **依赖包安装失败**
   - 确保pip已更新到最新版本：
   ```bash
   python -m pip install --upgrade pip
   ```
   - 如果出现权限问题，可以使用：
   ```bash
   pip install -r requirements.txt --user
   ```

3. **程序无法启动**
   - 检查Python版本是否满足要求：
   ```bash
   python --version
   ```
   - 检查是否所有依赖包安装成功：
   ```bash
   pip list
   ```
   - 查看错误信息进行排查

### 4. 基本命令使用

1. **创建进程**
   ```
   creatproc 进程名称 运行时长 内存需求大小 [I/O起始停止时间/-1]
   ```
   示例：
   ```
   creatproc test1 100 64 -1
   ```

2. **终止进程**
   ```
   killproc 进程号
   ```
   示例：
   ```
   killproc 1
   ```

3. **查看进程状态**
   ```
   psproc
   ```

4. **查看内存使用情况**
   ```
   mem
   ```

5. **创建文件**
   ```
   creatfile 文件名
   ```
   示例：
   ```
   creatfile test.txt
   ```

6. **删除文件**
   ```
   deletefile 文件名
   ```
   示例：
   ```
   deletefile test.txt
   ```

7. **查看文件信息**
   ```
   lsfile 文件名
   ```
   示例：
   ```
   lsfile test.txt
   ```

### 5. 开发环境说明

- 操作系统：Linux/Windows/MacOS
- Python版本：3.8+
- Web框架：Flask 2.0.1
- 前端技术：HTML5, CSS3, JavaScript
- 通信协议：WebSocket

## 项目结构

```
newOS3/
├── app.py              # 主程序入口
├── os_simulator.py     # 操作系统模拟器核心代码
├── requirements.txt    # 项目依赖包列表
├── static/            # 静态资源文件
│   ├── css/
│   └── js/
└── templates/         # HTML模板文件
    └── index.html
```

## 注意事项

1. 确保Python环境正确安装
2. 安装依赖包时可能需要管理员权限
3. 如果使用虚拟环境，请先激活虚拟环境
4. 确保防火墙不会阻止程序访问网络
5. 建议使用现代浏览器（Chrome、Firefox、Edge等）访问

## 技术支持

如果遇到问题，请检查：
1. Python版本是否满足要求
2. 所有依赖包是否正确安装
3. 端口是否被占用
4. 网络连接是否正常
5. 浏览器控制台是否有错误信息 