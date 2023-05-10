import win32com.client
import os


PATH=os.getcwd()
print(PATH)

Application = win32com.client.Dispatch("PowerPoint.Application")
Presentation = Application.Presentations.Open(PATH+"/1.pptx")
Presentation.Slides[0].Export(PATH+"/1.jpg", "JPG")
Application.Quit()
Presentation =  None
Application = None