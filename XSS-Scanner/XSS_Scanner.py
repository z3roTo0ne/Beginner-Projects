import urllib
import urlparse
import os
import FileSetter
import re
import threading
from time import sleep
import time
import mechanize
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


# Function that returns id's of input fields of a given url
def id_crawler(start_url):

    ids = []
    try:
        x = urllib.urlopen(start_url)
        y = x.read()

        inputs = re.findall(r'<input[^>]* name="([^"]*)"', y)

        for input in inputs:
            ids.append(input)

    except (KeyError, ValueError, IndexError, IOError):
        pass

    ids.append(start_url)

    if len(ids) > 1 and start_url in ids:
        return ids
    else:
        pass


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


# This function stores every id that was found by id_crawler and writes it to ids.txt
def store_input_field_ids(i):
        try:
            with open(os.path.join(Path_To_Project_Dir, 'allLinks.txt'), 'rt') as f:
                line = f.read().split('\n')
                if len(line) >= i+1:
                    FileSetter.put_ids_in_file(id_crawler(line[i]), os.path.join(Path_To_Project_Dir, 'ids.txt'))
                    if len(line[i]) > 1:
                        print str(i + 1) + '. link scanned'
                    store_input_field_ids(i + 1)
                elif len(line) < i+1:
                    pass
        except:
            pass


# This function takes a url and a text input field id and checks the url for a simple xss vulnerability
def xss_check(n, i, u):

        vulnerable = False

        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Firefox')]

        br.open(url[u])
        br.select_form(nr=0)

        try:
            br.form[ids[u][n]] = payloads[i]

            # Press Submit
            sub = br.submit()

            response = br.open(sub.geturl())

            if payloads[i] in response.read():
                vulnerable = True
                FileSetter.append_to_file(os.path.join(Path_To_Project_Dir, 'XSS_Results.txt'), "Page is vulnerable here is the http response: \n" + br.open(sub.geturl()).read() + '\n')
                print "Page is vulnerable!"

            else:
                pass

            # Print url after submitting
            print "URL to page after injecting payload: " + sub.geturl() + '\n'
            FileSetter.append_to_file(os.path.join(Path_To_Project_Dir, 'XSS_Results.txt'), "URL to page after injecting payload: " + sub.geturl() + '\n')

            br.close()
        except ValueError:
            pass

        try:
            if i < len(payloads):
                xss_check(n, i + 1, u)
            elif i >= len(payloads):
                xss_check(n + 1, 0, u)
        except IndexError:
            if not vulnerable:
                FileSetter.append_to_file(os.path.join(Path_To_Project_Dir, 'XSS_Results.txt'), 'All text input fields of url: ' + url[u] + ' were checked, no vulnerabilities found' + '\n\n')
                print 'All text input fields of url: ' + url[u] + ' were checked, no vulnerabilities found'
            elif vulnerable:
                FileSetter.append_to_file(os.path.join(Path_To_Project_Dir, 'XSS_Results.txt'), 'Vulnerabilities in: ' + url[u] + ' were found!' + '\n\n')
                print 'Vulnerabilities in: ' + url[u] + ' were found!'


# Scanning starts here
print "\nScanning started. Scanning for " + str(time_to_scan) + " seconds" + "\n"

# These two functions create the main directory and create the crawled.txt and queued.txt file
FileSetter.create_main_directory(Path_To_Project_Dir)
FileSetter.create_result_files(Path_To_Project_Dir, start_link)

print "\nResults will be stored in " + os.path.join(Path_To_Project_Dir + '/allLinks.txt') + " and " + os.path.join(Path_To_Project_Dir + '/XSS_Results.txt') + "\n"

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

# Store every found text input id from id_crawler into one file called ids.txt
FileSetter.store_all_ids(Path_To_Project_Dir)

# Create a file named XSS_Results.txt which will be used to store the results of the xss scan
FileSetter.create_all_results_txt_file(Path_To_Project_Dir)

print 'Running text input id scan\n'
print 'Injecting payloads\n'

# Store the id of every input field that can be found on every found link
store_input_field_ids(0)

# Print out how many of our found links refer to pages with text input fields
print "\nFound" + FileSetter.count_ids(Path_To_Project_Dir) + "links that refer to pages with text input fields\n"

# Put every found id from ids.txt into one list called mainList
mainList = FileSetter.file_to_list(Path_To_Project_Dir)

# Create lists that store url's and id's that can be found on these specific pages
ml = []
url = []
ids = []

# Extracts every element between quotation marks from mainList and store it into ml
# This is needed because every element in mainList is a char and needs to be converted to a string
# If every element is a string it can be addressed properly
for i in range(0, len(mainList)):
    char_elements = mainList[i]
    string_elements = re.findall(r'\'(.*?)\'', char_elements)
    ml.append(string_elements)


# Extract every url from ml and add it to the url list
for i in range(0, len(ml)):
    url.append(ml[i][len(ml[i])-1])

# Extract every id from ml and add it to ids list
for i in range(0, len(ml)):
    ids.append(ml[i])
    del ids[i][len(ids[i]) - 1]


# All payloads that will be injected to test the xss vulnerability
payloads = ["<script>alert('Test')</script>", "<script>alert('Hello')</script>"]


# Check for a xss vulnerability on every crawled url with a text-input field
try:
    if len(url) > 1:
        for u in range(0, len(url)):
            try:
                xss_check(0, 0, u)
            except:
                print url[u] + " could not be scanned"

    else:
        try:
            xss_check(0, 0, 0)
        except:
            print url[0] + " could not be scanned"
except IndexError:
    print "No pages with text input fields to check xss on"
