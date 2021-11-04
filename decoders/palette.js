// title:  Palette
// author: Decca/Rift
// desc:   just set a palette
// script: js

// DESCRIPTION
//
// format: <colorvalues> (16xRGB)
// digits: <2 digits R><2 digits G><2 digits B>
var pal = "1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57"

// CODEBLOCK

// set the palette
function tovram(str) {
  var o=0
  for (var c=0;c<=str.length-1;c+=2) { // walk colors
    var v=parseInt(str.substring(c,c+2),16) // get color (v)alue
    poke(0x3fc0+o,v); o=o+1 // set color
  }
}

// call the palette-function
tovram(pal)
