# Gunicorn配置文件
import multiprocessing

# 监听地址和端口
bind = "0.0.0.0:5000"

# 工作进程数（建议CPU核心数*2 + 1）
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = "sync"

# 每个工作进程的线程数
threads = 2

# 最大客户端并发数
worker_connections = 1000

# 进程名称
proc_name = "abc_backend"

# 超时时间（秒）
timeout = 120

# 优雅重启超时时间
graceful_timeout = 30

# 访问日志
accesslog = "/var/log/abc_backend/access.log"

# 错误日志
errorlog = "/var/log/abc_backend/error.log"

# 日志级别
loglevel = "info"

# 守护进程模式（后台运行）
daemon = False

# PID文件路径
pidfile = "/var/run/abc_backend.pid"

# 预加载应用代码
preload_app = True
