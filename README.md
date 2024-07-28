# WCloud-py 庫

1:下載：
```
  pip install git+https://github.com/wangtry/WCloud.git
```
2:引入及初始化：
```
from wcloud import WcloudServer

# 創建服務器
server = WcloudServer(host="0.0.0.0", port=3550)
```
3:上傳檔案：
```
# 上傳文件
server.upload("test.py", "test.py")
```
4:下載檔案：
```
# 下載文件
server.download("test.py", "downloaded_test.py")
```
