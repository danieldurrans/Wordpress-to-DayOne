import os
import markdownify

def parseData():
    input_file= open("personal_data.xml", "r")
    content= input_file.read()

    output_date_file= open("dateTime.txt", "w")
    file_count= 0
    tag_count= 0
    cat_count= 0

    while True:
        if "<item>" in content:
            file_count+= 1
            output_text_file= open("files/"+ str(file_count)+ ".txt", "w")
            print(file_count)

            #print(len(content))
            file_content= content[content.index("<item>"):content.index("</item>")]
            #print(file_content)

            title= file_content[file_content.index("<title>")+7 : file_content.index("</title>")]
            if "<![CDATA" in title:
                title= title[title.index("<![CDATA")+9 : title.index("]]")]
            print(title)

            file_content= file_content[file_content.index("</title>"):]
            text= file_content[file_content.index("<content:encoded>")+26 : file_content.index("</content:encoded>")-3]
            text= text.replace("#", '{hash}')
            mdtext = markdownify.markdownify(text, heading_style="ATX")
            #print(text)

            file_content= file_content[file_content.index("</content:encoded>"):]
            dateTime= file_content[file_content.index("<wp:post_date_gmt>")+18 : file_content.index("</wp:post_date_gmt>")]
            #print(dateTime+ "\n")

            file_content= file_content[file_content.index("</wp:post_date_gmt>"):]

            tags= []
            while '<category domain="post_tag"' in file_content:
                file_content= file_content[file_content.index('<category domain="post_tag"'):]
                tags.append(file_content[file_content.index("<![CDATA")+9 : file_content.index("</category>")-3])
                tag_count+= 1

                file_content= file_content[file_content.index("</category>"):]
            
            tags.append("wordpress2dayone")
            tag_count+= 1

            #print(tags)

            cats= []
            while '<category domain="category"' in file_content:
                file_content= file_content[file_content.index('<category domain="category"'):]
                cats.append(file_content[file_content.index("<![CDATA")+9 : file_content.index("</category>")-3])
                cat_count+= 1

                file_content= file_content[file_content.index("</category>"):]

            tags_string= " ".join(["#"+ i for i in tags])
            cats_string =""
            if len(cats) > 0:
                cats_string= "Categories: "+ ", ".join([i for i in cats])
            #print(tags_string)

            output_text_file_content= title+ "\n\n"+ mdtext+ "\n\n"+ cats_string+ "\n\n"+ tags_string
            #print(output_text_file_content)

            output_date_file.write(dateTime+ "\n")
            output_text_file.write(output_text_file_content)
            output_text_file.close()


            content= content[content.index("</item>")+5:]
            print("\n..................\n")
        else:
            output_date_file.close()
            print(file_count)
            print(tag_count)
            break

def makeDayOneEntries():
    this_dir= os.getcwd()
    #print(this_dir)
    entries= os.listdir(this_dir+ "/files")

    input_date_file= open("dateTime.txt", "r")

    for i in range(len(entries)):
        dateTime= input_date_file.readline()
        dateTime= dateTime[:-1]
        #print(dateTime)

        #print('dayone2 -d="'+ dateTime+ '" new<files/'+ str(i+1)+ '.txt')
        os.system('dayone2 -d="'+ dateTime+ '" new<files/'+ str(i+1)+ '.txt')


if __name__== "__main__":
    parseData()
    makeDayOneEntries()
