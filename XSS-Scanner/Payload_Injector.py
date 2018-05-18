import mechanize
import FileSetter
import re
import urllib
import os


# Set target
start_link = raw_input("Enter Target Address (Please use a full domain name address): ")

# Set path to folder where you want to save your project
Path_To_Project_Dir = raw_input("Enter path to folder where you want to save your project: ")

# Scanning starts here
print "\nScanning started.\n"

FileSetter.create_main_directory(Path_To_Project_Dir)
FileSetter.create_all_results_txt_file(Path_To_Project_Dir)

print "\nResults will be stored in " + os.path.join(Path_To_Project_Dir + '/XSS_Results.txt') + "\n"


# Function that returns id's of input fields of a given url
def id_crawler(url):

    ids = []
    try:
        x = urllib.urlopen(url)
        y = x.read()

        inputs = re.findall(r'<input[^>]* name="([^"]*)"', y)

        for input in inputs:
            ids.append(input)

    except (KeyError, ValueError, IndexError, IOError):
        pass

    if len(ids) > 0:
        return ids
    else:
        pass


id = id_crawler(start_link)

payloads = ["<script>alert('Test')</script>", "<script>alert('Hello')</script>"]


# This function takes a url and a text input field id and checks the url for a simple xss vulnerability
def xss_check(n, i, url):

        vulnerable = False

        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Firefox')]

        br.open(url)
        br.select_form(nr=0)

        try:
            br.form[id[n]] = payloads[i]

            #Press Submit
            sub = br.submit()

            # Print url after submitting
            print "URL to page after injecting payload: " + sub.geturl() + '\n'
            FileSetter.append_to_file(os.path.join(Path_To_Project_Dir, 'XSS_Results.txt'),
                                      "URL to page after injecting payload: " + sub.geturl() + '\n')
            response = br.open(sub.geturl())

            if payloads[i] in response.read():
                vulnerable = True
                FileSetter.append_to_file(os.path.join(Path_To_Project_Dir, 'XSS_Results.txt'),
                                          "Page is vulnerable here is the http response: \n" + br.open(
                                              sub.geturl()).read() + '\n')
                print "Page is vulnerable here is the http response:"
                response = br.open(sub.geturl())
                print response.read()

            else:
                response = br.open(sub.geturl())
                print response.read()

            br.close()
        except ValueError:
            pass

        try:
            if i < len(payloads):
                xss_check(n, i + 1, url)
            elif i >= len(payloads):
                xss_check(n + 1, 0, url)
        except IndexError:
            if not vulnerable:
                FileSetter.append_to_file(os.path.join(Path_To_Project_Dir, 'XSS_Results.txt'), 'All text input fields of url: ' + url + ' were checked, no vulnerabilities found' + '\n\n')
                print 'All text input fields of url: ' + url + ' were checked, no vulnerabilities found'
            elif vulnerable:
                FileSetter.append_to_file(os.path.join(Path_To_Project_Dir, 'XSS_Results.txt'), 'Vulnerabilities in: ' + url + ' were found!' + '\n\n')
                print 'Vulnerabilities in: ' + url + ' were found!'


try:
    xss_check(0, 0, start_link)
except:
    print "No pages with text input fields to check xss on"
