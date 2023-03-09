# 实验环境
## requirements
- python 3.x
- php 7.x
- sklearn
- [php-parser](https://github.com/nikic/PHP-Parser)

## install

```sh
$ compsoer install
$ pip install -r requirements.txt
```




# 数据集
## webshell

- https://github.com/tennc/webshell.git
- https://github.com/xl7dev/WebShell.git
- https://github.com/ysrc/webshell-sample.git
- https://github.com/tanjiti/webshellSample.git
- https://github.com/BlackArch/webshells.git.git

## whitecode

- https://github.com/LavaLite/cms.git
- https://github.com/top-think/framework.git
- https://github.com/WordPress/WordPress.git
- https://github.com/yiisoft/yii2.git


# 使用
## 生成AST并提取节点
使用`GenASTBoW.php`脚本将php文件进行转化

```shell
$ php GenASTBoW.php /path/to/phpfile
```


## 将数据批量生成AST
使用`TransformToASTBoW.py`将收集的正常代码和webshell分别提取出AST的所有节点到`webshellBoW`和`whitecodeBoW`文件夹


## 数据清洗
这里只做了简单的数据清洗处理，将空文件或者只包含`html`标签的文件清除

~~本打算做一个随机数据分割，分别用于训练和测试，但写完后发现sklearn本身支持数据的分割...~~


## 训练
使用`train.py`对之前生成的BoW文件进行提取和训练

可以通过传递参数修改`MLP`的激励函数和优化模型参数的算法，以及修改`KNN`的`K`值


## 训练模型存储
使用`pickle`库对已经训练好的模型进行序列化存储，以供后续对训练好的模型的利用。在`train.py`中的`store_model`函数有具体实现。训练好的模型存储在`*_model`文件夹下


## 模型利用
将要检测的php文件内容写入`test.php`，运行`predictByTrainedModel.py`对其进行检测，也可以对`predict`函数传入路径参数来指定要检测文件的路径
