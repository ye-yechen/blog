# 博客
`python|django|crawler`


博客地址：[blog](http://123.207.222.175/blog/)

**blog** 是基于 python 2.7 和 django 1.10 开发的博客系统,包含`注册登录、写文章、评论、标签云制作、文章归档`等常用功能,并包含一个`知乎用户数据爬虫`模块，使用 echarts 将分析的数据可视化展示。

- **标签云**：标签按被引用次数呈现不同大小和颜色。定义一个标签云类，设置了最大字体和最小字体以及默认的几种颜色，根据公式 `MIN_FONT_SIZE + n* step = MAX_FONT_SIZE` 算出 step，即为步长，其中，n 为标签引用次数最大值与最小值的差值。然后根据各标签实际使用的次数计算出此标签的大小`（最小字体+（实际引用次数-最小引用次数）* step）`以及相应的颜色。

- **评论功能**：采用了一种简单的处理方式，直接将对评论的回复保存为`“@作者+评论内容”`的形式直接和普通的评论保存在一起，只在评论或者回复评论的时候作了区别，js 代码实现在点击“回复”时在textarea域中自动填上“@”

- **部署**：部署环境为：ubuntu 16.04，apache

- **网站截图**：
![c1](https://github.com/creatorYC/blog/blob/master/image/c25.PNG)
![c2](https://github.com/creatorYC/blog/blob/master/image/c26.PNG)
![c3](https://github.com/creatorYC/blog/blob/master/image/c27.PNG)
---

### contact me:
- email: <1522120424@qq.com> <yechoor@gmail.com>
