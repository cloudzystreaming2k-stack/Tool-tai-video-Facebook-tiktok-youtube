import re

class URLParser:
    @staticmethod
    def detect_platform(url: str) -> str:
        url = url.lower()
        if "youtube.com" in url or "youtu.be" in url:
            return "youtube"
        elif "facebook.com" in url or "fb.watch" in url:
            return "facebook"
        elif "tiktok.com" in url:
            return "tiktok"
        elif "instagram.com" in url:
            return "instagram"
        elif "threads.net" in url:
            return "threads"
        return "unknown"
        
    @staticmethod
    def is_valid_url(url: str) -> bool:
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None
