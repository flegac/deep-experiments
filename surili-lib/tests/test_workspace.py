from surili_core.workspace import Workspace

ws = Workspace.from_path('flo')

ws.writer(lambda x: x)('coucou')

x = ws.reader()('coucou')

print(x)
