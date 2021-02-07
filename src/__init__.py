import nimporter

# PyMine imports
from pymine.api.abc import AbstractChunkIO
from pymine.types.chunk import Chunk

# KnightsOfNi imports
import nim.chunkio as chunkio


class ChunkIO(AbstractChunkIO):
    calc_offset = staticmethod(chunkio.calc_offset)
    find_chunk = staticmethod(chunkio.find_chunk)

    def fetch_chunk(world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
        chunk_data, timestamp = chunkio.fetch_chunk(world_path, chunk_x, chunk_z)

    async def fetch_chunk_async(world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
        pass


async def setup(server, config: dict) -> None:
    if config.get("enabled", True):
        server.chunkio = ChunkIO


async def teardown(server) -> None:
    pass
