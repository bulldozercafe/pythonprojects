import sys

sys.setrecursionlimit(10000000)

def consume_memory(depth):
    large_data = []
    
    try:
        while True:
            # 대규모 문자열을 생성하여 메모리를 소비
            large_data.append("x" * (10**7))  # 10,000,000 문자를 가진 문자열
            depth += 1
            print(f"Depth: {depth}, Current memory usage: {len(large_data)} items")
            
    except (KeyboardInterrupt, RecursionError, MemoryError):
        depth+=1
        return consume_memory(depth)
depth = 1
consume_memory(depth)
