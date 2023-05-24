from pypdf import PdfReader, PdfWriter
import win32com.client as win32
import os, glob

basedir = os.getcwd()
pdf_folder = os.path.join(basedir, "시설물대장")
cropped_pdf_folder = os.path.join(basedir,"tmp")

for pdf in glob.glob(pdf_folder+"\\*.pdf"):
    reader = PdfReader(pdf)
    for num_page, page in enumerate(reader.pages, start=1):        
        if num_page == 2:
            writer = PdfWriter()
            writer.add_page(page)
            with open(cropped_pdf_folder + "\\" + pdf.split('\\')[-1].replace(".pdf","") + "_기본현황.pdf", "wb") as fp:
                writer.write(fp)
        elif num_page == 3:
            writer = PdfWriter()
            writer.add_page(page)
            with open(cropped_pdf_folder + "\\" + pdf.split('\\')[-1].replace(".pdf","") + "_상세제원.pdf", "wb") as fp:
                writer.write(fp)
        # elif num_page > 3:
        #     if num_page == 4:
        #         writer = PdfWriter()            
        #     writer.add_page(page)
        #     if num_page == 7:
        #         with open(cropped_pdf_folder + "\\" + pdf.split('\\')[-1].replace(".pdf","") + "_진단이력.pdf", "wb") as fp:
        #             writer.write(fp)
        #             break
    
word = win32.gencache.EnsureDispatch('Word.Application')

for cropped_pdf in glob.glob(cropped_pdf_folder+"\\*.pdf"):
    word.Documents.Open(cropped_pdf)    
    doc=word.ActiveDocument

    if cropped_pdf.endswith("_기본현황.pdf"):
        tables = doc.Tables
        table = tables(1)

        시설물번호 = table.Cell(Row=3, Column=1).Range.Text.replace('\r\x07','').replace('\r','')
        시설물명 = table.Cell(Row=3, Column=3).Range.Text.replace('\r\x07','').replace('\r','')
        시설물종류 = table.Cell(Row=3, Column=6).Range.Text.replace('\r\x07','').replace('\r','')
        시설물종별 = table.Cell(Row=3, Column=7).Range.Text.replace('\r\x07','').replace('\r','')
        시설물구분 = table.Cell(Row=3, Column=8).Range.Text.replace('\r\x07','').replace('\r','')

        first_addr = table.Cell(Row=5, Column=1).Range.Text.replace('\r\x07','').replace('\r','')
        second_addr = table.Cell(Row=5, Column=2).Range.Text.replace('\r\x07','').replace('\r','')
        third_addr = table.Cell(Row=5, Column=3).Range.Text.replace('\r\x07','').replace('\r','')
        fourth_addr = table.Cell(Row=5, Column=4).Range.Text.replace('\r\x07','').replace('\r','')
        시설물주소 = " ".join([first_addr, second_addr, third_addr, fourth_addr])

        관리주체 = table.Cell(Row=5, Column=5).Range.Text.replace('\r\x07','').replace('\r','')
        준공일 = table.Cell(Row=9, Column=2).Range.Text.replace('\r\x07','').replace('\r','')
        설계자 = table.Cell(Row=11, Column=2).Range.Text.replace('\r\x07','').replace('\r','')
        공사기간 = table.Cell(Row=11, Column=3).Range.Text.replace('\r\x07','').replace('\r','')
        시공자 = table.Cell(Row=11, Column=4).Range.Text.replace('\r\x07','').replace('\r','')
        감리자 = table.Cell(Row=15, Column=3).Range.Text.replace('\r\x07','').replace('\r','')

    elif cropped_pdf.endswith("_상세제원.pdf"):    
        tables = doc.Tables
        table = tables(1)
        
        주용도 = table.Cell(Row=2, Column=2).Range.Text.replace('\r\x07','').replace('\r','')

        basement = table.Cell(Row=5, Column=3).Range.Text.replace('\r\x07','').replace('\r','').replace(' ','')
        basement = '' if basement == '0층' else basement
        ground = table.Cell(Row=5, Column=1).Range.Text.replace('\r\x07','').replace('\r','').replace(' ','')
        층수 = ('지하' + basement + ', ' if basement else '') + '지상' + ground

        최고높이 = table.Cell(Row=5, Column=4).Range.Text.replace('\r\x07','').replace('\r','')
        건축면적 = table.Cell(Row=9, Column=3).Range.Text.replace('\r\x07','').replace('\r','')
        건축연면적 = table.Cell(Row=9, Column=4).Range.Text.replace('\r\x07','').replace('\r','')
        구조형식 = table.Cell(Row=7, Column=1).Range.Text.replace('\r\x07','').replace('\r','')

    # elif cropped_pdf.endswith("_진단이력.pdf"):        
    #     tables = doc.Tables
    #     for num_tbl, table in enumerate(tables, start=1):
    #         if num_tbl == 1:
    #             continue
    
    doc.Close(SaveChanges=win32.constants.wdDoNotSaveChanges)

word.Quit()  

for file in os.listdir(cropped_pdf_folder):
    os.remove(os.path.join(cropped_pdf_folder, file))