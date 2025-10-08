-- title:  RLE Decoder v5
-- author: Decca/Rift
-- desc:   decode rle to a string and raw-result to mem, 3 digits for width
-- script: lua

-- DESCRIPTION
--
-- store tiles/sprites (data) as rle-encoded string
--  format: <offset><width><rle-encoded colorvalues>
--  digits: <5 digits><3 digits><rest of digits>
--  offset: tiles = 08000 / 08100 / 08200 / 08300
--          sprites = 0c000 / 0c100 / 0c200 / 0c300
--          palette = 07F80 / systemfont = 28E08
--   width: 040 (64) up to 400 (1024)
--     rle: colorvalues in uppercase letters - A=0,B=1...P=15
--          repeat of values in digits - 0...9
--          easier decoding using different symbols for values vs. repeats
--          a single value has no repeat-digit: A
--          two same values have no repeat-digit, just double letters: AA
--          three or more same values are appended with repeat-digits: A2
--          three: the letter itself and two additional repeats: A2 > AAA
--          seven: the letter itself and six additional repeats: A6 > AAAAAAA
local gfx = "08000040MK4M3PMMKKM2NMMCFM2KMMEPM2PMMKKMMK4M3KM4AK2AM2"

-- the offset from the raw-string can be overwritten by providing
-- an optional address when calling the function: tomem(gfx,0x8400)

-- CODEBLOCK

-- the rle-decoder
function unpac(str)
  local r = str:sub(1,5) -- get (o)ffset into (r)aw data
  local r = r .. str:sub(6,8) -- get (w)idth into (r)aw data
  local e=str:sub(9,str:len()) -- remove header to get (e)ncoded data
  local d = "" -- (d)ecoded data
  for m, c in e:gmatch("(%u+)([^%u]+)") do -- decode rle, (m)atch & (c)ounter
    d = d .. m .. (m:sub(-1):rep(c)) -- (d)ecoded data
  end
  for x = 1,#d,1 do -- get (d)ecoded data into (r)aw data
    r = r .. string.format("%x",(string.byte(d:sub(x,x))-65))
  end
  return r
end

-- the raw-decoder
function tomem(str,adr)
  local o = adr or tonumber(str:sub(1,5),16) -- get (o)ffset, from param or string
  local w=tonumber(str:sub(6,8),16)-1 -- get (w)idth
  local d=str:sub(9,str:len()) -- remove header to get (d)ata
  local y=0
  for x = 1,#d,1 do -- write to mem
    local c=tonumber(d:sub(x,x),16) -- get (c)olor value
    poke4(o+y,c) y=y+1
    if y>w then y=0 o=o+1024 end
  end
end

-- call the decoders
col = unpac(pal)
tomem(col)
pix = unpac(gfx)
tomem(pix)
