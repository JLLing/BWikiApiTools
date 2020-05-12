# BWikiApiTools
some demo with python to use bwiki's api



## 注意事项

请先将必需的参数写入 config.json 中：

```json
{
	"url": "https://wiki.biligame.com/xxxx/api.php", // 改为指定的api请求地址
	"cookie":"xxxx"                                  // 改为当前登录用户的cookie
}
```

> 如何获取 cookie ？
>
> 登录BWIKI后，打开浏览器开发者工具（F12）的网络（network）标签页，再刷新当前页面（F5），点击列表中的第一个请求，在右侧弹出的信息窗口中找到cookie一项，全部复制并粘入对应位置。

> 示例数据文件（已进行删减）均在data文件夹下，请修改路径并改写文件内容后再尝试。
> 请注意！从excel 导出 csv 文件后要检查 csv 文件有没有导出多余的空白列和空白行，暂时没有做数据检查。
> 可能还需要注意文件编码问题。



## Method


### getPageContent(title)
请求指定词条页面的数据。

```python
getPageContent("【书写崭新的2020】元旦微博活动获奖公示")
```



### updateWithCSV(fileName)

读取指定csv文件对wiki词条数据进行更新，其中：
    csv第一列为词条名，第二列为模板名；
    后面可以自定义数据列，并以第一行为列名为字段名（key）。
```python
updateWithCSV("闪耀WIKI-美甲模板5.1.csv")
updateWithCSV("闪耀wiki-设计师模板5.2.csv")
```



### addToCategory(category, title)

对指定词条添加分类标记。
```python
addToCategory("公告", "【书写崭新的2020】元旦微博活动获奖公示")
```



### addToCategoryWithCSV(category, filename)

读取指定csv文件，对文件中词条名（一行一个）对应的词条添加分类标记，
可通过 `特殊:未分类页面` 查看未分类页面。

```python
addToCategoryWithCSV("公告", "添加至公告分类的页面5.11.CSV")
```



### updateWithFolder(rootdir)

将指定文件夹中的所有txt写入（覆盖）进wiki指定词条，
文件名为词条名，文件内容为页面内容。

```python
print(updateWithFolder(r'C:\_project\SyLuaTw\wiki\story'))
```



### clearCache(titles)

清除指定页面的缓存，词条名以“|”分割。
```python
clearCache("阿欢|爱衣|茶薄荷|池小鱼|海")
```