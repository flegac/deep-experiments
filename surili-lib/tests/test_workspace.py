from surili_core.workspace import Workspace

ws = Workspace.from_path('flo')

ws.save(lambda x: x)('coucou')

x = ws.load()('coucou')

print(x)
