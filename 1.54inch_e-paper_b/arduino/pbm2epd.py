import sys
import re

def main():

    # Read ASCII PBM from standard input
    lines = [l.strip() for l in sys.stdin.readlines() if l and l[0]!="#"]

    # Parse header
    if lines[0].upper()!="P1":
        sys.stderr.write("Input is not a raw PBM file\n")
        sys.exit(1)
    lines = lines[1:]
    try:
        ncols, nrows = [int(s) for s in lines[0].split(" ")]
        if nrows%8:
            sys.stderr.write(
                "Number of rows ({}) isn't divisible by 8\n".format(nrows))
            sys.exit(1)
        nbytes = nrows>>3
        lines = [re.sub('\s','',l) for l in lines[1:]]
        for l in lines:
            print l
    except:
        sys.stderr.write("Input should be an ASCII PBM file where number of rows is divisible by 8.\n")
        sys.exit(1)

    # Read pixels
    sys.stderr.write("Processing {}x{} bitmap...\n".format(ncols,nrows))
    pixels = []
    for l in lines:
        pixels += [c=="1" for c in l]
    if len(pixels)!=nrows*ncols:
        sys.stderr.write("Expected {} pixels, got {}.\n".format(ncols*nrows, len(pixels)))
        sys.exit(1)

    # Convert to E-Paper Display format
    epd_bytes = (nbytes*ncols)*[0]
    sys.stderr.write("Image bytes: {}\n".format(len(epd_bytes)))
    for r in range(nrows):
        for c in range(ncols):
           if not pixels[(r+1)*ncols-(c+1)]: # Inverted pixels, right to left scan
               epd_bytes[c*nbytes+(r>>3)] |= (0x80>>(r%8)) # top to bottom

    # Compress to RLE1B (1-bit run-length encoding), where
    # each byte is split into two 4-bit numbers:
    #   * Number of [max 15] zeros
    #   * Number of [max 15] ones
    compressed = []
    expected_value = 0
    counters = [0, 0]
    for b in epd_bytes:
        #print("0x{:b}".format(b))
        for digit in range(8):
            bit = b&(0x80>>digit) and 1 or 0
            if bit==expected_value:
                counters[expected_value] += 1
            if bit!=expected_value or counters[expected_value]==15:
                if expected_value==1: # send entire byte
                    compressed.append(16*counters[0]+counters[1])
                    #print("Ones: {} >>>compressed: 0x{:02x}>>>".format(
                    #    counters, compressed[-1]))
                else: # accumulate the zeros, wait for the ones
                    #print("Zeros: {}".format(counters))
                    pass
                expected_value = 1-expected_value
                counters[expected_value] = bit==expected_value and 1 or 0
    # Output remaining byte (if any)
    if counters[0] or counters[1]:
        compressed.append(16*counters[0]+counters[1])

    sys.stderr.write("Compressed {} bytes to {} ({:5.2f}%)\n".format(
        len(epd_bytes), len(compressed),
        100*(len(compressed)/len(epd_bytes))))

    # Print Arduino code to standard output
    print("""#include "imagedata.h"
#include <avr/pgmspace.h>
// RLE1B (1-bit run-length encoding) format, where
// each byte is split into two 4-bit numbers:
//   * Number of [max 15] zeros
//   * Number of [max 15] ones
const unsigned char BITMAP_NAME_GOES_HERE[] PROGMEM = {""")
    last_index = len(compressed)-1
    line = "    "
    for i,c in enumerate(compressed):
        line+="0x{:02x}".format(c)
        if i<last_index:
            line+=", " 
        if (i==last_index or i%16==15):
            print(line)
            line = "    "
    print("};")
if __name__=="__main__":
    main() 
