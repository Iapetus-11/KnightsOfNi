import nimporter
import zlib

# PyMine imports
from pymine.logic.worldio import ChunkIO as DefaultChunkIO
from pymine.api.abc import AbstractChunkIO
from pymine.types.buffer import Buffer
from pymine.types.chunk import Chunk
from pymine.api import call_async
import pymine.types.nbt as nbt

# KnightsOfNi imports
import chunkio


class ChunkIO(AbstractChunkIO):
    calc_offset = staticmethod(chunkio.calc_offset)
    find_chunk = staticmethod(chunkio.find_chunk)

    @classmethod
    def fetch_chunk(cls, world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
        chunk_data, timestamp = chunkio.fetch_chunk(world_path, chunk_x, chunk_z)

        chunk_data = nbt.TAG_Compound.unpack(Buffer(zlib.decompress(chunk_data)))

        return Chunk(chunk_data, timestamp)

    @classmethod
    async def fetch_chunk_async(cls, world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
        return await call_async(cls.fetch_chunk, world_path, chunk_x, chunk_z)


async def setup(server, config: dict) -> None:
    if config.get("enabled", True):
        server.chunkio = ChunkIO


async def teardown(server) -> None:
    server.chunkio = DefaultChunkIO
