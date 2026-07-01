

import os
import pandas as pd
from datetime import datetime

security_code = input(
    "请输入资产代码："
    #输入600519测试
)

found = False
error_count = 0
results = {}
preview_results = {}

for root, dirs, files in os.walk("data"):

    for file in files:

        if file.endswith((".xlsx",".xls")):

            file_path = os.path.join(root, file)

            try:
                excel = pd.ExcelFile(file_path)
            except Exception as e:
                error_count += 1
                print("无法打开:", file)
                print("错误信息：", e)
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

                    raw_df = pd.read_excel(
                        file_path,
                        sheet_name = sheet_name,
                        header = None,
                        dtype = str
                    )

                    preview_df = raw_df.head(5)

                    preview_results[
                        (file, sheet_name)
                    ] = preview_df

                    matched_rows = df[
                        match.any(axis = 1)
                    ]

                    results[
                        (file, sheet_name)
                    ] = matched_rows

                    
                    print()
                    print("找到资产代码:", security_code)
                    print("文件:", file)
                    print("Sheet:", sheet_name)

if results:

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = f"搜索结果_{security_code}_{timestamp}.xlsx"

    with pd.ExcelWriter(
        output_file
        #engine="openpyxl"
        ) as writer:
        for(
            file,
            sheet_name
        ), result_df in results.items():
            
            preview_df = preview_results[
                (file, sheet_name)
            ]
            
            preview_sheet = (
                file[:10]
                + "_预览"
            )

            preview_df.to_excel(
                writer,
                sheet_name = preview_sheet,
                # startrow = 3,
                index = False,
                header = False
            )

            match_sheet = (
                file[:10]
                +"_匹配"
            )

           

            info_df = pd.DataFrame(
                {
                    "信息": [
                        f"来源文件:{file}",
                        f"来源sheet:{sheet_name}",
                        ""
                    ]
                }
            )

            info_df.to_excel(
                writer,
                sheet_name=match_sheet,
                index = False,
                header = False
            )

            result_df.to_excel(
                writer,
                sheet_name=match_sheet,
                startrow = 3,
                index = False
            )
        
        print()
        print(f"结果已导出到：{output_file}")



if not found:
    if error_count == 0:
        print("未找到资产代码")
    else:
        print(
            f"未找到资产代码有{error_count}个文件未能扫描"
            )
    