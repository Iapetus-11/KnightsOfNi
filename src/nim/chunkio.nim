import bitops

proc calc_offset(chunk_x: int, chunk_z: int): int =
  return 4 * (bitops.bitand(chunk_x, 31) + bitops.bitand(chunk_z, 31) * 32)
