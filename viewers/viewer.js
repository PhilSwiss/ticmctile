// title:  Viewer incl. System Font Demo
// author: Decca/Rift, Tomee/Avena & Josh Goebel
// desc:   view tiles/sprites/charsets from memory
// script: js

// USAGE:
//
// CTRL - toggle Tiles/Sprites
// Up/Down - switch colormode
// Left/Right - switch pages
// TAB - display system font

// CODEBLOCK

// the viewer
m=2 // mode
t=0 // tiles/sprites
r=0 // range

function draw() {
  if (m==2 && r>0) {r=0}
  if (m==4 && r>16) {r=16}
  if (t==0) {s=r} else {s=r+(128*m)}
  poke4(2*0x03ffc,m)
  cls(0)
  for (var y = 0;y <= 128-8;y+=8) {
    for (var x = 0;x <= (m*64)-8;x+=8) {
      spr(s,x+56,y+4); s=s+1
    }
  }
  rect(184,2,56,132,00)
  rectb(54,2,132,132,10)
  print("Tiles",4-(t*32),4,15)
  print("Sprites",-40+(t*44),4,15)
  print("Page: "+(Math.floor(r/16)),4,12,15)
  print("Mode: "+m,4,20,15)
  print("CTRL\n toggle\n Tiles or\n Sprites",4,32,10,false,1,true)
  print("Up/Down\n switch\n color\n mode",4,62,10,false,1,true)
  print("Left/Right\n switch\n pages",4,92,10,false,1,true)
  print("TAB\n display\n system font",4,116,10,false,1,true)
}

// call the viewer
draw()

// system font demo - https://github.com/nesbox/TIC-80/wiki/system-font
offy=4
offx=65

function font() {
  cls()
  print("SYSTEM",0,5,12)
  print("FONT",0,12,12)
  print("CTRL\n back to\n Tiles or\n Sprites",0,24,10,false,1,true)
  for (var x = 0;x <= 15;x++) {
    off = x*16
    print(String("  "+off).slice(-3),offx-20,(x*8)+offy+1,14,true,1,true)
    for (var y = 0;y <= 15;y++) {
      char = (y*16)+x
      rect((x*11)+offx,(y*8)+offy,8,7,15)
      print(String.fromCharCode(char),(x*11)+offx,(y*8)+offy,12)
    }
  }
}

function TIC() {
  if (btnp(00,60,6) && m<8) {m=m*2; draw()}
  if (btnp(01,60,6) && m>2) {m=Math.floor(m/2); draw()} 
  if (btnp(03,60,6) && r<48) {r=r+16; draw()}
  if (btnp(02,60,6) && r>0) {r=r-16; draw()} 
  if (keyp(63,60,6)) {t=1-t; draw()}
  if (keyp(49,60,6)) {t=1-t; font()}
}
