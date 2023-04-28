def replaceUrl(new_url):
    file = './README.md'
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if "https" in line:
                line = line.replace("https",new_url)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)

replaceUrl("--[hello world]--")
