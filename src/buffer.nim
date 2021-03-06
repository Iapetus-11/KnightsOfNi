import strutils
import streams
import nimpy

proc packVarint(num: var int, maxBits: int = 32): string =
  let numMin = (-1 shl (maxBits - 1))
  let numMax = (1 shl (maxBits - 1))

  if not (numMin <= num and num < numMax):
    raise newException(ValueError, strutils.format("num doesn't fit in given range: {numMin} <= {num} < {numMax}"))

  if num < 0:
    num += 1 + 1 shl 32

  var outString: StringStream = newStringStream()
  var b: int

  for i in countup(0, 10):
    b = num and 0x7F
    num = num shr 7

    outString.write(uint8(b or (if num > 0: 0x80 else: 0)))

    if num == 0:
      break

  return outString.readAll()

proc packChunkSectionBlocks(blockStates: seq, bitsPerBlock: int): string =
  if isNil(blockStates):
    return "\x00"

  var data: array[0..(16 ** 3 * bitsPerBlock div 64), byte]
  var individualValueMask: int = (1 shl bitsPerBlock) - 1

  for y in countup(0, 16):
    for z in countup(0, 16):
      for x in countup(0, 16):
        let blockNum: int = (((y * 16) + z) * 16) + x
        let startLong: int = (blockNum * bitsPerBlock) div 64
        let startOffset: int = (blockNum * bitsPerBlock) mod 64
        let endLong: int = ((blockNum + 1) * bitsPerBlock - 1) div 64

        let value = blockStates[x][y][z] and individualValueMask

        data[startLong] = data[startLong] or (value shl startOffset)

        if startLong != endLong:
          data[endLong] = value shr (64 - startOffset)
