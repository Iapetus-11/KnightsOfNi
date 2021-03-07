import asyncio
import zlib

# PyMine imports
from pymine.logic.worldio import ChunkIO as DefaultChunkIO
from pymine.api.abc import AbstractChunkIO
from pymine.types.buffer import Buffer
from pymine.types.chunk import Chunk
import pymine.types.nbt as nbt

# KnightsOfNi imports
try:
    import chunkio
    import buffer
except ModuleNotFoundError:
    NIM_IMPORT_SUCCESS = False
else:
    NIM_IMPORT_SUCCESS = True


async def setup(server, config: dict) -> None:
    if config.get("enabled", True):
        if not NIM_IMPORT_SUCCESS:
            server.console.warning("KnightsOfNi: Failed to load nim extensions, KnightsOfNi will be disabled.")
            return

        class ChunkIO(AbstractChunkIO):
            calc_offset = staticmethod(chunkio.calcOffset)
            find_chunk = staticmethod(chunkio.findChunk)

            @classmethod
            def fetch_chunk(cls, world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
                chunk_data, timestamp = chunkio.fetchChunk(world_path, chunk_x, chunk_z)

                chunk_nbt = nbt.TAG_Compound.unpack(
                    Buffer(zlib.decompress(b"".join([ord(c).to_bytes(1, "big") for c in chunk_data])))
                )

                return Chunk(chunk_nbt, int(timestamp))

            @classmethod
            async def fetch_chunk_async(cls, world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
                return await asyncio.get_event_loop().run_in_executor(
                    server.thread_executor, cls.fetch_chunk, world_path, chunk_x, chunk_z
                )

        server.chunkio = ChunkIO
        Buffer.pack_varint = buffer.packVarint
        Buffer.pack_chunk_section_blocks = buffer.packChunkSectionBlocks


async def teardown(server) -> None:
    server.chunkio = DefaultChunkIO
