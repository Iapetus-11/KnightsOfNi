import asyncio
import zlib

# PyMine imports
from pymine.logic.worldio import ChunkIO as DefaultChunkIO
from pymine.api.abc import AbstractChunkIO
from pymine.types.buffer import Buffer
from pymine.types.chunk import Chunk
import pymine.types.nbt as nbt

import pymine.types.buffer as buffer_module

# KnightsOfNi imports
import chunkio
import buffer


class ChunkIO(AbstractChunkIO):
    calc_offset = staticmethod(chunkio.calcOffset)
    find_chunk = staticmethod(chunkio.findChunk)

    @classmethod
    def fetch_chunk(cls, world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
        chunk_data, timestamp = chunkio.fetchChunk(world_path, chunk_x, chunk_z)

        chunk_nbt = nbt.TAG_Compound.unpack(Buffer(zlib.decompress(b"".join([ord(c).to_bytes(1, "big") for c in chunk_data]))))

        return Chunk(chunk_nbt, int(timestamp))

    @classmethod
    async def fetch_chunk_async(cls, world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
        return await asyncio.get_event_loop().run_in_executor(
            server.thread_executor, cls.fetch_chunk, world_path, chunk_x, chunk_z
        )


async def setup(server, config: dict) -> None:
    if config.get("enabled", True):
        server.chunkio = ChunkIO
        buffer_module.Buffer.pack_varint = buffer.packVarint
        buffer_module.Buffer.pack_chunk_section_blocks = buffer.packChunkSectionBlocks


async def teardown(server) -> None:
    server.chunkio = DefaultChunkIO
