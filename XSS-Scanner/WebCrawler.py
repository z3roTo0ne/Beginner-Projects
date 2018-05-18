import urllib
import urlparse
import os
import FileSetter
import re
import threading
from time import sleep
import time
import sys

# Set target
start_link = raw_input("Enter Target Address (Please use a full domain name address): ")

# Set path to folder where you want to save your project
Path_To_Project_Dir = raw_input("Enter path to folder where you want to save your project: ")

# Set to True to scan sites outside the main site (Could end in an infinite loop)
YorN = raw_input("Also crawl and scan external addresses? (y/N): ")

if YorN == 'y' or YorN == 'Y':
    check_external_urls = True
elif YorN == 'n' or YorN == 'N':
    check_external_urls = False
else:
    print "Wrong input please try again"
    sys.exit(0)

# Set amount of simultaneously working threads
threads = int(raw_input("Enter amount of threads to create: "))

# Set for how long to perform the scan
time_to_scan = int(raw_input("How long you want to scan (Enter time in seconds): "))

# Store the time before the scan starts
old_time = time.time()

# Set how many times a function can call itself
sys.setrecursionlimit(1000)


# Function that scans for other links
def link_crawler(url):

    links = []
    try:
        x = urllib.urlopen(url)
        y = x.read()

        link = re.findall(r'<a[^>]* href="([^"]*)"', y)
        jslink = re.findall(r'<script[^>]* src="([^"]*)"', y)
        js2link = re.findall(r'window.location.replace\s*\("([^"]*)"\)', y)
        js3link = re.findall(r'window.location.href\s*=\s*"([^"]*)"', y)

        FileSetter.transfer_links(url, Path_To_Project_Dir)

        for link in link:
            link = urlparse.urljoin(url, link)
            if FileSetter.check_if_written(link, Path_To_Project_Dir):
                print ("Link already Crawled, skipping...")
            elif FileSetter.check_if_base_url(link, url) and not check_external_urls:
                print ("Link not part of base URL, skipping...")
            else:
                print ('Found Link: ' + link)
                links.append(link)
        for jslink in jslink:
            jslink = urlparse.urljoin(url, jslink)
            if FileSetter.check_if_written(jslink, Path_To_Project_Dir):
                print ("Link already Crawled, skipping...")
            elif FileSetter.check_if_base_url(jslink, url) and not check_external_urls:
                print ("Link not part of base URL, skipping...")
            else:
                print ('Found Link: ' + jslink)
                links.append(jslink)
        for js2link in js2link:
            js2link = urlparse.urljoin(url, js2link)
            if FileSetter.check_if_written(js2link, Path_To_Project_Dir):
                print ("Link already Crawled, skipping...")
            elif FileSetter.check_if_base_url(js2link, url) and not check_external_urls:
                print ("Link not part of base URL, skipping...")
            else:
                print ('Found Link: ' + js2link)
                links.append(js2link)
        for js3link in js3link:
            js3link = urlparse.urljoin(url, js3link)
            if FileSetter.check_if_written(js3link, Path_To_Project_Dir):
                print ("Link already Crawled, skipping...")
            elif FileSetter.check_if_base_url(js3link, url) and not check_external_urls:
                print ("Link not part of base URL, skipping...")
            else:
                print ('Found Link: ' + js3link)
                links.append(js3link)
            links.remove(start_link)

    except (KeyError, ValueError, IndexError, IOError):
        pass

    links = FileSetter.filter_duplicates(links)

    return links


# This functions runs in several threads, runs link_crawler and writes found links to the result text files
def store_links(i):
    if time.time() - old_time >= time_to_scan:
        print('Crawling Done. Closing Thread ' + str(i+1) + '\n')
    else:
        try:
            with open(os.path.join(Path_To_Project_Dir, 'queued.txt'), 'rt') as f:
                line = f.read().split('\n')
                if len(line) >= i+1:
                    FileSetter.remove_empty_lines(os.path.join(Path_To_Project_Dir, 'queued.txt'))
                    FileSetter.put_links_in_file(link_crawler(line[i]), os.path.join(Path_To_Project_Dir, 'queued.txt'))
                    FileSetter.remove_empty_lines(os.path.join(Path_To_Project_Dir, 'queued.txt'))
                    store_links(i)
                elif len(line) < i+1:
                    sleep(10)
                    store_links(i)
        except:
            pass


# Scanning starts here
print "\nScanning started. Scanning for " + str(time_to_scan) + " seconds" + "\n"


# These two functions create the main directory and create the crawled.txt and queued.txt file
FileSetter.create_main_directory(Path_To_Project_Dir)
FileSetter.create_result_files(Path_To_Project_Dir, start_link)

print "\nResults will be stored in " + os.path.join(Path_To_Project_Dir + '/allLinks.txt') + "\n"

# This for-loop creates several threads and runs the store-link function
t = {}
for n in range(0, threads):
        t["t{0}".format(n)] = threading.Thread(target=store_links, args=(n,))
        t["t{0}".format(n)].start()

# Wait another 10 seconds until every previously created thread except the main thread is closed
sleep(time_to_scan + 10)
time_to_scan = 0

# Store every found link from queued.txt and crawled.txt into one file called allLinks.txt
FileSetter.store_all_links(Path_To_Project_Dir)

# Print out how many links were found in total
print "\nFound" + FileSetter.count_links(Path_To_Project_Dir) + "links\n"

