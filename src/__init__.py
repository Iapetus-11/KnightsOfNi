import nimporter

global server
server = None

async def setup(server, config: dict) -> None:
    global server
    server = server

async def teardown(server):
    pass
