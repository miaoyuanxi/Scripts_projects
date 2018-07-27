import c4d, sys, re, os
from c4d import documents, gui

def main():
    doc = documents.GetActiveDocument()
    texs = doc.GetAllTextures()
    for i in (texs):
        if not texs: return
        tex = str(i)
        for i in tex.split():
            if ")" in i:
                keyword1 = i
                #print keyword1
                break
        word = keyword1.replace(")","")
        wordSplit = word.split("'")
        if wordSplit:
            wordHead1 = wordSplit[1]
            print wordHead1 + '\n'
        #print (b'wordHead1'.decode('utf-8'))
if __name__=='__main__':
    main()
