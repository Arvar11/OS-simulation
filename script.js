// 系统状态
const systemState = {
    processes: new Map(), // 进程表
    memory: {
        total: 1024, // 总内存大小（MB）
        used: 0,     // 已使用内存
        blocks: []   // 内存块列表
    },
    files: new Map(),    // 文件系统
    nextProcessId: 1,    // 下一个进程ID
    nextFileId: 1       // 下一个文件ID
};

// 进程状态枚举
const ProcessState = {
    CREATED: 'created',
    READY: 'ready',
    RUNNING: 'running',
    BLOCKED: 'blocked',
    TERMINATED: 'terminated'
};

// 进程类
class Process {
    constructor(name, duration, memorySize, ioTime) {
        this.id = systemState.nextProcessId++;
        this.name = name;
        this.duration = duration;
        this.memorySize = memorySize;
        this.ioTime = ioTime;
        this.state = ProcessState.CREATED;
        this.memoryAddress = null;
        this.remainingTime = duration;
    }
}

// 文件类
class File {
    constructor(name) {
        this.id = systemState.nextFileId++;
        this.name = name;
        this.blocks = []; // 文件占用的磁盘块
        this.size = 0;
    }
}

// 命令处理函数
const commands = {
    creatproc: (args) => {
        if (args.length < 3) {
            return '错误：参数不足。用法：creatproc <进程名称> <运行时长> <内存需求大小> [I/O起始停止时间/-1]';
        }
        
        const [name, duration, memorySize, ioTime = -1] = args;
        const process = new Process(name, parseInt(duration), parseInt(memorySize), parseInt(ioTime));
        
        // 分配内存
        if (!allocateMemory(process)) {
            return '错误：内存不足，无法创建进程';
        }
        
        systemState.processes.set(process.id, process);
        updateProcessStatus();
        return `进程创建成功！进程ID: ${process.id}`;
    },
    
    killproc: (args) => {
        if (args.length < 1) {
            return '错误：请指定进程ID';
        }
        
        const processId = parseInt(args[0]);
        const process = systemState.processes.get(processId);
        
        if (!process) {
            return '错误：进程不存在';
        }
        
        // 释放内存
        freeMemory(process);
        systemState.processes.delete(processId);
        updateProcessStatus();
        return `进程 ${processId} 已终止`;
    },
    
    psproc: () => {
        let output = '进程列表：\n';
        systemState.processes.forEach(process => {
            output += `ID: ${process.id}, 名称: ${process.name}, 状态: ${process.state}, 内存地址: ${process.memoryAddress}\n`;
        });
        return output;
    },
    
    mem: () => {
        let output = '内存使用情况：\n';
        output += `总内存: ${systemState.memory.total}MB\n`;
        output += `已使用: ${systemState.memory.used}MB\n`;
        output += `空闲: ${systemState.memory.total - systemState.memory.used}MB\n`;
        return output;
    },
    
    creatfile: (args) => {
        if (args.length < 1) {
            return '错误：请指定文件名';
        }
        
        const fileName = args[0];
        if (systemState.files.has(fileName)) {
            return '错误：文件已存在';
        }
        
        const file = new File(fileName);
        systemState.files.set(fileName, file);
        updateFileStatus();
        return `文件 ${fileName} 创建成功`;
    },
    
    deletefile: (args) => {
        if (args.length < 1) {
            return '错误：请指定文件名';
        }
        
        const fileName = args[0];
        if (!systemState.files.has(fileName)) {
            return '错误：文件不存在';
        }
        
        systemState.files.delete(fileName);
        updateFileStatus();
        return `文件 ${fileName} 已删除`;
    },
    
    lsfile: (args) => {
        if (args.length < 1) {
            return '错误：请指定文件名';
        }
        
        const fileName = args[0];
        const file = systemState.files.get(fileName);
        
        if (!file) {
            return '错误：文件不存在';
        }
        
        return `文件信息：\nID: ${file.id}\n名称: ${file.name}\n大小: ${file.size}MB\n磁盘块: ${file.blocks.join(', ')}`;
    }
};

// 内存管理函数
function allocateMemory(process) {
    if (systemState.memory.used + process.memorySize > systemState.memory.total) {
        return false;
    }
    
    process.memoryAddress = systemState.memory.used;
    systemState.memory.used += process.memorySize;
    return true;
}

function freeMemory(process) {
    systemState.memory.used -= process.memorySize;
}

// 更新状态显示
function updateProcessStatus() {
    const processStatus = document.getElementById('process-status');
    processStatus.innerHTML = '';
    systemState.processes.forEach(process => {
        const processElement = document.createElement('div');
        processElement.className = 'process-item';
        processElement.innerHTML = `
            <p>ID: ${process.id}</p>
            <p>名称: ${process.name}</p>
            <p>状态: ${process.state}</p>
            <p>内存: ${process.memorySize}MB</p>
        `;
        processStatus.appendChild(processElement);
    });
}

function updateFileStatus() {
    const fileStatus = document.getElementById('file-status');
    fileStatus.innerHTML = '';
    systemState.files.forEach(file => {
        const fileElement = document.createElement('div');
        fileElement.className = 'file-item';
        fileElement.innerHTML = `
            <p>ID: ${file.id}</p>
            <p>名称: ${file.name}</p>
            <p>大小: ${file.size}MB</p>
        `;
        fileStatus.appendChild(fileElement);
    });
}

// 命令行处理
const commandInput = document.getElementById('command-input');
const output = document.getElementById('output');

commandInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const command = commandInput.value.trim();
        output.innerHTML += `<div class="command">$ ${command}</div>`;
        
        const [cmd, ...args] = command.split(' ');
        const commandHandler = commands[cmd];
        
        if (commandHandler) {
            const result = commandHandler(args);
            output.innerHTML += `<div class="result">${result}</div>`;
        } else {
            output.innerHTML += `<div class="error">错误：未知命令 ${cmd}</div>`;
        }
        
        commandInput.value = '';
        output.scrollTop = output.scrollHeight;
    }
});

// 初始化显示
updateProcessStatus();
updateFileStatus(); 