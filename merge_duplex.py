from PyPDF2 import PdfReader, PdfWriter
import os

def main(pdf_path):
    # 读取PDF文件
    reader = PdfReader(pdf_path)
    
    # 创建两个写入器
    odd_writer = PdfWriter()
    even_writer = PdfWriter()
    
    # 遍历所有页面
    for i, page in enumerate(reader.pages):
        # 页码从0开始，所以奇数页是偶数索引
        if i % 2 == 0:
            odd_writer.add_page(page)

    for i in range(len(reader.pages) // 2):
        # 页码从0开始，所以奇数页是偶数索引
        even_writer.add_page(reader.pages[len(reader.pages) // 2 * 2 - i * 2 - 1])
        
    
#     # 倒序偶数页
    # even_writer.pages.reverse()
    
    # 获取基础路径
    base_path = os.path.splitext(pdf_path)[0]
    
    # 写入奇数页文件
    with open(f"{base_path}_odd.pdf", "wb") as odd_file:
        odd_writer.write(odd_file)
    
    # 写入偶数页文件
    with open(f"{base_path}_even.pdf", "wb") as even_file:
        even_writer.write(even_file)

# 示例用法
if __name__ == '__main__':
    main("example_odd.pdf")
