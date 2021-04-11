#!/usr/bin/python3
#
# TicMcTile - convert images to TIC-80 tiles or sprites
#
# Hint: python -m pip install pillow (install PIL on Windows)
#
# last updated by Decca / RiFT on 10.04.2021 00:45
#

# import modules
from PIL import Image
import argparse
import os.path
import sys


# replace argparse-error message with own, nicer help/usage
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print("Usage: ticmctile imagefile [OPTION...]\n"
              "Generate TIC-80 tile/sprite values from pixeled images\n"
              "\n"
              "mandatory arguments:\n"
              "  imagefile          imagefile with pixeled graphics (e.g.: .png, .gif, etc.)\n"
              "\n"
              "optional arguments:\n"
              "  -o, --output       outputfile for tile/sprite values (e.g.: .lua)\n"
              "  -f, --force        force overwrite of outputfile when it already exist\n"
              "  -s, --sprites      export as sprites (FG) instead of tiles (BG)\n"
              "  -p, --page         start page (1-3) for tiles/sprites, default is 0\n"
              "  -b, --bank         memory bank (1-7) for TIC-80 PRO version, default is 1\n"
              "  -v, --version      show version info\n"
              "  -h, --help         show this help\n"
              "\n"
              "The optional arguments are only needed if the default setting doesnt meet the\n"
              "required needs. A specific name for the outputfile can be set (-o/--output).\n"
              "The data can be saved as sprites instead of tiles (-s / --sprites).\n"
              "Tiles/sprites can start on a different page (-p / --page) instead of 0.\n"
              "In the PRO version of TIC-80 there are up to 8 memory banks (-b / --bank)\n"
              "to store the tiles/sprites, instead of only one.\n"
              "\n"
              "examples:\n"
              "  ticmctile imagefile.png \n"
              "  ticmctile graphic.gif -o myticprog.lua\n"
              "  ticmctile logo.png -o tempvalues.lua -f\n"
              "  ticmctile goblins.gif -o sprites.txt -s\n"
              "  ticmctile font.png -o lettering.lua -p 2\n"
              "  ticmctile tilesgalore.gif -o membank3.lua -b 3\n", file=sys.stderr)
        self.exit(1, '%s: ERROR: %s\n' % (self.prog, message))


# set commandline arguments
parser = ArgumentParser(prog='TicMcTile', add_help=False)
parser.add_argument('image',
                    metavar='imagefile',
                    type=str,
                    help='imagefile with pixels')
parser.add_argument('-o', '--output',
                    metavar='output.lua',
                    type=str,
                    action='store',
                    help='outputfile for sprite/tile values')
parser.add_argument('-f', '--force',
                    action='store_true',
                    help='force overwrite of outputfile')
parser.add_argument('-p', '--page',
                    metavar='0',
                    const=0,
                    default=0,
                    choices=range(0, 4),
                    type=int,
                    nargs='?',
                    action='store',
                    help='start page (1-3) for sprite/tiles, default is 0')
parser.add_argument('-s', '--sprites',
                    action='store_true',
                    help='export sprites instead of tiles')
parser.add_argument('-b', '--bank',
                    metavar='1',
                    const=1,
                    choices=range(1, 8),
                    type=int,
                    nargs='?',
                    action='store',
                    help='memory bank (1-7) for TIC-80 PRO version, default is 1')
parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s 1.0')
args = parser.parse_args()


# get commandline arguments
imageFile = args.image
outputFile = args.output
outputForce = args.force
outputPage = args.page
outputSprites = args.sprites
outputBank = args.bank


# load image file
print("       Image: " + imageFile)
try:
    orgImg = Image.open(imageFile)
except Exception as error:
    print("ERROR: " + str(error), file=sys.stderr)
    exit(1)


# get image mode & format
orgMode = orgImg.mode
orgFormat = orgImg.format
orgFormat = '.' + orgFormat.lower()
print("      Format: " + orgFormat + " (" + orgMode + ")")


# get image dimensions
orgSizeX, orgSizeY = orgImg.size
print("  Resolution: " + str(orgSizeX) + " x " + str(orgSizeY))


# get image colors & amount
orgColors = orgImg.convert('RGB').getcolors(maxcolors=(orgSizeX * orgSizeY))
print("      Colors: " + str(len(orgColors)))


# set global parameter by color amount
if 0 <= len(orgColors) <= 2:
    digits = 1
elif 3 <= len(orgColors) <= 4:
    digits = 2
elif 5 <= len(orgColors) <= 16:
    digits = 4
else:
    print("ERROR: image has more than 16 colors")
    exit(1)


# check image mode and convert if neccessary
if orgMode != 'P':
    srcImg = orgImg.convert("P", palette=Image.ADAPTIVE, colors=len(orgColors))
    print("     WARNING: image converted to indexed colors, results may vary")
else:
    srcImg = orgImg


# check image dimensions
if orgSizeY > 128:
    print("ERROR: image is higher than 128 pixels")
    exit(1)
if outputPage == 0:
    maxSizeX = 512 // digits
    if orgSizeX > maxSizeX:
        print("ERROR: image cant be wider than " + str(maxSizeX) + " pixels")
        exit(1)
else:
    maxSizeX = (512 // digits) - (128 * outputPage)
    if orgSizeX > maxSizeX:
        print("ERROR: image starting at page " + str(outputPage) + " cant be wider than " + str(maxSizeX) + " pixels")
        exit(1)


# set string for output file
if not outputSprites:
    outputString = "TILES"
else:
    outputString = "SPRITES"


# set or init vars
offsetX = 0
offsetY = 0
stepsX = 32 // digits
adrOffset = outputPage * 4
address = adrOffset
digitString = "0" + str(digits) + "b"


# get a tile as 32 bytes of pixel data
def get_tile():
    tileString = ""
    tileY = 0
    while tileY < 8:
        doubleWord = ""
        tileX = 0
        while len(doubleWord) < 8:
            pixelByte = ""
            while len(pixelByte) < 8:
                if ((tileX + offsetX) < orgSizeX) and ((tileY + offsetY) < orgSizeY):  # check if position is in bounds
                    pixelBits = format(srcImg.getpixel((tileX + offsetX, tileY + offsetY)), digitString)  # get binary palette-index from pixel
                else:
                    pixelBits = format(0, digitString)  # if position is out of bounds, append zeros
                pixelByte = str(pixelBits) + pixelByte  # get bits in reversed order
                tileX = tileX + 1
            hexByte = '%0*x' % ((len(pixelByte) + 3) // 4, int(pixelByte, 2))  # convert byte to hex
            hexByte = hexByte[-1:] + hexByte[:1]  # swap low & high nibble
            doubleWord = doubleWord + hexByte  # add byte to doubleword
        tileString = tileString + doubleWord  # add doubleword to string
        tileY = tileY + 1
    return tileString


# get all tiles from the image
tiles = dict()
while offsetY < orgSizeY:
    while offsetX < orgSizeX:
        tiles[address] = get_tile()
        address = address + 1
        offsetX = offsetX + stepsX
    offsetY = offsetY + 8
    address = offsetY * 2 + adrOffset
    offsetX = 0
print("   generated: " + str(len(tiles)) + " " + outputString.lower())


# set memory bank if set
if outputBank:
    outputString = outputString + str(outputBank)
    print("  Memorybank: " + str(outputBank))


# generate name for output file if not set
if not isinstance(outputFile, str):
    outputFile = os.path.splitext(imageFile)[0]+'.lua'


# check if output file already exist
def check_file(outputName):
    if not outputForce:
        if os.path.isfile(outputName):
            print("ERROR: file already exist")
            exit(1)
    else:
        return


# save data to output file
print(" try to save: " + str(outputFile))
check_file(outputFile)
try:
    with open(outputFile, 'w') as file:
        file.write("-- title:  " + str(imageFile) + "\n-- author: TicMcTile\n-- script: lua\n")  # write header
        file.write("\nfunction TIC()\n print(\"...press ESC to continue!\",7,43)\nend\n\n")
        file.write("-- <PALETTE>\n")
        file.write("-- 000:1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57\n")  # SWEETIE-16 palette
        file.write("-- </PALETTE>\n\n")
        file.write("-- <" + outputString + ">\n")
        for tile in tiles:
            file.write("-- " + format(tile, "03d") + ":" + tiles[tile] + "\n")  # write content
        file.write("-- </" + outputString + ">\n")  # write footer
except Exception as error:
    print("ERROR: " + str(error), file=sys.stderr)
    exit(1)


# end message
print(" done.")
