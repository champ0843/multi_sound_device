import textract
text = textract.process("C:\\Users\\PCCS\\Downloads\\LETTERS.DOCX")
text = text.decode("utf-8")
text = text.split("\n")
filt = filter(None,text)
text = list(filt)
