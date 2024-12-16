@echo off
pdftk %* cat output "%* COMBINED.pdf"
goto :eof

REM ALTERNATIVES:
REM C:\portableapps\Calibre\Calibre\pdfmanipulate.exe merge ...
REM http://pieceofpy.com/index.php/2009/03/05/concatenating-pdf-with-python/ -> using http://pybrary.net/pyPdf/
REM http://pypi.python.org/pypi/pdfcat/1.0dev-r17

REM TODO: for image files: "i_view32.exe /panorama=(1,c:\pics\china1.png,c:\pics\china2.png,c:\pics\china3.png)"  http://www.makeuseof.com/tag/10-useful-commandline-irfanview-tools-working-images/