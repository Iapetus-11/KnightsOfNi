import nimpy

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
