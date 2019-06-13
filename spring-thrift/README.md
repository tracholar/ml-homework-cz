## 利用thrift和spring搭建服务
- 利用thrift定义接口,并生成接口类java文件
- 实现服务端和客户端代码,要求完成以下功能
    - `ls(path)` 列出路径path下的所有文件,返回`list<file>`
    - `file`结构**至少**要包含以下数据
        - `path` 路径
        - `name` 文件名
        - `mime` 文件MIME类型
        - `size` 文件大小
        - `mode` 文件权限
    - `cat(path, mode)` 列出文件内容, `mode` 有两种类型文本和二进制,取值请使用thrift定义,如果是文本则直接输出文件内容, 如果是二进制则需要做16进制编码输出文本
    - `upload(name, data)` 上传文件
    - `download(path)` 下载文件
- 实现python版本的client段代码,client端代码上述函数都必须调用一次
- 服务端代码请使用spring框架实现, server的配置信息请使用XML文件配置
- 请使用spring 在client端提供上述4个方法的HTTP接口
- 请对server端每一个接口编写单元测试(用JUnit)

## 思考题
1. 为什么要使用thrift来定义接口,有什么好处?
2. thrift的序列化与JSON和XML序列化之间的差异和优劣是什么?
3. 用自己的话描述一下RPC和本地函数调用的关系与区别,请举一个例子进行描述
4. spring bean是什么? 请举例说明
5. junit 的@Before 和 @After有什么用途? 请在你的单元测试中使用一次


## 实现
- [tracholar](tracholar/)
- [getstart](getstart/)