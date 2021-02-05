import bitops

proc calc_offset(chunk_x: int, chunk_z: int): int =
  return 4 * (bitops.bitand(chunk_x, 31) + bitops.bitand(chunk_z, 31) * 32)

proc find_chunk(location: int): tuple =
  var offset: int = bitops.bitand(bitops.rotateRightBits(location, 8), 0xFFFFFF)
  var size: int = bitops.bitand(location, 0xFF)

  return (offset * 4096, size * 4096)
