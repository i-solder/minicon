#!/usr/bin/env python3

import getopt
import fileinput
import sys

# Usage
def usage():
    print("Usage: python3 " + sys.argv[0] + " [options]")
    print("""
Options:
  -h, --help             Display this information"
  --file=FILENAME        Parse file""")

# Print print packet
def print_packet(packet):
    if not packet:
        return
    msg = ""
    for v in packet:
        msg += " " + format(v, "02X")
    if len(packet) == 8:
        print("REQ:" + msg)
    else:
        print("RES:" + msg)

# Main
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf", ["help", "file="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    file_name = None
    for k, v in opts:
        if k in ("-h", "--help"):
            usage()
            sys.exit()
        elif k in ("-f", "--file"):
            file_name = v
        else:
            assert False, "unhandled option"

    state = 0
    packet = []

    if file_name:
        # From file
        f = open(file_name, "rb")
        c = f.read(1)
        while c:
            byte = ord(c)
            if state == 0:
                if byte == 0x02:
                    packet = [byte]
                    state = 1
            elif state == 1:
                if byte == 0x2F:
                    packet.append(byte)
                    state = 2
                else:
                    state = 0
            elif state == 2:
                if byte == 0x02:
                    c = f.read(1)
                    if c:
                        byte = ord(c)
                        if byte == 0x2F:
                            print_packet(packet)
                            state = 0
                            f.seek(-2, 1)
                        else:
                            packet.append(0x02)
                            f.seek(-1, 1)
                else:
                    packet.append(byte)

            c = f.read(1)



# Start
if __name__ == "__main__":
    main()
