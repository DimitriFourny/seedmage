"""Helper methods to encode and decode Bencoding data."""

def _decode(raw_buffer, elements, index=0):
    if raw_buffer[index] == ord('d'):
        index += 1
        obj = {}
        while raw_buffer[index] != ord('e'):
            key = []
            value = []
            index = _decode(raw_buffer, key, index)
            index = _decode(raw_buffer, value, index)
            obj[key[0]] = value[0]
        index += 1
        elements.append(obj)
    elif raw_buffer[index] == ord('l'):
        index += 1
        list_elements = []
        while raw_buffer[index] != ord('e'):
            value = []
            index = _decode(raw_buffer, value, index)
            list_elements.append(value[0])
        index += 1
        elements.append(list_elements)
    elif raw_buffer[index] == ord('i'):
        index += 1
        pos = index + raw_buffer[index:].find(ord('e'))
        number = int(raw_buffer[index:pos])
        index = pos+1
        elements.append(number)
    else:
        pos = index + raw_buffer[index:].find(ord(':'))
        size = int(raw_buffer[index:pos])
        index = pos+1
        data = raw_buffer[index:index+size]
        index += size
        elements.append(data)
    return index

def decode(raw_buffer):
  """Decode a bytes string into its corresponding data via Bencoding."""
  elements = []
  _decode(raw_buffer, elements)
  return elements[0]

def encode(data):
  """Encode data into a bytes string via Bencoding."""
  if isinstance(data, bytes):
    return str(len(data)).encode("ascii") + b':' + data
  elif isinstance(data, str):
    return encode(data.encode("ascii"))
  elif isinstance(data, int):
    return  b'i' + str(data).encode("ascii") + b'e'
  elif isinstance(data, list):
    result = b'l'
    for d in data:
      result += encode(d)
    result += b'e'
    return result
  elif isinstance(data, dict):
    result = b'd'
    for key, value in data.items():
      result += encode(key)
      result += encode(value)
    result += b'e'
    return result

  raise ValueError("Unexpected bencode_encode() data")
