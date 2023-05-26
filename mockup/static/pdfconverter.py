from pypdf import PdfReader, PdfWriter
import win32com.client as win32
import os, glob

basedir = os.getcwd()
pdf_folder = os.path.join(basedir, "시설물대장")
cropped_pdf_folder = os.path.join(basedir,"tmp")

for pdf in glob.glob(pdf_folder+"\\*.pdf"):
    reader = PdfReader(pdf)
    for num_page, page in enumerate(reader.pages, start=1):        
        if num_page == 1:
            # writer = PdfWriter()
            # writer.add_page(page)
            # with open(cropped_pdf_folder + "\\" + pdf.split('\\')[-1].replace(".pdf","") + "_기본현황.pdf", "wb") as fp:
            #     writer.write(fp)
            pass
        elif num_page == 2:
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

    try: 
        tables = doc.Tables
        table = tables(1)
        for i in range(1, 10):
            for j in range(1, 12):
                try:
                    result = table.Cell(Row=i, Column=j).Range.Text.replace('\r\x07','').replace('\r','')
                    print(str(i)+"/"+str(j)+" : "+result)
                except Exception as e:
                    print('pass')

        doc.Close(SaveChanges=win32.constants.wdDoNotSaveChanges)
        word.Quit()  
        print('저기?', cropped_pdf)
    except Exception as e:
        print('여기?', cropped_pdf)
        doc.Close(SaveChanges=win32.constants.wdDoNotSaveChanges)
        word.Quit()  

for file in os.listdir(cropped_pdf_folder):
    os.remove(os.path.join(cropped_pdf_folder, file))