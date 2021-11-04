// title:  Viewer
// author: Decca/Rift & Tomee/Avena
// desc:   view tiles/sprites from memory
// script: js

// USAGE:
//
// CTRL - toggle Tiles/Sprites
// Up/Down - switch colormode
// Left/Right - switch pages

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
  print(" Bg  Fg",4,8,15)
  print(">   <",4+(t*20),8,15)
  print("Page: "+(Math.floor(r/16)),4,16,15)
  print("Mode: "+m,4,24,15)
  print("CTRL\n toggle\n Tiles or\n Sprites",4,40,15,false,1,true)
  print("Up/Down\n switch\n color\n mode",4,70,15,false,1,true)
  print("Left/Right\n switch\n pages",4,100,15,false,1,true)
}

// call the viewer
draw()

function TIC() {
  if (btnp(00,60,6) && m<8) {m=m*2; draw()}
  if (btnp(01,60,6) && m>2) {m=Math.floor(m/2); draw()} 
  if (btnp(03,60,6) && r<48) {r=r+16; draw()}
  if (btnp(02,60,6) && r>0) {r=r-16; draw()} 
  if (keyp(63,60,6)) {t=1-t; draw()}
}
