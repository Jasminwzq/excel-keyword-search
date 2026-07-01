#================
#test 1: os.walk测试能不能找到excel
#================

# import os

# for root, dirs, files in os.walk("data"):

#     for file in files:

#         if file.endswith(".xlsx"):

#             file_path = os.path.join(root, file)

#             print(file_path)

#================
#test2: Read Excel测试能不能打开excel
#================
# import pandas as pd

# excel = pd.ExcelFile(
#     "data/Folder1/Fund_Holdings.xlsx"
# )

# print(excel.sheet_names)

#================
#test3: Read sheet数据测试能不能读取sheet内容
#================
# import pandas as pd

# df = pd.read_excel(
#     "data/Folder1/Fund_Holdings.xlsx",
#     sheet_name="持仓明细"
# )

# print(df)

import os
import pandas as pd

security_code = input(
    "请输入资产代码："
    #输入600519测试
)

found = False

for root, dirs, files in os.walk("data"):

    for file in files:

        if file.endswith(".xlsx"):

            file_path = os.path.join(root, file)

            try:
                excel = pd.ExcelFile(file_path)
            except Exception as e:
                print("无法打开:", file)
                continue

            for sheet_name in excel.sheet_names:

                try:
                     df = pd.read_excel(
                        file_path,
                        sheet_name=sheet_name,
                        dtype=str
                    )
                except Exception:
                    continue
                #=================
                #如果所有资产代码的表头都叫资产代码，记得改成series和用.str.strip()，去掉空格
                #=================
                # if "资产代码" in df.columns:

                #     code_series = (
                #         df["资产代码"]
                #         .astype(str)
                #         .str.strip()
                #     )

                #     if (code_series == security_code).any():

                #         found = True

                #         print()
                #         print("找到资产代码")
                #         print("文件:", file)
                #         print("Sheet:", sheet_name)


#=================
#精准查找
#=================
                
                # if (df.astype(str) == security_code).any().any():


                #     found = True

                #     print()
                #     print("找到资产代码", security_code)
                #     print("文件:", file)
                #     print("Sheet:", sheet_name)
#=================
#模糊查找，包含关系
#=================
                # if (
                #     df.astype(str)
                #     .apply(
                #         lambda col:
                #         col.str.contains(
                #             security_code,
                #             na=False
                #         )
                #     )
                #     .any()
                #     .any()
                # ):

                #     found = True

                #     print()
                #     print("找到资产代码")
                #     print("文件:", file)
                #     print("Sheet:", sheet_name)
#=================
#模糊查找version2
#=================
                match = (
                    df.astype(str)
                    .apply(
                        lambda col:
                        col.str.contains(
                            security_code,
                            na=False
                        )
                    )
                )

                if match.any().any():

                    found = True

                    print()
                    print("找到资产代码:", security_code)
                    print("文件:", file)
                    print("Sheet:", sheet_name)

                    for row_index in range(len(match)):

                        for column in match.columns:

                            if match.loc[row_index, column]:

                                print(
                                    "匹配单元格:",
                                    df.loc[row_index, column]
                                )

if not found:

    print("未找到资产代码")