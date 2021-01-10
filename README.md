# What is it

A webserver to search epub file text with calibre installed

# Feature
* Search texts inside epub files that are tracked by calibre app
* Filter by tag name in epub metadata
* Configure how much context should be displayed.

# Installation
1. Make suer calibre is installed, and all its binary commanline executables are available in PATH, especially `calibredb`.
2. Run `pip3 install -r requirements.txt`
3. Run `python3 app.py` and it will run the web server locally at port 5000. 
4. Use browser to open `127.0.0.1:5000` and now, you can search text and see the results in the webpage.

## Credits
The main logic of finding texts inside epub is from https://github.com/Grollicus/epubgrep.py/blob/master/epubgrep.py with some modifications to suit my needs.

