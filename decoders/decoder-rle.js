// title:  RLE Decoder v5
// author: Decca/Rift
// desc:   decode rle to a string and raw-result to mem, 3 digits for width
// script: js

// DESCRIPTION
//
// store tiles/sprites (data) as rle-encoded string
//  format: <offset><width><rle-encoded colorvalues>
//  digits: <5 digits><3 digits><rest of digits>
//  offset: tiles = 08000 / 08100 / 08200 / 08300
//          sprites = 0c000 / 0c100 / 0c200 / 0c300
//          palette = 07F80 / systemfont = 28E08
//   width: 040 (64) up to 400 (1024)
//     rle: colorvalues in uppercase letters - A=0,B=1...P=15
//          repeat of values in digits - 0...9
//          easier decoding using different symbols for values vs. repeats
//          a single value has no repeat-digit: A
//          two same values have no repeat-digit, just double letters: AA
//          three or more same values are appended with repeat-digits: A2
//          three: the letter itself and two additional repeats: A2 > AAA
//          seven: the letter itself and six additional repeats: A6 > AAAAAAA
var gfx = "08000040MK4M3PMMKKM2NMMCFM2KMMEPM2PMMKKMMK4M3KM4AK2AM2"

// the offset from the raw-string can be overwritten by providing
// an optional address when calling the function: tomem(gfx,0x8400)

// CODEBLOCK

// the rle-decoder
function unpac(str) {
  var r=str.substring(0,5) // get (o)ffset into (r)aw data
  var r=r+str.substring(5,8) // get (w)idth into (r)aw data
  var e=str.substring(8,str.length) // remove header to get (e)ncoded data
  var d = "" // (d)ecoded data
  d = e.replace(/(\w)(\d+)/g, function(m,n,c){ // decode rle, (m)atch & (c)ounter
        return new Array( parseInt(c,10)+2 ).join(n);
      }
  )
    for (var x = 0;x <= d.length;x++) { // get (d)ecoded data into (r)aw data
      var r=r+(d.substring(x,x+1).charCodeAt()-65).toString(16)
  }
  return r
}

// the raw-decoder
function tomem(str,adr) {
  var o=adr || parseInt(str.substring(0,5),16) // get (o)ffset, from param or string
  var w=parseInt(str.substring(5,8),16)-1 // get (w)idth
  var d=str.substring(8,str.length) // remove header to get (d)ata
  var y=0
  for (var x = 0;x <= d.length;x++) { // write to mem
    var c=parseInt(d.substring(x,x+1),16) // get (c)olor value
    poke4(o+y,c); y=y+1
    if (y>w) {y=0; o=o+1024}
  }
}


// call the decoders
col = unpac(pal)
tomem(col)
pix = unpac(gfx)
tomem(pix)
