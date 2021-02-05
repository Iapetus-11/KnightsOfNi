import bitops

proc calc_offset(chunk_x: int32, chunk_z: int32): int32 =
  return 4 * (bitops.bitand(chunk_x, 31) + bitops.bitand(chunk_z, 31) * 32)

proc find_chunk(location: uint32): array[0..1, uint32] =
  let offset: uint32 = bitops.bitand(bitops.rotateRightBits(location, 8), 0xFFFFFF)
  let size: uint32 = bitops.bitand(location, 0xFF)

  return [offset * 4096, size * 4096]
