### 运行
```
npm i
npm start
npm restart
npm stop
```

```sh
# 查看指定端口的占用情况
C:\>netstat -aon|findstr "9050"

# 查看PID对应的进程
C:\>tasklist|findstr "2016"

# 结束该进程
C:\>taskkill /f /t /im tor.exe
```