# [Imports]
import webbrowser

# [Get argv]
argus = (' '.join(argv)).strip()

# [Arguments]

_id = ""
_nid = ""
_open = False
_list = False

if "-o" in argus or "-open" in argus:
    argus = argus.replace("-open","")
    argus = argus.replace("-o","")
    argus = argus.strip()
    _open = True

if "-list" in argus:
    argus = argus.replace("-list","")
    argus = argus.strip()
    _list = True

if "-id" in argus:
    _id = argus.replace("-id","")
    _id = _id.strip()
elif "-nid" in args:
    _nid = argus.replace("-nid","")
    _nid = _nid.strip()
else:
    _id = argus


# [Code]

# list
if _list == True:
    id_linkbase = "https://simonkalmiclaesson.github.io/"
    id_link1 = "websa/shortener.html"
    url = id_linkbase + id_link1 + "?list"
    c = "id_shorteners = "
    rawlist = (((requests.get(url)).text).split(c)[1].split("\n")[0]).replace('"','')
    rawlist = rawlist.replace(" ","")
    webiItems = rawlist.split(",")
    print("Avaliable shortener ids: ")
    for item in webiItems:
        print(pt_format(cs_palette,f"\033[33m{item}\033[0m"))

# id
if _id != "" and _id != None:
    id_linkbase = "https://simonkalmiclaesson.github.io/"
    id_link1 = "websa/shortener.html"
    url = id_linkbase + id_link1 + f"?id={id}&giveurl"
    c = "urllocation_" + _id + " = "
    newlink = (((requests.get(url)).text).split(c)[1].split("\n")[0]).replace('"','')
    url = id_linkbase + newlink
    if url == id_linkbase:
        print(pt_format(cs_palette,f"\033[31mId '{id}' not found online. Try 'webi -list'\033[0m"))
    else:
        if _open == True:
            webbrowser.open(url)
        else:
            content = (requests.get(url)).text
            pattern = r'<h1>.*</h1>|<p>.*</p>|<i>.*</i>|<br>|<h3>.*</h3>|<b>.*</b>'
            matches = re.finditer(pattern,content)
            for m in matches:
                s = m.group()
                s = s.replace("<i>","\033[3m")
                s = s.replace("</i>","\033[23m")
                s = s.replace("<b>","\033[1m")
                s = s.replace("</b>","\033[22m")
                s = s.replace("<h3>","\033[1m")
                s = s.replace("</h3>","\033[22m")
                s = s.replace("<h1>","\033[1mArticle: ")
                s = s.replace("</h1>","\033[22m")
                s = s.replace("<p>","")
                s = s.replace("</p>","")
                s = s.replace("<br>","")
                print(s)