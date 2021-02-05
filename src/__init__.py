import nimporter

# PyMine imports
# from pymine.api.abc import AbstractChunkIO


# KnightsOfNi imports
import nim.chunkio as chunkio

nimporter.build_nim_extensions()


class ChunkIO:
    calc_offset = staticmethod(chunkio.calc_offset)
    find_chunk = staticmethod(chunkio.find_chunk)

    def fetch_chunk(world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
        chunk_data, timestamp = chunkio.fetch_chunk(world_path, chunk_x, chunk_z)

    async def fetch_chunk_async(world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
        pass


async def setup(server_, config_: dict) -> None:
    global server, config
    server = server_
    config = config_


async def teardown(server) -> None:
    pass
