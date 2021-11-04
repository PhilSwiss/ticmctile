-- title:  Viewer
-- author: Decca/Rift
-- desc:   view tiles/sprites from memory
-- script: lua

-- USAGE:
--
-- CTRL - toggle Tiles/Sprites
-- Up/Down - switch colormode
-- Left/Right - switch pages

-- CODEBLOCK

-- the viewer
m=2 -- mode
t=0 -- tiles/sprites
r=0 -- range

function draw()
  if m==2 and r>0 then r=0 end
  if m==4 and r>16 then r=16 end
  if t==0 then s=r else s=r+(128*m) end
  poke4(2*0x03ffc,m)
  cls(0)
  for y = 0,128-8,8 do
    for x = 0,(m*64)-8,8 do
      spr(s,x+56,y+4) s=s+1
    end
  end
  rect(184,2,56,132,00)
  rectb(54,2,132,132,10)
  print(" Bg  Fg",4,8,15)
  print(">   <",4+(t*20),8,15)
  print("Page: "..(r//16),4,16,15)
  print("Mode: "..m,4,24,15)
  print("CTRL\n toggle\n Tiles or\n Sprites",4,40,15,false,1,true)
  print("Up/Down\n switch\n color\n mode",4,70,15,false,1,true)
  print("Left/Right\n switch\n pages",4,100,15,false,1,true)
end

-- call the viewer
draw()

function TIC()
  if btnp(00,60,6) and m<8 then m=m*2 draw() end
  if btnp(01,60,6) and m>2 then m=m//2 draw() end 
  if btnp(03,60,6) and r<48 then r=r+16 draw() end
  if btnp(02,60,6) and r>0 then r=r-16 draw() end 
  if keyp(63,60,6) then t=1-t draw() end
end
