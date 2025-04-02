from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# 模拟系统状态
system_state = {
    'processes': [],
    'memory': {
        'total': 1024,  # 总内存1024MB
        'used': 0,
        'free': 1024
    },
    'files': []
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(data):
    command = data['command']
    result = process_command(command)
    emit('command_result', {'result': result})
    emit('update_status', system_state)

def process_command(command):
    parts = command.split()
    if not parts:
        return "请输入有效命令"
    
    cmd = parts[0]
    
    if cmd == 'creatproc':
        if len(parts) < 4:
            return "creatproc 命令需要至少3个参数：进程名称、运行时长、内存需求大小"
        name = parts[1]
        duration = int(parts[2])
        memory = int(parts[3])
        io_time = -1
        if len(parts) > 4:
            io_time = int(parts[4])
        
        # 创建新进程
        new_process = {
            'id': len(system_state['processes']) + 1,
            'name': name,
            'state': '就绪',
            'memory': memory,
            'duration': duration,
            'io_time': io_time
        }
        system_state['processes'].append(new_process)
        system_state['memory']['used'] += memory
        system_state['memory']['free'] -= memory
        
        return f"进程 {name} 创建成功，ID: {new_process['id']}"
    
    elif cmd == 'killproc':
        if len(parts) < 2:
            return "killproc 命令需要进程ID参数"
        pid = int(parts[1])
        
        # 查找并终止进程
        for process in system_state['processes']:
            if process['id'] == pid:
                system_state['memory']['used'] -= process['memory']
                system_state['memory']['free'] += process['memory']
                system_state['processes'].remove(process)
                return f"进程 {pid} 已终止"
        return f"未找到进程 {pid}"
    
    elif cmd == 'psproc':
        if not system_state['processes']:
            return "当前没有运行中的进程"
        result = "进程列表：\n"
        for process in system_state['processes']:
            result += f"ID: {process['id']}, 名称: {process['name']}, 状态: {process['state']}, 内存: {process['memory']}MB\n"
        return result
    
    elif cmd == 'mem':
        return f"内存使用情况：\n总内存: {system_state['memory']['total']}MB\n已使用: {system_state['memory']['used']}MB\n空闲: {system_state['memory']['free']}MB"
    
    elif cmd == 'creatfile':
        if len(parts) < 2:
            return "creatfile 命令需要文件名参数"
        filename = parts[1]
        
        # 创建新文件
        new_file = {
            'id': len(system_state['files']) + 1,
            'name': filename,
            'size': random.randint(1, 100)  # 随机文件大小
        }
        system_state['files'].append(new_file)
        return f"文件 {filename} 创建成功"
    
    elif cmd == 'deletefile':
        if len(parts) < 2:
            return "deletefile 命令需要文件名参数"
        filename = parts[1]
        
        # 删除文件
        for file in system_state['files']:
            if file['name'] == filename:
                system_state['files'].remove(file)
                return f"文件 {filename} 已删除"
        return f"未找到文件 {filename}"
    
    elif cmd == 'lsfile':
        if not system_state['files']:
            return "当前没有文件"
        result = "文件列表：\n"
        for file in system_state['files']:
            result += f"ID: {file['id']}, 名称: {file['name']}, 大小: {file['size']}MB\n"
        return result
    
    else:
        return "未知命令，请查看帮助信息"

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080) 