from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
import time

class ProcessState(Enum):
    CREATED = "created"
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    TERMINATED = "terminated"

@dataclass
class Process:
    id: int
    name: str
    duration: int
    memory_size: int
    io_time: int
    state: ProcessState
    memory_address: Optional[int]
    remaining_time: int

@dataclass
class File:
    id: int
    name: str
    blocks: List[int]
    size: int

class OperatingSystem:
    def __init__(self):
        self.processes: Dict[int, Process] = {}
        self.files: Dict[str, File] = {}
        self.memory = {
            "total": 1024,  # MB
            "used": 0,
            "blocks": []
        }
        self.next_process_id = 1
        self.next_file_id = 1

    def create_process(self, name: str, duration: int, memory_size: int, io_time: int = -1) -> str:
        """创建新进程"""
        if self.memory["used"] + memory_size > self.memory["total"]:
            return "错误：内存不足，无法创建进程"

        process = Process(
            id=self.next_process_id,
            name=name,
            duration=duration,
            memory_size=memory_size,
            io_time=io_time,
            state=ProcessState.CREATED,
            memory_address=self.memory["used"],
            remaining_time=duration
        )

        self.memory["used"] += memory_size
        self.processes[process.id] = process
        self.next_process_id += 1

        return f"进程创建成功！进程ID: {process.id}"

    def kill_process(self, process_id: int) -> str:
        """终止进程"""
        if process_id not in self.processes:
            return "错误：进程不存在"

        process = self.processes[process_id]
        self.memory["used"] -= process.memory_size
        del self.processes[process_id]
        return f"进程 {process_id} 已终止"

    def list_processes(self) -> str:
        """列出所有进程"""
        if not self.processes:
            return "当前没有运行的进程"

        output = "进程列表：\n"
        for process in self.processes.values():
            output += f"ID: {process.id}, 名称: {process.name}, 状态: {process.state.value}, 内存地址: {process.memory_address}\n"
        return output

    def show_memory(self) -> str:
        """显示内存使用情况"""
        output = "内存使用情况：\n"
        output += f"总内存: {self.memory['total']}MB\n"
        output += f"已使用: {self.memory['used']}MB\n"
        output += f"空闲: {self.memory['total'] - self.memory['used']}MB\n"
        return output

    def create_file(self, name: str) -> str:
        """创建文件"""
        if name in self.files:
            return "错误：文件已存在"

        file = File(
            id=self.next_file_id,
            name=name,
            blocks=[],
            size=0
        )
        self.files[name] = file
        self.next_file_id += 1
        return f"文件 {name} 创建成功"

    def delete_file(self, name: str) -> str:
        """删除文件"""
        if name not in self.files:
            return "错误：文件不存在"

        del self.files[name]
        return f"文件 {name} 已删除"

    def list_file(self, name: str) -> str:
        """显示文件信息"""
        if name not in self.files:
            return "错误：文件不存在"

        file = self.files[name]
        return f"文件信息：\nID: {file.id}\n名称: {file.name}\n大小: {file.size}MB\n磁盘块: {file.blocks}"

    def get_process_status(self) -> List[Dict]:
        """获取进程状态（用于Web界面）"""
        return [
            {
                "id": process.id,
                "name": process.name,
                "state": process.state.value,
                "memory": process.memory_size
            }
            for process in self.processes.values()
        ]

    def get_file_status(self) -> List[Dict]:
        """获取文件状态（用于Web界面）"""
        return [
            {
                "id": file.id,
                "name": file.name,
                "size": file.size
            }
            for file in self.files.values()
        ]

    def get_memory_status(self) -> Dict:
        """获取内存状态（用于Web界面）"""
        return {
            "total": self.memory["total"],
            "used": self.memory["used"],
            "free": self.memory["total"] - self.memory["used"]
        } 