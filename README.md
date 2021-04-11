![TicMcTile Logo](https://repository-images.githubusercontent.com/356870078/b9283c00-9ad7-11eb-980e-53f1262f85d8)

TicMcTile
========

Commandline tool to convert images to tiles or sprites for the [TIC-80](https://tic80.com/).

When developing a [game](https://en.wikipedia.org/wiki/Video_game) or a [demo](https://en.wikipedia.org/wiki/Demoscene), sooner or later you will need to add some nice [graphics](https://en.wikipedia.org/wiki/Pixel_art).

Of course those images can be loaded into the [sprite editor](https://github.com/nesbox/TIC-80/wiki#sprite-editor) by using the *import sprites*-[command](https://github.com/nesbox/TIC-80/wiki/Console#available-commands), after converting them to [GIF](https://en.wikipedia.org/wiki/GIF) first. And when you use the *save*-[command](https://github.com/nesbox/TIC-80/wiki/Console#available-commands), you can export these informations also to your sourcecode file.

But why do those steps manually, when you can just use a tool for that: **TicMcTile**

TicMcTile reads your imagefile(s) in a varity of [formats](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) and creates .[lua](https://www.lua.org/)-file(s) from it, which can be run/loaded by the [TIC-80](https://tic80.com/) or your favourite [editor](https://en.wikipedia.org/wiki/Text_editor)/[ide](https://en.wikipedia.org/wiki/Integrated_development_environment).

This tool can also stuff more tiles/sprites into your program, allowing you to import images as 4 or 2 color images instead of 16, thanks to a new [feature](https://github.com/nesbox/TIC-80/releases/tag/v0.80.1344) of the [TIC-80](https://tic80.com/).


Information
========
The [TIC-80](https://tic80.com/) [offers](https://github.com/nesbox/TIC-80/wiki) you 8192 bytes (8kb) for tiles (8x8 pixels), which can be used in the [map editor](https://github.com/nesbox/TIC-80/wiki#map-editor) or as sprites. Another 8192 bytes (8kb) can be used for regular sprites of the same pixel size.
You can have **one page** (128 x 128 pixels each) with up to 256 tiles and 256 sprites in total. Each one of these tiles/sprites will be stored in **32 bytes** of data, when using the default of 16 colors.
You can switch between both types in the upper, middle of the [sprite editor](https://user-images.githubusercontent.com/1101448/92114358-5d872900-edf9-11ea-8252-35b9c5c27083.png), by clicking on the **BG** (tiles) or **FG** (sprites) button.

A new feature introduced in version [0.80](https://github.com/nesbox/TIC-80/releases/tag/v0.80.1344) will allow you to have more tiles/sprites if less colors (4 or 2) are used.
This is accomplished by storing more **pixels per byte** into the **32 byte**-chunks already used for the 16 color tiles/sprites.
The 4 color-mode will then give you **two pages** (128 x 128 pixels each) for tiles and the same amount for regular sprites in the [sprite editor](https://user-images.githubusercontent.com/1101448/92114358-5d872900-edf9-11ea-8252-35b9c5c27083.png).
And 2 colors will result in **four pages** of the same size for each type. You can switch between those pages in the upper, right corner of the [sprite editor](https://user-images.githubusercontent.com/1101448/92114828-2a916500-edfa-11ea-9905-0650335f5860.png).
See this [animation](https://user-images.githubusercontent.com/1101448/92115601-5b25ce80-edfb-11ea-8153-3abc187153ac.gif) for a better explaination/usage of the [sprite editor](https://user-images.githubusercontent.com/1101448/92114828-2a916500-edfa-11ea-9905-0650335f5860.png).

But there is currently no easy way to use these extended capabilities with images made outside the [TIC-80](https://tic80.com/). The *import*-[command](https://github.com/nesbox/TIC-80/wiki/Console#available-commands) used with the [sprite editor](https://user-images.githubusercontent.com/1101448/92114828-2a916500-edfa-11ea-9905-0650335f5860.png) will always fall back to **one** page (128 x 128 pixels) with 16 colors each.
But **TicMcTile** comes to the rescue. It will convert your images (no matter if 16, 4 or 2 colors) into a .lua-file with the correct _encoding_ of the data. This file can then directly be used by the [TIC-80](https://tic80.com/) and its [sprite editor](https://user-images.githubusercontent.com/1101448/92114358-5d872900-edf9-11ea-8252-35b9c5c27083.png).

You can convert a **singlepage**-image (128x128 or smaller) and assign it to one of the avaliable pages, or you can use **multipage**-images. When using 4 colors, a **multipage** can be
**max. 256 pixels** wide & 128 pixels high. In case of 2 colors, a **multipage** can be **max. 512 pixels** wide & 128 pixels high. You can select whether the image(s) should be converted to tiles (default) or sprites.

Only images with **16 colors or less** are supported, for obvious reasons. These images should consist of [indexed colors](https://en.wikipedia.org/wiki/Indexed_color) or have a [color-palette](https://en.wikipedia.org/wiki/Palette_(computing)). Truecolor-images will be converted, but results may vary. Also make sure, that images match the [color-palette](https://github.com/nesbox/TIC-80/wiki/palette) [(SWEETIE-16)](https://lospec.com/palette-list/sweetie-16) of the **TIC-80**. Custom palettes are not yet supported.


Requirements
=============

- Python (3.5, 3.6, 3.7, 3.8, 3.9) - https://www.python.org/
- Pillow (Python Imaging Library) - https://pypi.org/project/Pillow/


Installation
=============
If missing, **Pillow** can be installed using **pip**.

Linux: 

    $ pip install pillow
Windows:

    $ python -m pip install pillow


Quickstart
==========

**TicMcTile** is straightforward to use, and its really easy to convert an image to TIC-80.
Just run `ticmctile` using the provided example images:

    $ ticmctile.py singlepage-16colors.png

    Will generate an output file called "singlepage-16colors.lua", can be opened with an editor or the TIC-80.

Specify a different name for the output file:

    $ ticmctile.py singlepage-2colors.png -o twocolors.lua
	
	At the moment its only possible to generate .lua files, sorry.

Generate a sprite page (FG) instead of a tile page (BG):

    $ ticmctile.py singlepage-4colors.png -o mysprites.lua -s

    In the Sprite editor of the TIC-80 you can switch between tiles (BG) and sprites (FG).

Start the tiles on a different page e.g. 1 instead of 0 (default):

    $ ticmctile.py multipage-2colors.png -o someotherpage.lua -p 1

    In the Sprite editor of the TIC-80 you can toggle between 4 different pages (when using 2 colors).

Save the tiles or sprites to a different memory bank, there is only 1 by default:

    $ ticmctile.py multipage-4colors.png -o bankbonkers.lua -b 7

    In the PRO Version of TIC-80 there are 8 memory banks instead of only 1.


Commandline options
===================

    $ ticmctile.py --help

    Usage: ticmctile imagefile [OPTION...]
    Generate TIC-80 tile/sprite values from pixeled images

    mandatory arguments:
       imagefile          imagefile with pixeled graphics (e.g.: .png, .gif, etc.)

    optional arguments:
       -o, --output       outputfile for tile/sprite values (e.g.: .lua)
       -f, --force        force overwrite of outputfile when it already exist
       -s, --sprites      export as sprites (FG) instead of tiles (BG)
       -p, --page         start page (1-3) for tiles/sprites, default is 0
       -b, --bank         memory bank (1-7) for TIC-80 PRO version, default is 1
       -v, --version      show version info
       -h, --help         show this help
     
    The optional arguments are only needed if the default setting doesnt meet the
    required needs. A specific name for the outputfile (-o/--output) can be set.
    The data can be saved as sprites (-s / --sprites) instead of tiles.
    Tiles/sprites can start on a different page (-p / --page) instead of 0.
    In the PRO version of TIC-80 there are up to 8 memory banks (-b / --bank)
    to store the tiles/sprites, instead of only one.

    examples:
       ticmctile imagefile.png
       ticmctile graphic.gif -o myticprog.lua
       ticmctile logo.png -o tempvalues.lua -f
       ticmctile goblins.gif -o sprites.txt -s
       ticmctile font.png -o lettering.lua -p 2
       ticmctile tilesgalore.gif -o membank3.lua -b 3


Files
=====

* ticmctile.py (the commandlinetool itself)
* singlepage-2colors.png (example image with 2 colors, [original](https://demozoo.org/graphics/3719/) by Decca/Lego)
* singlepage-4colors.png (example image with 4 colors, [original](https://demozoo.org/graphics/3719/) by Decca/Lego)
* singlepage-16colors.png (example image with 16 colors, [original](https://demozoo.org/graphics/3719/) by Decca/Lego)
* multipage-2colors.png (3 pages with 2 colors, [originals](https://demozoo.org/graphics/3719/) [both](https://demozoo.org/graphics/115000/) by Decca/Lego, font from [Chartist](https://github.com/PhilSwiss/chartist))
* multipage-4colors.png (2 pages with 4 colors, [originals](https://demozoo.org/graphics/3719/) [both](https://demozoo.org/graphics/115000/) by Decca/Lego)


Future ideas
============

* Output of other languages than Lua, e.g. JavaScript
* keeping the color-palette of the image, instead of using the default palette
* Real compression of the values incl. a small decompressor for [Lua](https://www.lua.org/) 


Disclaimer
==========

There is no warranty for the script or it's functionality, use it at your own risk.

The icon/logo consists of the [Sweetie 16](https://lospec.com/palette-list/sweetie-16)-palette © by [GrafxKid](https://grafxkid.tumblr.com/) & a [Clamp emoji clipart](https://creazilla.com/nodes/57040-clamp-emoji-clipart) © by [Creazilla](https://creazilla.com/).


Bug tracker
===========

If you have any suggestions, bug reports or annoyances please report them to the issue tracker at https://github.com/PhilSwiss/ticmctile/issues


Contributing
============

Development of `ticmctile` happens at GitHub: https://github.com/PhilSwiss/ticmctile
