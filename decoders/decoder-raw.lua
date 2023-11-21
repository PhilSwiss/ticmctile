-- title:  Raw Decoder v4
-- author: Decca/Rift
-- desc:   just decode to memory
-- script: lua

-- DESCRIPTION
--
-- store tiles/sprites (data) as string
--  format: <offset><width><colorvalues>
--  digits: <5 digits><2 digits><rest of digits>
--  offset: tiles = 08000 / 08100 / 08200 / 08300
--          sprites = 0c000 / 0c100 / 0c200 / 0c300
--          palette = 07F80 / systemfont = 28E08
--   width: 08 (64) up to 80 (1024)
local gfx = "0800008caaaaaccccfccaacccdcc25cccacc4fcccfccaaccaaaaaccccaccccc0aaa0ccc"

-- CODEBLOCK

-- the raw decoder
function tomem(str)
  local tnb=tonumber
  local o=tnb(str:sub(1,5),16) -- get (o)ffset
  local w=tnb(str:sub(6,7),16)*8-1 -- get (w)idth
  local d=str:sub(8,str:len()) -- remove header to get (d)ata
  local y=0
  for x = 1,#d,1 do -- write to mem
    local c=tnb(d:sub(x,x),16) -- get (c)olor value
    poke4(o+y,c) y=y+1
    if y>w then y=0 o=o+1024 end
  end
end

-- call the decoder
tomem(pal)
tomem(gfx)