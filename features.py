import re
def url_length(url):
    return len(url)
def count_dots(url):
    return url.count(".")
def has_ip_address(url):
    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    if re.search(pattern, url):
        return 1
    else:
        return 0
def has_at_symbol(url):
    if "@" in url:
        return 1
    else:
        return 0
def count_hyphens(url):
    return url.count("-")
def has_https(url):
    if url.startswith("https"):
        return 1
    else:
        return 0
def count_slashes(url):
  return url.count("/")
def count_digits(url):
  count = 0
  for char in url:
    if char.isdigit():
      count += 1
  return count
def has_suspicious_words(url):
  words = ["login", "verify", "secure", "account", "update", "confirm"]
  url_lower = url.lower()
  for word in words:
    if word in url_lower:
      return 1
  return 0
