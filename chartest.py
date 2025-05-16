import chardet

with open("D:\\Yazilim\\erp-mgp\\firebridtooracle.py", "rb") as f:
    result = chardet.detect(f.read(10000))

print(f"Detected encoding: {result['encoding']} (Confidence: {result['confidence']})")
