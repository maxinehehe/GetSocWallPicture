#GetSocWallPicture
## 通过简单的python知识 爬取 <a href="http://www.socwall.com">social wallpapering</a> 网站的图片
【默认下载图片290x260】<br />
**GetSocallPic.py为初级版本只能下载290x260** <br />
**GetSocallPic_plus.py为升级版本可以选择下载，即可以下载高清版本**<br />
## 使用
##首先要确定有以下这些包
```python
import requests, re, time, urllib, os
from lxml import etree
import platform
```
**git clone https://github.com/maxinehehe/GetSocWallPicture.git** <br />
**GetSocallPic.py或者 运行GetSocallPic_plus.py**<br />
**另外也可以通过pyinstaller.py工具打包成 .exe 文件运行**  <br />
