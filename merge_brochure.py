import PyPDF2
import os

def main(input_file):
    # input_file = "/home/xht/Documents/文字文稿1.pdf"  # 原稿
    # output_file_even = "./out_even.pdf"  # 見開きにしたPDFの保存
    # output_file_odd = "./out_odd.pdf"  # 見開きにしたPDFの保存

    base_path = os.path.splitext(input_file)[0]

    output_file_even = base_path + "_even.pdf"# 見開きにしたPDFの保存
    output_file_odd = base_path + "_odd.pdf"# 見開きにしたPDFの保存

    pdf_reader = PyPDF2.PdfFileReader(input_file, strict=False)

    addedPageNum = (pdf_reader.getNumPages() + 3) // 4 * 4
    oddPageList = []
    evenPageList = []
    for i in range(0, addedPageNum // 2, 2):
        oddPageList.extend((addedPageNum - 1 - i, i))

    for j in range(1, addedPageNum // 2, 2):
        evenPageList.extend((addedPageNum - 1 - j, j))
    evenPageList = evenPageList[::-1]
        
    for i in range(len(oddPageList)):
        if oddPageList[i] < pdf_reader.getNumPages():
            oddPageList[i] = pdf_reader.getPage(oddPageList[i])
        else:
            p1 = pdf_reader.getPage(0)
            oddPageList[i] = PyPDF2.PageObject.createBlankPage(width=p1.mediaBox.getUpperRight_x(),
                                                    height=p1.mediaBox.getUpperRight_y())


    for i in range(len(evenPageList)):
        if evenPageList[i] < pdf_reader.getNumPages():
            evenPageList[i] = pdf_reader.getPage(evenPageList[i])
        else:
            p1 = pdf_reader.getPage(0)
            evenPageList[i] = PyPDF2.PageObject.createBlankPage(width=p1.mediaBox.getUpperRight_x(),
                                                    height=p1.mediaBox.getUpperRight_y())

    def merge(pageList, output_file):
        pdf_writer = PyPDF2.PdfFileWriter()
        for i in range(0, len(pageList), 2):
        # for i in range(0, pdf_reader.getNumPages(), 2):
            # 最後に1ページ残る場合は見開きにしない
            p1 = pageList[i]
            p2 = pageList[i + 1]

            # 繋ぎ合わせるページ（p1：左側、p2：右側）

            # 見開きにしたページサイズ
            total_width = p1.mediaBox.getUpperRight_x() + p2.mediaBox.getUpperRight_x()
            total_height = max([p1.mediaBox.getUpperRight_y(), 
                                p1.mediaBox.getUpperRight_y()])

            # ページを貼り付ける空白ページ
            p = PyPDF2.PageObject.createBlankPage(width=total_width, 
                                                      height=total_height)
            # 左側のページを貼り付け
            p.mergePage(p1)
            # 右側のページを位置を指定して貼り付け
            p.mergeTranslatedPage(p2, p1.mediaBox.getUpperRight_x(), 0)

          # 見開きにしたページを出力用オブジェクトに追加
            pdf_writer.addPage(p)

        # ファイルに出力
        with open(output_file, mode="wb") as f:
            pdf_writer.write(f)

    merge(oddPageList, output_file_odd)
    merge(evenPageList, output_file_even)
    

if __name__ == "__main__":
    main()