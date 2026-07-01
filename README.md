[README.md](https://github.com/user-attachments/files/29555457/README.md)
# search_ver3.py 搜索工具

## 功能简介

`search_ver3.py` 会递归扫描 `data` 目录下的所有 Excel 文件（`.xlsx` 和 `.xls`），并查找用户输入的资产代码。匹配方式为“模糊匹配”，只要单元格中包含输入字符串即可被识别。

搜索完成后，程序会：

* 在控制台打印找到的文件名和 Sheet 名称
* 为每个匹配的 Sheet 生成预览数据
* 将最终匹配结果导出到一个新的 Excel 文件

---

## 主要行为

脚本会执行以下步骤：

1. 读取用户输入的资产代码
2. 遍历 `data` 目录中的所有 `.xlsx` 和 `.xls` 文件
3. 对每个 Sheet 读取内容并将所有单元格转为字符串
4. 使用 `str.contains(security_code, na=False)` 进行模糊匹配
5. 记录匹配结果并生成前 5 行的预览
6. 将匹配结果写入一个新的 Excel 文件，包含：
   * 每个文件的预览 Sheet
   * 对应的匹配 Sheet（带来源文件和来源 Sheet 信息）

---

## 项目结构

```text
SU26project
├── README.md
├── requirements.txt
├── search_ver3.py
└── data
    ├── Folder1
    ├── Folder2
    ├── Folder3
    └── Folder4
```

---

## 环境配置

### 创建虚拟环境

Mac / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 安装依赖

```bash
python -m pip install -r requirements.txt
```

---

## 运行方式

```bash
python search_ver3.py
```

程序启动后输入资产代码：

```text
请输入资产代码：600519
```

---

## 输出说明

当找到匹配时，控制台会输出：

* 找到的资产代码
* 对应 Excel 文件名
* 对应 Sheet 名称

如果匹配结果存在，程序还会生成一个导出文件，文件名格式为：

```text
搜索结果_<资产代码>_<时间戳>.xlsx
```

导出文件中每个匹配项包含：

* `文件名前10个字符_预览` Sheet：对应文件的前 5 行预览
* `文件名前10个字符_匹配` Sheet：匹配结果表格，顶部附带来源文件和来源 Sheet 信息

---

## 异常处理

脚本会自动跳过以下情况：

* 无法打开的 Excel 文件
* 无法读取的 Sheet

并继续扫描剩余文件。如果有文件无法扫描，程序会在结束时提示无法扫描的文件数量。

---

## 注意事项

* 匹配使用的是“包含”关系，因此输入 `600519` 会匹配 `600519贵州茅台`、`贵州茅台600519`、`6005191` 等。
* 当前脚本会将所有数据都按字符串读取并搜索，不区分数据类型。
* 若未找到匹配结果，且无文件读取错误，程序会打印 `未找到资产代码`。
```
