-- title:  RLE Decoder v2
-- author: Decca/Rift
-- desc:   decode rle to memory
-- script: lua

-- DESCRIPTION
--
-- store tiles/sprites (data) as rle-encoded string
--  format: <offset><width><rle-encoded colorvalues>
--  digits: <2 digits><2 digits><rest of digits>
--  offset: tiles = 80 / 81 / 82 / 83
--          sprites = c0 / c1 / c2 / c3
--   width: 08 (64) up to 80 (1024)
--     rle: colorvalues in uppercase letters - A=0,B=1...P=15
--          repeat of values in digits - 0...9
--          easier decoding using different symbols for values vs. repeats
--          a single value has no repeat-digit: A
--          two same values have no repeat-digit, just double letters: AA
--          three or more same values are appended with repeat-digits: A2
--          three: the letter itself and two additional repeats: A2 > AAA
--          seven: the letter itself and six additional repeats: A6 > AAAAAAA
local gfx = "8008MK4M3PMMKKM2NMMCFM2KMMEPM2PMMKKMMK4M3KM4AK2AM2"

-- CODEBLOCK

-- the rle-decoder
function tomem(str)
  local o=tonumber(str:sub(1,2),16)*256 -- get (o)ffset
  local w=tonumber(str:sub(3,4),16)*8-1 -- get (w)idth
  local e=str:sub(5,str:len()) -- remove header to get (e)ncoded data
  local d = "" -- (d)ecoded data
  for m, c in e:gmatch("(%u+)([^%u]+)") do -- decode rle, (m)atch & (c)ounter
    d = d .. m .. (m:sub(-1):rep(c))  
  end
  local y=0
  for x = 1,#d,1 do -- write to mem
    local c=string.byte(d:sub(x,x))-65 -- get (c)olor value
    poke4(o+y,c) y=y+1
    if y>w then y=0 o=o+1024 end
  end
end

-- call the decoder
tomem(gfx)
