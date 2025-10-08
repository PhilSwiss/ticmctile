// title:  Raw Decoder v5
// author: Decca/Rift
// desc:   just decode to memory, incl. adr-param, 3 digits for width
// script: js

// DESCRIPTION
//
// store tiles/sprites (data) as string
//  format: <offset><width><colorvalues>
//  digits: <5 digits><3 digits><rest of digits>
//  offset: tiles = 08000 / 08100 / 08200 / 08300
//          sprites = 0c000 / 0c100 / 0c200 / 0c300
//          palette = 07F80 / systemfont = 28E08
//   width: 040 (64) up to 400 (1024)
var gfx = "08000040caaaaaccccfccaacccdcc25cccacc4fcccfccaaccaaaaaccccaccccc0aaa0ccc"

// the offset from the data-string can be overwritten by providing
// an optional address when calling the function: tomem(gfx,0x8400)

// CODEBLOCK

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

// call the decoder
tomem(pal)
tomem(gfx)
