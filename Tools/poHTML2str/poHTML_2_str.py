import os
import subprocess
from time import sleep
from  bs4 import BeautifulSoup
'''
def getFilePaths():
    # Returns a list of absolute filepaths for all files within the "HTML" folder
    filepaths = []
    for (dirpath, dirnames, filenames) in os.walk(os.path.join(os.getcwd(), "HTML")):
        for filename in filenames:
            if filename.endswith(".html"):
                filepaths.append(filename)
        break
    return filepaths
'''
def makeSoup(file):
    # Makes an HTML 'soup' for a given .html file in the HTML folder
    with open(os.path.join("HTML", file), "r", encoding="utf8") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, features = "html.parser")
    return soup

def alignItem(header, translation):
    return header + "\n\t" + '"' + translation + '"' + "\nEnd\n"

# Create list of filenames from the HTML folder
HTML_Directory = os.getcwd() + "\\HTML"
filepaths = [file for file in os.listdir(HTML_Directory) if file.endswith(".html")]

# Make an HTML 'soup' for each file in 'filepaths'
soups = [makeSoup(file) for file in filepaths]

#if os.path.exists("mod.str"):
#    os.rename("mod.str", "mod.str.old")

for soup in soups:
    print("Parsing HTML soup for '{}'...".format(filepaths[soups.index(soup)]))
    # Grabs raw HTML for item headers, then the actual text for the headers
    html_src = soup.body.find_all("td", attrs={"class":"src"})
    headers = [header.find("span", attrs={"class":"msgctxt"}).text for header in html_src]

    # Grabs translated definition text from HTML; this data isn't stored the same way as the headers
    translations = [tra.text[1:] for tra in soup.body.find_all("td", attrs={"class":"tra"})]

    print("\tTranslation data retrieved. Correcting newlines in definitions...")
    # The data above are in parallel to each other
    # For example: the data in headers[0] corresponds to translations[0]
    
    '''
    headers_to_rename = {"NAME:ArmorBarracksArmor":"UPGRADENAME:ArmorBarracksArmor",
                         "NAME:ArmorMCVHealth":"UPGRADENAME:ArmorMCVHealth",
                         "NAME:ArmorNavalMissile":"UPGRADENAME:ArmorNavalMissile",
                         "NAME:ArmorNavalProduction":"UPGRADENAME:ArmorNavalProduction",
                         "NAME:ArmorTechAA":"UPGRADENAME:ArmorTechAA",
                         "NAME:ArmorTechRush":"UPGRADENAME:ArmorTechRush",
                         "NAME:ArmorTechScout":"UPGRADENAME:ArmorTechScout",
                         "NAME:ArmorWarFire":"UPGRADENAME:ArmorWarFire",
                         "NAME:ArmorWarReform":"UPGRADENAME:ArmorWarReform",
                         "NAME:ArmorWarTank":"UPGRADENAME:ArmorWarTank"}

    headers_to_add = {"MAP:[RAT]Snow_Town":"[AR] Snow Town-ST",
                      "MAP:[RAT]Tank_Crash":"[AR] Tank Graveyard-TC",
                      "MAP:MAP_MP_2_FEASEL11_EP1":"[AR] Hot Spring",
                      "MAP:MAP_MP_4_FEASEL1_EP1":"[AR] Return to Lake Blez"}
    
    
    for i in range(len(headers)):
        if headers[i] in headers_to_rename.keys():
            headers[i] = headers_to_rename[headers[i]]

    for key in headers_to_add.keys():
        headers.append(key)
        translations.append(headers_to_add[key])
    '''
    # Loop through each translated definition
    for i in range(len(translations)):
        #if '"' in translations[i]:
        #    listTrans = list(translations[i])
        #    for j in range(len(listTrans)):
        #        if listTrans[j] == '"':
        #            listTrans[j] = "\\" + '"'
        #    newTrans = "".join(listTrans)
        #    translations[i] = newTrans

        # Scan the current translation for the "\n" characters and replace them with actual newlines/breaks
        if "\n" in translations[i]:
            listTrans = list(translations[i])
            for j in range(len(listTrans)):
                if listTrans[j] == "\n":
                    listTrans[j] = r"\n"
            newTrans = "".join(listTrans)
            translations[i] = newTrans

    # Create a temporary .str file and append data to it on each iteration
    print("\tAppending formatted translation data to 'tempSTR.str'...")
    with open(os.getcwd() + "\\Tools\\temp\\tempSTR.str", "a+") as f:
        for i in range(len(translations)):
            f.write(alignItem(headers[i], translations[i]))

    print("\tTranslations appended to 'tempSTR.str'.\n\n")

# Call STR_Fixer to finalize the new mod.str file
print("Launching 'STR_Fixer.exe' to finalize 'mod.str'.\nPlease keep your hands off of the keyboard to avoid breaking the control automation...")
sleep(10)
subprocess.call([os.getcwd() + "\\Tools\\STR_Fixer.exe"])

print("Conversion complete. You may now resume control of the keyboard.")
