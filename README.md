# WCloud-py 庫

1:下載：
``` bash
  pip install git+https://github.com/wangtry/WCloud.git
```
2:引入及初始化：
``` python
from wcloud import WcloudServer

# 創建服務器
server = WcloudServer(host="0.0.0.0", port=3550)
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
5:運行代碼：
``` python
from wcloud import WcloudRunner

runner = WcloudRunner(host="0.0.0.0", port=3550)
result = runner.run_script("test.py")
print(result)
```
