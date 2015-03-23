# TODO LIST

### Tasks
1. ~~创建Scrapy工程~~
1. ~~构建Item数据结构~~
1. ~~构建Pipeline框架~~
1. ~~完成以name为关键字的搜索结果页获取~~
1. ~~完成搜索结果页的解析~~
1. ~~构造MP3资源地址列表~~
1. 下载并保存资源

### Problems
* ~~MP3资源文件源地址分析~~

通过搜索列表获取到每篇Podcast的标题（title）

标题的URL编码

%e5%95%86%e4%b8%9a%e4%bb%b7%e5%80%bc07%ef%bc%9a%e6%8b%af%e6%95%91Hello+Kitty

对比资源地址

http://dl.justing.com.cn/page/%E5%95%86%E4%B8%9A%E4%BB%B7%E5%80%BC07%EF%BC%9A%E6%8B%AF%E6%95%91HelloKitty.mp3

得出

编码规则：URL编码，但空格在编码前被消除

编码公式：http://dl.justing.com.cn/page/ + url_code( remove_space(title) )

* 文件的下载与保存
