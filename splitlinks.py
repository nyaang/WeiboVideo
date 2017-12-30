import json
def splitlinks(splitnum):
    links=json.load(open("values/links.json", 'r', encoding='utf-8'))["links"]
    links_len = len(links)
    split_len = links_len // splitnum
    i = 1
    while (i < splitnum):
        linki = links[split_len * (i - 1):split_len * i]
        linkfile = open('values/links/'+'links'+str(i)+'.json', 'w', encoding='utf-8')
        json.dump(linki, linkfile, indent=4, sort_keys=False, ensure_ascii=False)
        linkfile.close()
        i=i+1
    linkend = links[split_len * (i-1):links_len]
    linkfile = open('values/links/' + 'links' + str(i) + '.json', 'w', encoding='utf-8')
    json.dump(linkend, linkfile, indent=4, sort_keys=False, ensure_ascii=False)