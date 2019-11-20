import string
import random

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def urlencode(bytes):
  result = ""
  valids = (string.ascii_letters + "_.").encode("ascii")
  for b in bytes:
    if b in valids:
      result += chr(b)
    elif b == " ":
      result += "+"
    else:
      result += "%%%02X" % b
  return result

def random_id(length):
  return ''.join(random.choices(string.ascii_letters + string.digits, k=length))