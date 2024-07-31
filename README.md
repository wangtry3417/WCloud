# WCloud-py 庫

wcloud 是一個基於docker的庫，主要用於雲端儲存服務。 

1:下載：
``` bash
  pip install git+https://github.com/wangtry/WCloud.git
```
2:引入及初始化：
``` python
from wcloud import createServer

# 創建服務器
server = createServer(host="0.0.0.0", port=3550)
```
3:上傳檔案：
``` python
# 上傳文件
server.upload("test.py", "test.py")
```
4:下載檔案：
``` python
# 下載文件
server.download("test.py", "downloaded_test.py")
```
5:在虛擬機上運行代碼：
``` python
from wcloud import WcloudRunner

runner = WcloudRunner(host="0.0.0.0", port=3550)
result = runner.run_script("test.py")
print(result)
```
6:運行完整示例：
``` python
from wcloud import WcloudServer, WcloudRunner

class WcloudApp(WcloudServer):
    def __init__(self, host="0.0.0.0", port=3550):
        super().__init__(host, port)
        self.runner = WcloudRunner(host, port)

    def run_script(self, script_path):
        return self.runner.run_script(script_path)

    def start(self):
        self.run_server()

if __name__ == "__main__":
    app = WcloudApp()
    app.start()
```
