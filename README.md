﻿> 系统：64x系统，我一般都用ubuntu ， 其他系统应该不影响脚本运行，但是环境部署可能需要调整，下面以ubuntu为例

- 安装mysql，设置用户名，密码(本地数据库运行最快)
apt install -y mysql-server
- 安装tmux（我习惯用这个，screen也一样）
apt install -y tmux
- 安装python集成开发环境
wget --no-check-certificate https://raw.githubusercontent.com/hexiaoya/scrapy_58/master/anaconda3.sh && bash anaconda3.sh
- 新建一个tmux窗口进行操作
tmux （新建）
tmux a（能够重新连入这个窗口）

- 安装python依赖
pip install pymysql

- 将三个py文件放到任意目录中

- 修改config.py内容
主要包括DB_开头的四个为本地数据库连接参数
可以修改每个分类读取的页数 FENLEI_PAGE_READ 为一个 <60 的数（越大每个分类读的越全，但是有很多老旧数据，看情况取）

- 初始化数据库
python init.py
没特殊需求这步只需执行一次，以后再执行会清空数据库，建议初始化后删除该文件

- 运行脚本开跑
while true; do python run58.py; done


> 58爬取中会有滑动验证码，见img1.png与img.png，在同IP下运行pic_code.py自动处理滑动验证码

- pic_code.py 使用selenium自动化模拟浏览器，安装配置过程此处略
