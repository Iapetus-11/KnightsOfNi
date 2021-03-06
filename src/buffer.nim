import strutils
import streams
import nimpy
import math

proc packVarintInto(s: Stream, num: int, maxBits: int = 32) {.discardable.} =
  var num = num

  let numMin = (-1 shl (maxBits - 1))
  let numMax = (1 shl (maxBits - 1))

  if not (numMin <= num and num < numMax):
    raise newException(ValueError, strutils.format("num doesn't fit in given range: {numMin} <= {num} < {numMax}"))

  if num < 0:
    num += 1 + 1 shl 32

  var b: int

  for i in countup(0, 10):
    b = num and 0x7F
    num = num shr 7

    s.write(uint8(b or (if num > 0: 0x80 else: 0)))

    if num == 0:
      break

proc packChunkSectionBlocks(blockStates: seq[seq[seq[int]]], bitsPerBlock: int): string =
  var outString: StringStream = newStringStream()
  let dataLen: int = int((16 * 16 * 16) * bitsPerBlock / 64)
  var data: seq[int64] = newSeq[int64](dataLen)
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

  packVarintInto(outString, len(data))

  for long in data:
    outString.write(long)

  return outString.readAll()
