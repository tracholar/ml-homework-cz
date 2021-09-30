# 推荐系统
## 总体架构
- 包括以下子模块：
    - API层：负责渲染
    - engine层：负责召排引擎
      - 召回层：各种召回策略
      - 排序层：负责排序

## 数据准备
- Amazon electronics 数据集，包括 meta_Electronics.json 和 reviews_Electronics_5.json 用
  导入工具类 LoadDataController 导入数据到sqlite
- 倒排索引数据：InvertIndexController 导入测试用的倒排索引数据


## 完成剩下的代码
- 完成标记为TODO中的代码块