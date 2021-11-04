-- title:  Raw Decoder v2
-- author: Decca/Rift
-- desc:   just decode to memory
-- script: lua

-- DESCRIPTION
--
-- store tiles/sprites (data) as string
--  format: <offset><width><colorvalues>
--  digits: <2 digits><2 digits><rest of digits>
--  offset: tiles = 80 / 81 / 82 / 83
--          sprites = c0 / c1 / c2 / c3
--   width: 08 (64) up to 80 (1024)
local gfx = "8008caaaaaccccfccaacccdcc25cccacc4fcccfccaaccaaaaaccccaccccc0aaa0ccc"

-- CODEBLOCK

-- the raw decoder
function tomem(str)
  local tnb=tonumber
  local o=tnb(str:sub(1,2),16)*256 -- get (o)ffset
  local w=tnb(str:sub(3,4),16)*8-1 -- get (w)idth
  local d=str:sub(5,str:len()) -- remove header to get (d)ata
  local y=0
  for x = 1,#d,1 do -- write to mem
    local c=tnb(d:sub(x,x),16) -- get (c)olor value
    poke4(o+y,c) y=y+1
    if y>w then y=0 o=o+1024 end
  end
end

-- call the decoder
tomem(gfx)