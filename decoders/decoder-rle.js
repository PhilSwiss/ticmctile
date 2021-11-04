// title:  RLE Decoder v2
// author: Decca/Rift
// desc:   decode rle to memory
// script: js

// DESCRIPTION
//
// store tiles/sprites (data) as rle-encoded string
//  format: <offset><width><rle-encoded colorvalues>
//  digits: <2 digits><2 digits><rest of digits>
//  offset: tiles = 80 / 81 / 82 / 83
//          sprites = c0 / c1 / c2 / c3
//   width: 08 (64) up to 80 (1024)
//     rle: colorvalues in uppercase letters - A=0,B=1...P=15
//          repeat of values in digits - 0...9
//          easier decoding using different symbols for values vs. repeats
//          a single value has no repeat-digit: A
//          two same values have no repeat-digit, just double letters: AA
//          three or more same values are appended with repeat-digits: A2
//          three: the letter itself and two additional repeats: A2 > AAA
//          seven: the letter itself and six additional repeats: A6 > AAAAAAA
var gfx = "8008MK4M3PMMKKM2NMMCFM2KMMEPM2PMMKKMMK4M3KM4AK2AM2"

// CODEBLOCK

// the rle-decoder
function tomem(str) {
  var o=parseInt(str.substring(0,2),16)*256 // get (o)ffset
  var w=parseInt(str.substring(2,4),16)*8-1 // get (w)idth
  var e=str.substring(4,str.length) // remove header to get (e)ncoded data
  var d = "" // (d)ecoded data
  d = e.replace(/(\w)(\d+)/g, function(m,n,c){ // decode rle, (m)atch & (c)ounter
        return new Array( parseInt(c,10)+2 ).join(n);
      }
  )
  var y=0
  for (var x = 0;x <= d.length;x++) { // write to mem
    var c=d.substring(x,x+1).charCodeAt()-65 // get (c)olor value
    poke4(o+y,c); y=y+1
    if (y>w) {y=0; o=o+1024}
  }
}

// call the decoder
tomem(gfx)
