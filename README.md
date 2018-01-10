# XSS-Scanner
A combination of crawling links and scanning each site for Cross Site Scripting Vulnerabilities 

How the scanner works:
First this scanner acts as a web crawler by scanning a given site for all its links. Then it will scan for text-input-fields in every found site, in which it then injects malicous javascript. It will then analyse the http-response for unescaped Javascript code that was send in a http-request first. That way it will determine whether or not a site is vulnerable to Cross Site Scripting.

