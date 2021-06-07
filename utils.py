import string
import random
import time

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

def sleep(count):
  while count > 0:
    print("\rSleeping for " + str(count) + " seconds ....         ", end = '')
    time.sleep(1)
    count -= 1
  print("\r                                                            ")

def humanbytes(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)