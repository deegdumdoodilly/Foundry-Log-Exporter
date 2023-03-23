import sys
import requests
import json

def get_messagebox(image_source, character_name, timestamp, message):
    return '''<div class ="chatlog__message-group" >
                <div class="chatlog__author-avatar-container">
                    <img class="chatlog__author-avatar" src="{0}" alt="Avatar" loading="lazy">
                </div>
                
                <div class="chatlog__messages">
                    <span class="chatlog__author-name" title="{1}" data-user-id="319222181022138370" style=""> 
                        {1} 
                    </span>
        
                    <span class="chatlog__timestamp">
                        {2}
                    </span>
        
                    <div class="chatlog__message " data-message-id="952726323934154802" id=
                        "message-952726323934154802" title="Message sent: {2}">
                        <div class="chatlog__content">
                            <div class ="markdown">
                                <span class="preserve-whitespace">{3}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>\n'''.format(image_source, character_name, timestamp, message)


def getPNG(address):
    html = requests.get(address).text
    index = html.find("Size of this PNG preview of this SVG file: ")
    if index == -1:
        print("Error, could not find image to use for default profile pic: " + address)
    html = html[index+52:]
    html = html[:html.find("\"")]
    return html


if __name__ == '__main__':
    try:
        mappingFile = open('mappings.json')
        imageMapping = json.load(mappingFile)
    except IOError:
        print("Warning, could not locate mappings.json file. Will continue with default images")

    colorSequence = ["deep-orange", "blue", "light-green", "purple", "teal", "pink", "yellow","indigo","brown","amber","red","cyan","orange","deep-purple","light-blue","green","lime","grey","blue-grey"]
    colorIndex = 0
    if len(sys.argv) < 2:
        print("ERROR: must supply a text document as a parameter")
        exit(1)
    with open("preamble.txt", "r") as preamble:
        try:
            with open(sys.argv[1], "r", encoding='UTF-8') as infile, open(sys.argv[1][:-4] + ".html", "w", encoding='UTF-8') as output:
                for line in preamble.readlines():
                    output.write(line)
                output.write("\t\t<div class=\"preamble__entry\">Group /" + sys.argv[1][:-4] + "</div>\n\t</div>\n</div>\n<div class=\"chatlog\">")                      
                # Can be 'timestamp', 'content' or 'separator', REPRESENTS PREVIOUS LINE
                last_line = 'separator'
                timestamp = ''
                message = ''
                author = ''
                unknownNames = []
                linesRead = 0
                for line in infile.readlines():
                    linesRead += 1
                    try:
                        if line.strip() == "":
                            continue
                        if last_line == 'separator':  # Next should be timestamp
                            closing_bracket_index = line.index(']')
                            timestamp = line[1:closing_bracket_index]
                            author = line[closing_bracket_index+2:-1]
                            last_line = 'timestamp'
                            content = ''
                        elif last_line == 'timestamp':
                            if line == '---------------------------\n':
                                last_line = 'separator'
                                if author in imageMapping.keys():
                                    img = imageMapping[author]
                                else:
                                    wikiString = "https://commons.wikimedia.org/wiki/File:Eo_circle_" + colorSequence[colorIndex] + "_white_letter-" + author[0:1].lower() + ".svg"
                                    colorIndex = (colorIndex + 1) % len(colorSequence)
                                    img = getPNG(wikiString)
                                    imageMapping[author] = img
                                    if unknownNames.count(author) == 0:
                                        unknownNames.append(author)
                                output.write(get_messagebox(img, author, timestamp, content))
                            else:
                                content += line
                    except Exception as e:
                        print("Error processing file, please make sure that the input file was a Foundry text log. Error encountered at line number " + str(linesRead))
                        exit(1)

                if author in imageMapping.keys():
                    img = imageMapping[author]
                else:
                    img = 'https://upload.wikimedia.org/wikipedia/commons/thumb/' \
                        '1/11/Blue_question_mark_icon.svg/1200px-Blue_question_mark_icon.svg.png'
                output.write(get_messagebox(img, author, timestamp, content))
                output.write('''</div>

                                

                                </body>

                                </html>''')
                print("Names with no images specified:")
                for name in unknownNames:
                    print(name)
        except IOError:
            print("Error opening file: " + sys.argv[1])
            exit(1)
