// title:  Raw Decoder v4
// author: Decca/Rift
// desc:   just decode to memory
// script: js

// DESCRIPTION
//
// store tiles/sprites (data) as string
//  format: <offset><width><colorvalues>
//  digits: <5 digits><2 digits><rest of digits>
//  offset: tiles = 08000 / 08100 / 08200 / 08300
//          sprites = 0c000 / 0c100 / 0c200 / 0c300
//          palette = 07F80 / systemfont = 28E08
//   width: 08 (64) up to 80 (1024)
var gfx = "0800008caaaaaccccfccaacccdcc25cccacc4fcccfccaaccaaaaaccccaccccc0aaa0ccc"

// CODEBLOCK

// the raw decoder
function tomem(str) {
  var psi=parseInt
  var o=psi(str.substring(0,5),16) // get (o)ffset
  var w=psi(str.substring(5,7),16)*8-1 // get (w)idth
  var d=str.substring(7,str.length) // remove header to get (d)ata
  var y=0
  for (var x = 0;x <= d.length;x++) { // write to mem
    var c=psi(d.substring(x,x+1),16) // get (c)olor value
    poke4(o+y,c); y=y+1
    if (y>w) {y=0; o=o+1024}
  }
}

// call the decoder
tomem(pal)
tomem(gfx)
