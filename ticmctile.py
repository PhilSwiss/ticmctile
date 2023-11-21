#!/usr/bin/python3
#
# TicMcTile - convert images to TIC-80 tiles or sprites
#
# Done:
# - resolution of image no longer has to be dividble by 8
# - different image sizes per color
# - export as tiles (BG) or sprites (FG)
# - optional page selection
# - convert RGB to Palette if neccessary
# - optional memory banks for the PRO version
# - export as JavaScript (.js) - replace "-- " with "// "
# - keep palette of original image
# - inline code feature
# - bonus: real compression
# - fixed bug: when calculating start address for pages, the amount of colors was not respected
# - fixed bug: error message for images too wide for pages greater 0 was improved
# - fixed bug: replace 2nd if with elif in the rle-encoder
# - fixed bug: append zero to rle enc-string to fix decoder-bug (flush last values)
# - removed palette-decoder: the palette-data is now working with the same decoder as the pixeldata
# - Charset-mode: eleminate the need for the big gaps between letters in the source image
# - Charset-mode: show error when the image has more than 2 colors
# - Charset-mode: when RLE is used, to many zeroes are stored at the end
# - include viewer and decoder NON-Path relative
# - write tests
# - doc: how to load files / import code
#
# ToDo (Version 3):
# - reduce languages to Lua and Javascript, the rest seems to be useless
# - default output should be raw nowadays, not config
# - lz-based compression

# import modules
from PIL import Image
import argparse
import os.path
import sys


# replace argparse-error message with own, nicer help/usage
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print("Usage: ticmctile.py imagefile [OPTION...]\n"
              "Generate TIC-80 tile/sprite or charset values from pixeled images\n"
              "\n"
              "mandatory arguments:\n"
              "  imagefile          imagefile with pixeled graphics (e.g.: .png, .gif, etc.)\n"
              "\n"
              "optional arguments:\n"
              "  -o, --output       outputfile for tile/sprite or charset values (e.g.: .lua)\n"
              "  -l, --language     output as: js, fennel, wren, moon or squirrel, default is lua\n"
              "  -f, --force        force overwrite of outputfile when it already exist\n"
              "  -s, --sprites      export as sprites instead of tiles\n"
              "  -c, --charset      export as charset to replace the systemfont\n"
              "  -p, --page         start page (1-3) for tiles/sprites, default is 0\n"
              "  -m, --mode         mode to encode as: raw, rle, binary, default is config\n"
              "  -b, --bank         memory bank (1-7) for TIC-80 PRO version, default is 1\n"
              "  -k, --keep         keep colors of imagefile to adjust the TIC-80 palette\n"
              "  -v, --version      show version info\n"
              "  -h, --help         show this help\n"
              "\n"
              "The optional arguments are only needed if the default setting does not meet the\n"
              "required needs. A specific name for the output file (-o / --output) can be set.\n"
              "The output can be in different scripting languages (-l / --language). Lua is\n"
              "default, but the following languages are also supported: JavaScript, Squirrel,\n"
              "Fennel, Wren and Moonscript. Dont expect too much, is just different formatting.\n"
              "The data can be saved as sprites (-s / --sprites) instead of tiles.\n"
              "Tiles/sprites can start on a different page (-p / --page) instead of 0.\n"
              "Mode (-m / --mode) to encode the tiles/sprites as part of the code as raw, rle,\n"
              "as a binary-file (binary) or as part of the config, which is the default.\n"
              "Replace the systemfont with a correct formated charset (-c / --charset).\n"
              "To replace the smallfont choose (-p 1 / --page 1) instead of 0, which is default.\n"
              "In the PRO version of TIC-80 there are up to 8 memory banks (-b / --bank)\n"
              "to store the tiles/sprites, instead of only one. The colors of the image can\n"
              "be kept (-k / --keep), replacing the default colors (Sweetie-16) of the TIC-80.\n"
              "\n"
              "examples:\n"
              "  ticmctile.py imagefile.png \n"
              "  ticmctile.py graphic.gif -o myticprog.lua\n"
              "  ticmctile.py pixels.bmp -o javascript.js -l js\n"
              "  ticmctile.py logo.png -o tempvalues.lua -f\n"
              "  ticmctile.py goblins.gif -o sprites.lua -s\n"
              "  ticmctile.py atothez.png -o lettering.lua -p 2\n"
              "  ticmctile.py flextiles.bmp -o thecodeinside.lua -m rle\n"
              "  ticmctile.py dafont.png -o freshchars.lua -m raw -c\n"
              "  ticmctile.py tilesgalore.gif -o membank3.lua -b 3\n"
              "  ticmctile.py nicecolors.png -o mypalette.lua -k \n", file=sys.stderr)
        self.exit(1, '%s: ERROR: %s\n' % (self.prog, message))


# set commandline arguments
parser = ArgumentParser(prog='TicMcTile', add_help=False)
parser.add_argument('image',
                    metavar='imagefile',
                    type=str,
                    help='imagefile with pixels')
parser.add_argument('-o', '--output',
                    metavar='outputfile',
                    type=str,
                    action='store',
                    help='outputfile for sprite/tile values')
parser.add_argument('-l', '--language',
                    metavar='language',
                    const='lua',
                    default='lua',
                    choices=('js', 'fennel', 'wren', 'moon', 'squirrel', 'lua'),
                    type=str,
                    nargs='?',
                    action='store',
                    help='language for the outputfile')
parser.add_argument('-f', '--force',
                    action='store_true',
                    help='force overwrite of outputfile')
parser.add_argument('-p', '--page',
                    metavar='page',
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
parser.add_argument('-c', '--charset',
                    action='store_true',
                    help='export charset for systemfont')
parser.add_argument('-m', '--mode',
                    metavar='mode',
                    const='config',
                    default='config',
                    choices=('raw', 'rle', 'binary', 'config'),
                    type=str,
                    nargs='?',
                    action='store',
                    help='store data in other formats then config')
parser.add_argument('-b', '--bank',
                    metavar='membank',
                    const=1,
                    choices=range(1, 8),
                    type=int,
                    nargs='?',
                    action='store',
                    help='memory bank (1-7) for TIC-80 PRO version, default is 1')
parser.add_argument('-k', '--keep',
                    action='store_true',
                    help='keep original image colors')
parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s 2.2')
args = parser.parse_args()


# check charset argument
if args.charset and args.mode == "config":
    parser.error("charset-option is not supported in config-mode")


# get commandline arguments
imageFile = args.image
outputFile = args.output
outputLang = args.language
outputEnc = args.mode
outputForce = args.force
outputKeep = args.keep
outputPage = args.page
outputSprites = args.sprites
outputCharset = args.charset
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
if outputCharset and len(orgColors) > 2:
    print("ERROR: charset has more than 2 colors")
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
        print("ERROR: image with " + str(len(orgColors)) + " colors cant be wider than " + str(maxSizeX) + " pixels")
        exit(1)
else:
    maxSizeX = (512 // digits) - (128 * outputPage)
    if orgSizeX > maxSizeX:
        print("ERROR: image with " + str(len(orgColors)) + " colors and " + str(orgSizeX) + " pixels width cant start at page " + str(outputPage))
        exit(1)


# set palette for output file
stdPalette = "1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57"  # SWEETIE-16 palette
if not outputKeep:
    Palette = stdPalette
else:
    srcPalette = srcImg.getpalette()  # get original palette from image
    rgbEntries = (2 ** digits) * 3
    rgbPalette = srcPalette[:rgbEntries]
    Palette = ""
    for entry in rgbPalette:
        hexVal = '%0*x' % (2, entry)
        Palette = Palette + hexVal
    Palette = Palette + stdPalette[len(Palette):]  # fill up with default palette
if outputEnc == "raw" or outputEnc == "rle":
    # swap values (low & high nibble) for the unified decoder
    Palette = ''.join([Palette[val:val + 2][::-1] for val in range(0, len(Palette), 2)])  # (https://stackoverflow.com/a/4606057)


# set string for output file
if not outputSprites:
    outputString = "TILES"
else:
    outputString = "SPRITES"
if outputCharset:
    outputString = "CHARS"


# set or init vars
if outputCharset:
    stepsX = 8
else:
    stepsX = 32 // digits
offsetX = 0
offsetY = 0
adrOffset = (outputPage * 4) * digits
address = adrOffset
digitString = "0" + str(digits) + "b"
outputMsg = "...press ESC to continue!"


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
    rowValues = offsetX * (digits * 2)
    offsetX = 0
print("   generated: " + str(len(tiles)) + " " + outputString.lower())


# serialize tile values if needed
if outputEnc != "config":
    serialTiles = ""
    for tile in tiles:
        serialTiles = serialTiles + tiles[tile]
    # set memory offset & width
    if not outputSprites:
        offsetAdr = "08"  # Offset for tiles
    else:
        offsetAdr = "0c"  # Offset for sprites
    offsetAdr = offsetAdr + str(outputPage * digits) + "00"  # Offset for page
    hexWidth = '%0*x' % (2, rowValues // 8)  # Width aka Values per row


# reformat tile values if systemfont is replaced
if outputCharset:
    serialTiles = ''.join([serialTiles[val:val + 2] for val in range(0, len(serialTiles), 8)])
    serialTiles = serialTiles[:1520]  # truncate to max. 95 chars, to prevent overwriting of newline-settings
    if outputPage == 0:
        offsetAdr = "28E08"  # Offset for systemfont
    else:
        offsetAdr = "29608"  # Offset for smallfont
    hexWidth = '%0*x' % (2, len(serialTiles) // 8)  # Width aka Length of the Valuestring


# set memory bank if set
if outputBank:
    outputString = outputString + str(outputBank)
    print("  Memorybank: " + str(outputBank))


# set language specialties
if outputLang == "fennel":
    outputExt = ".fnl"
    outputCode = '(fn _G.TIC []\n (print (.. "' + outputMsg + '") 7 43)\n)'
    outputCmnt = ";; "
    outputVar = "let "
elif outputLang == "wren":
    outputExt = ".wren"
    outputCode = 'class Game is TIC {\n construct new() { TIC.print("' + outputMsg + '",7,43) }\n}'
    outputCmnt = "// "
    outputVar = "var "
elif outputLang == "squirrel":
    outputExt = ".nut"
    outputCode = 'function TIC() {\n print("' + outputMsg + '",7,43)\n}'
    outputCmnt = "// "
    outputVar = "local "
elif outputLang == "js":
    outputExt = ".js"
    outputCode = 'function TIC() {\n print("' + outputMsg + '",7,43)\n}'
    outputCmnt = "// "
    outputVar = "var "
elif outputLang == "moon":
    outputExt = ".moon"
    outputCode = 'export TIC=-> print("' + outputMsg + '",7,43)'
    outputCmnt = "-- "
    outputVar = "local "
else:
    outputExt = ".lua"
    outputCode = 'function TIC()\n print("' + outputMsg + '",7,43)\nend'
    outputCmnt = "-- "
    outputVar = "local "


# set file-extension for binary encoding
if outputEnc == "binary":
    outputExt = ".bin"


# include decoders for the encoded data
if outputEnc == "raw" or "rle":
    decoderFile = os.path.join(os.path.curdir, "decoders", "decoder-" + outputEnc + outputExt)
    if os.path.isfile(decoderFile):
        with open(decoderFile, "r") as file:
            fileLines = [line.strip('\n') for line in file.readlines()]
            codeStart = next((index for index, tag in enumerate(fileLines) if tag == outputCmnt + 'CODEBLOCK'), -1)
            outputDecoder = "\n".join(fileLines[codeStart + 1:]) + "\n"
    else:
        outputDecoder = '\n' + outputCmnt + "No " + outputEnc + "-decoder for " + outputLang + " found!\n"

    viewerFile = os.path.join(os.path.curdir, "viewers", "viewer" + outputExt)
    if os.path.isfile(viewerFile):
        with open(viewerFile, "r") as file:
            fileLines = [line.strip('\n') for line in file.readlines()]
            codeStart = next((index for index, tag in enumerate(fileLines) if tag == outputCmnt + 'CODEBLOCK'), -1)
            outputViewer = "\n".join(fileLines[codeStart + 1:]) + "\n"
    else:
        outputViewer = '\n' + outputCmnt + "No viewer for " + outputLang + " found!\n"


# generate name for output file if not set
if not isinstance(outputFile, str):
    outputFile = os.path.splitext(imageFile)[0] + outputExt  # replace file-extension
    outputFile = os.path.basename(outputFile)  # remove path if imagefile has one


# check if output file already exist
def check_file(fileName):
    if not outputForce:
        if os.path.isfile(fileName):
            print("ERROR: file already exist")
            exit(1)
    else:
        return


# encode data with Run-Length Encoding (only append number if value repeats more than twice)
def encode_rle(data):
    enc = ""
    prev = ""
    count = 1
    for symbol in data:
        value = chr(int(symbol, 16) + 65)
        if value != prev:
            if prev:
                enc = enc + prev
                if count == 2:
                    enc = enc + prev
                elif count > 2:
                    enc = enc + str(count - 1)
            count = 1
            prev = value
        else:
            count = count + 1
    enc = enc + prev
    if count == 2:
        enc = enc + prev
    elif count > 2:
        enc = enc + str(count - 1)
    if not enc[-1].isdigit():
        enc = enc + "0"
    return enc


# write data as BINARY output file
def write_binary():
    outputCode = ""
    outputCode = outputCode + offsetAdr
    outputCode = outputCode + str(hexWidth)
    outputCode = outputCode + serialTiles
    outputBytes = bytes.fromhex(outputCode)
    try:
        with open(outputFile, 'wb') as file:
            file.write(outputBytes)  # write binary stream
    except Exception as error:
        print("ERROR: " + str(error), file=sys.stderr)
        exit(1)
    return


# write data as CONFIG to output file
def write_config():
    try:
        with open(outputFile, 'w') as file:
            file.write(outputCmnt + "title:  " + str(imageFile) + "\n")  # write header
            file.write(outputCmnt + "author: TicMcTile\n")
            file.write(outputCmnt + "script: " + outputLang + "\n\n")
            file.write(outputCode + "\n\n")
            file.write(outputCmnt + "<PALETTE>\n")
            file.write(outputCmnt + "000:" + Palette + "\n")  # write palette
            file.write(outputCmnt + "</PALETTE>\n\n")
            file.write(outputCmnt + "<" + outputString + ">\n")
            for tile in tiles:
                file.write(outputCmnt + format(tile, "03d") + ":" + tiles[tile] + "\n")  # write content
            file.write(outputCmnt + "</" + outputString + ">\n")  # write footer
    except Exception as error:
        print("ERROR: " + str(error), file=sys.stderr)
        exit(1)
    return


# write data as RAW (unencoded) to output file
def write_raw():
    outputPalette = '\n' + outputVar + 'pal = "' + "07F80" + "0c" + Palette + '"\n'  # Offset and width for palette
    outputCode = '\n' + outputVar + 'gfx = "'
    outputCode = outputCode + offsetAdr
    outputCode = outputCode + str(hexWidth)
    outputCode = outputCode + serialTiles + '"\n'
    try:
        with open(outputFile, 'w') as file:
            file.write(outputCmnt + "title:  " + str(imageFile) + "\n")  # write header
            file.write(outputCmnt + "author: TicMcTile\n")
            file.write(outputCmnt + "script: " + outputLang + "\n")
            file.write(outputPalette)
            file.write(outputCode)
            file.write(outputDecoder)
            file.write(outputViewer)
    except Exception as error:
        print("ERROR: " + str(error), file=sys.stderr)
        exit(1)
    return


# write data as RLE-encoded to output file
def write_rle():
    encPalette = encode_rle(Palette)
    outputPalette = '\n' + outputVar + 'pal = "' + "07F80" + "0c" + encPalette + '"\n'  # Offset and width for palette
    outputCode = '\n' + outputVar + 'gfx = "'
    outputCode = outputCode + offsetAdr
    outputCode = outputCode + str(hexWidth)
    # encode serialized tile values
    encData = encode_rle(serialTiles)
    outputCode = outputCode + encData + '"\n'
    try:
        with open(outputFile, 'w') as file:
            file.write(outputCmnt + "title:  " + str(imageFile) + "\n")  # write header
            file.write(outputCmnt + "author: TicMcTile\n")
            file.write(outputCmnt + "script: " + outputLang + "\n")
            file.write(outputPalette)
            file.write(outputCode)
            file.write(outputDecoder)
            file.write(outputViewer)
    except Exception as error:
        print("ERROR: " + str(error), file=sys.stderr)
        exit(1)
    return


# write the data with the choosen encoding
print("    Encoding: " + str(outputEnc))
print(" try to save: " + str(outputFile))
check_file(outputFile)
if outputEnc == "binary":
    write_binary()
elif outputEnc == "raw":
    write_raw()
elif outputEnc == "rle":
    write_rle()
else:
    write_config()


# end message
print(" done.")


# end of code
exit()
