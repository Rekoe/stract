#!/usr/bin/env python3

# Stract by Sam Foster, April 2022

# Takes a filename and 2 offsets in hex or decimal. first byte and last byte.
# Extract that chunk into a new file 

# This program requires the program "dd" which should be preinstalled on any Unix or Linux system.
# It should work in Windows if you have "dd" installed and in the path.

import sys
import os

def print_help():
    print("Usage: %s inputfile outputfile firstbye [lastbyte]\n" % sys.argv[0])
    print("Extract/carve out segments of a binary (or any) file into a new file.")
    print("Firstbye and lastbye offsets can be in decimal or hex (prefix with 0x for hex).")
    print("Omit 'lastbyte' to copy until it reaches the end of the file.")


def main():
    if len(sys.argv) < 4:
        print_help()
        exit(1)

    # etract data from command-line
    s_infile = sys.argv[1]
    s_outfile = sys.argv[2]
    s_first_byte = sys.argv[3]
    if len(sys.argv) == 5:
        s_last_byte = sys.argv[4]
        b_copy_to_end = False
    else:
        b_copy_to_end = True
    i_first_byte = int(s_first_byte, 0)
    if not b_copy_to_end:
        i_last_byte = int(s_last_byte, 0)
        i_file_size = i_last_byte - i_first_byte + 1

    # Generate dd command and print status message
    if b_copy_to_end:
        s_dd_command = "dd if=%s of=%s bs=1 skip=%i" % (s_infile, s_outfile, i_first_byte)
        print("Extracting bytes %i to the end of the file from %s..." % (i_first_byte, s_infile))
    else:
        s_dd_command = "dd if=%s of=%s bs=1 skip=%i count=%i" % (s_infile, s_outfile, i_first_byte, i_file_size)
        print("Extracting bytes %i to %i (%i bytes total) from %s..." % (i_first_byte, i_last_byte, i_file_size, s_infile))
    print("Running:", s_dd_command)

    # run it    
    dd_return = os.system(s_dd_command)
    if dd_return == 0:
        print("Wrote to file: %s" % (s_outfile))
    else:
        print("That didn't seem to work. Please check the above output for errors. (Is 'dd' installed on your system and in your path?)")
        exit(1)

if __name__ == '__main__':
    main()

