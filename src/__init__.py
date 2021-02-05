import nimporter

# PyMine imports
from pymine.api.abc import AbstractChunkIO

# KnightsOfNi imports
import nim.chunkio as chunkio

nimporter.build_nim_extensions()


class ChunkIO(AbstractChunkIO):
    calc_offset = staticmethod(chunkio.calc_offset)
    find_chunk = staticmethod(chunkio.find_chunk)


async def setup(server_, config_: dict) -> None:
    global server, config
    server = server_
    config = config_


async def teardown(server) -> None:
    pass
