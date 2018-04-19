#!/usr/bin/env python3

""" Will download latest broforce maps (highest rated, last 3 months) from
steamcommunity.com, using http://steamworkshop.download """

# to build a windows .exe:
#    use a windows machine (pyinstaller cannot compile to WIN from MAC)
#    have python 2.7.x installed (pyinstaller not compatible with python3.x at time of writing)
#        make sure python2 is on system PATH (during python2 installation)
#    adjust requests module to be python2 compatible (see below)
#
# pip install pyinstaller
#    build with:             pyinstaller -F broforce-maps-downloader.py     (for single executable)
#    to clear build, delete: *.spec, dist/, build/

import urllib.request
from urllib.request import urlopen
#   for python2 compatible: remove all '.request', replace urllib with urllib2
import re
import time


steam_per_page = 30 # max=30


def main():
    print("This script will download latest broforce maps (highest rated, last 3 months) \
           \nfrom steamcommunity.com, using http://steamworkshop.download, in ./maps directory.")

    matches = set()
    print('Loading broforce pages from steamcommunity.com :')

    for i in iter(range(1, 6)): # goes from page 1 to 5.
        steam_url = 'https://steamcommunity.com/workshop/browse/?appid=274190&browseso' \
                    'rt=trend&section=readytouseitems&actualsort=trend&p={}&days=90' \
                    '&numperpage={}'.format(str(i), str(steam_per_page))

        # Compile maps list:    --------------------------------------------------
        response = urllib.request.urlopen(steam_url)
        html = response.read().decode('utf-8')
        # print(html)
        # urllib.request.urlretrieve(steam_url, 'rawpage')  # save as 'rawpage'
        print('\n------------------ Page {} loaded.\n'.format(str(i)))

        matchObj = re.findall(r'https://steamcommunity.*searchtext=', html, re.M|re.I)
        ###    http://steamcommunity.com/sharedfiles/filedetails/?id=1128183775&searchtext=

        if matchObj:
            morematches = set(matchObj)  # remove duplicates
            # print(morematches)
            print('{} matches found.'.format(len(morematches)))
            matches = matches | morematches  # set union
        else:
            print('No match!')

        time.sleep(1)

    # print('\n\nTotal Matches Set >>>>>>> {} \n\n'.format(matches))

    # Download maps:    ------------------------------------------------------
    print('\n------------------ \n\nDownloading maps from steamworkshop.download :')
    for match in matches:
        id = match.split('https://steamcommunity.com/sharedfiles/filedetails/?id=')[1][:-12]
        ###    http://steamcommunity.com/sharedfiles/filedetails/?id=942186138&searchtext=

        workshop_url = 'http://steamworkshop.download/download/view/{}'.format(id)
        # print('>>> workshop_url: {}'.format(workshop_url))
        s = urlopen(workshop_url) # response
        html = s.read().decode('utf-8')
        # print(html)

        print('\n------------------\n')

        # matchObj = re.findall(r"<a href='http://cloud-.* title.*'>", html, re.M|re.I)
        ###   <a href='http://cloud-3.steamusercontent.com/ugc/831325411032538972/FA6AE993DE4FFE13CDB214C46E3303A89C6F040C/' title='Terror in the Jungle'>
        ###   /\_ no longer works, as of 19-Apr-2018, valid example is below:
        matchObj = re.findall(r"https://steamusercontent.* title.*'>", html, re.M|re.I)
        ###   <a href='https://steamusercontent-a.akamaihd.net/ugc/924801404255651641/0B9D88F9C2B0484E69AF18B3CEC25FB001A55C87/' title=
        # print('>>> matchObj: {}'.format(matchObj))  # SHOULD be ONE match ... :)
        if matchObj:
            downloadurl = matchObj[0].split(' title')
            title = downloadurl[1][2:-2]
            downloadurl = downloadurl[0][:-1] # ^ DO NOT CHANGE ORDER! ^
            print(title)
            print(downloadurl)
            # Download file:
            title = "".join(x for x in title if x not in "\/:*?<>|")  # clean up for filename, some peope use weird map names!
            # or use   https://github.com/un33k/python-slugify
            for attempt in range(3):
                try:
                    urllib.request.urlretrieve(downloadurl, 'maps/'+title+'.bfg')
                    print('> Done!')
                    break
                except Exception as e:
                    print(e)
                    continue
            else:
                print('Skipping this one ...')  # skip this particular file after 3 failed attempts
        else:
            print('No match!')

        time.sleep(1)


if __name__ == '__main__':
    main()
