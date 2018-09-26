#!/bin/env python3
import cgi, os
import cgitb; cgitb.enable()
from WebpageUtils import *
import hashlib

# ./HTTPServer.py --port 80 --dir ../qdropbox/ --mode cgi --pwd "user:password"

def uploadpage():
    P,b = makePageStructure("AAP 2018 Presentations")
    addTag(b,"h1",contents=["AAP 2018 Presentations Dropbox"])

    F = ET.Element("form", {"action":"/cgi-bin/qdropbox.py", "method":"POST", "enctype":"multipart/form-data"})
    addTag(F,"label",{"for":"file"},"File (.pdf only): ")
    addTag(F,"input", {"type":"file", "name":"file", "id":"file", "accept":"application/pdf"})
    addTag(F,"input",{"type":"submit","name":"submit","value":"Upload"})

    b.append(F)

    if os.path.exists("uploads/"):
        fs = os.listdir("uploads/")
        fs.sort()
        trows = [makeLink("/uploads/"+f, f) for f in fs]
        b.append(makeList(trows))

    print(docHeaderString())
    print(prettystring(P))

if __name__=="__main__":
    form = cgi.FieldStorage()
    if 'file' in form:

        f = form['file']
        if f.filename and f.filename[-4:] == ".pdf":

            # strip path to just get filename
            fn = os.path.basename(f.filename)

            # check if file with same name and hash already uploaded; rename if unique
            fn1 = fn
            v = 2
            while os.path.exists("uploads/"+fn1):
                h1 = hashlib.sha256(f.file.read()).hexdigest()
                h2 = hashlib.sha256(open("uploads/"+fn1, "rb").read()).hexdigest()
                if h1 == h2:
                    fn1 = None
                    break
                fn1 = fn[:-4]+"_v%i"%v+".pdf"
                v += 1

            # save uploaded file
            if fn1:
                os.system("mkdir -p uploads/")
                open('uploads/' + fn1, 'wb').write(f.file.read())

    uploadpage()
