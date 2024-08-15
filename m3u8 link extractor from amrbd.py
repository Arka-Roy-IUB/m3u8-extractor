import requests
from bs4 import BeautifulSoup
import re
import os

def scrape(url):
    # make a GET request to the URL
    response = requests.get(url)

    # create a Beautiful Soup object with the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # find all the <a> tags on the page
    links = soup.find_all("a")

    # loop through all the links and extract the onclick attributes
    onclicks = []
    for link in links:
        onclick = link.get("onclick")
        if onclick:
            onclicks.append(onclick)
    return onclicks


def curate_one(onclicks):
    cure_streams = []
    for onclick in onclicks:
        output_str = re.sub("tv.location.href='|'", lambda x: "" if x.group() == "'" else "", onclick)
        cure_streams.append(output_str)
    return cure_streams

def curl(url):
    # url = 'http://bdiptv.net/play.php?stream=STAR-SPORTS-2'
    headers = {'Referer': 'http://stream.amrbd.com/'}
    response = requests.get(url, headers=headers)
    return response

def tv_name(onclicks):
    names = []
    for onclick in onclicks:
        name = re.search("play\.php\?stream=([\w-]+)'", onclick)
        if name:
            names.append(name.group(1))
    return names

def custom_key(item):
    if item == 'Somoy-TV':
        return 0
    elif item == 'DBC-NEWS':
        return 1
    elif item == 'Ekattor-tv':
        return 2
    elif item == 'jamuna-tv':
        return 3
    elif item == 'Independent-Tv':
        return 4
    elif item == 'News24bd':
        return 5
    elif item == 'Channel24':
        return 6
    elif item == 'ZeeBanglaHD':
        return 7
    elif item == 'Star-Jalsha':
        return 8
    elif item == 'colorsbangla':
        return 9
    else:
        return 10



def extract_embed_html_link(response):
    regex = r'src="(.*?)&remote'
    matches = re.findall(regex, response.text)
    return matches

#for match in matches:
#print(matches[0])
def curate_two(matches):
    input_string = str(matches[0])
    output_str = re.sub("embed.html|autoplay=false&", lambda x: "" if x.group() == "autoplay=false&" else "index.m3u8", input_string)
    return output_str

def final_list(url):
    streams= curate_one(scrape(url))
    final_link = []
    for stream in streams:
        cure_stream = curl(stream)
        find_embed_html = extract_embed_html_link(cure_stream)
        replace_embed_html = curate_two(find_embed_html)
        final_link.append(replace_embed_html)
    return final_link

# write the URLs to a file
def write_to_file(url):
    urls = final_list(url)
    file_name = 'amrbd_urls.m3u'
    file_path = 'C:/Users/arkar/AppData/Local/Temp/' + file_name
    with open(file_path, 'w') as f:
        f.write('#EXTM3U' + '\n' )
        for i in range(len(urls)):
            f.write('#EXTINF:-1,' + str(names[i]) + '\n')
            f.write(urls[i] + '\n')


def sorting_file(input_file, sorted_names):
    # Read the lines from the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Split the lines into groups of two, where the first line starts with #EXTINF:-1
    groups = [lines[i:i+2] for i in range(0, len(lines), 2)]

    # Sort the groups based on the order of sorted_list
    sorted_groups = sorted(groups, key=lambda g: sorted_list.index(g[0].split(',')[1]))

    # Write the sorted lines to a new file
    output_file = 'sorted_file_amrbd.m3u'
    with open(output_file, 'w') as f:
        f.writelines([line for group in sorted_groups for line in group])


def sorted_file(input_file, sorted_names):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Group lines into two-line chunks
    line_groups = [(lines[i], lines[i+1]) for i in range(1, len(lines), 2) if "http://" in lines[i+1]]

    # Sort the line groups based on the position of the channel name in the sorted_list
    sorted_line_groups = sorted(line_groups, key=lambda x: sorted_names.index(x[0].split(",")[-1].strip()))

    # Flatten the sorted line groups and add back in the header lines
    sorted_lines = [lines[0]] + [l for group in sorted_line_groups for l in group]

    with open('C:/Users/arkar/Desktop/sorted_file_amrbd.m3u', 'w') as f:
        f.writelines(sorted_lines)

url = "http://amrbd.com/"
scraped = scrape(url)
names = tv_name(scraped)
sorted_names = sorted(names, key=custom_key)
input_file = 'C:/Users/arkar/AppData/Local/Temp/amrbd_urls.m3u'

write_to_file(url)
sorted_file(input_file, sorted_names)
