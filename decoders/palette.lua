-- title:  Palette
-- author: Decca/Rift
-- desc:   just set a palette
-- script: lua

-- DESCRIPTION
--
--  format: <colorvalues> (16xRGB)
--  digits: <2 digits R><2 digits G><2 digits B>
local pal = "1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57"

-- CODEBLOCK

-- set the palette
function tovram(str)
  local o=0
  for c=1,#str,2 do -- walk colors
    local v=tonumber(str:sub(c,c+1),16) -- get color (v)alue
    poke(0x3fc0+o,v) o=o+1 -- set color
  end
end

-- call the palette-function
tovram(pal)
