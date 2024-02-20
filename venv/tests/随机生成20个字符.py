# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
import random
import codecs

res = ''
# GB2312编码范围是从0xA1A1到0xFEFE
gb2312_range = range(0xA1A1, 0xFEFE + 1)

# 随机选择20个编码
random_codes = random.sample(gb2312_range, 20)

# 将编码转换为字节
random_bytes = [bytes([code >> 8, code & 0xFF]) for code in random_codes]
print(random_bytes)

for gb2312_encoded_bytes in random_bytes:
    print(gb2312_encoded_bytes)
    gb2312_decoded_str = codecs.decode(gb2312_encoded_bytes, 'gb2312')
    res.join(gb2312_decoded_str)
    # 打印解码后的字符串

print(res)
