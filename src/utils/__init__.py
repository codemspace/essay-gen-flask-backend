import re

def extract_info_apa(reference):    
    match = re.search(r'(?P<author>.+?)\s+\((?P<year>\d{4})\)\.\s+(?P<title>.+?)\.\s+(.+)', reference)
    if match:
        return match.groupdict()
    else: None

def extract_info_mla(reference):
    match = re.search(r'(?P<author>.+?)\.\s+"(?P<title>.+?)\."\s+(.+),\s+(?P<year>\d{4})\.', reference)
    if match:
        return match.groupdict()
    else: None
    
def extract_info_harvard(reference):
    match = re.search(r'(?P<author>.+?)\s+\((?P<year>\d{4})\)\.\s+(?P<title>.+?)\.\s*(?P<publisher>.+)', reference)
    if match:
        return match.groupdict()
    else: None

def extract_info_oxford(reference):
    match = re.search(r"(?P<author>.+?)\.\s+'(?P<title>.+?)',\s+(?P<publisher>.+?),\s+(?P<year>\d{4})\.", reference)
    if match:
        return match.groupdict()
    else: None