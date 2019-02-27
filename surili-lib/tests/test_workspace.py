from surili_core.workspace import Workspace

ws = Workspace.from_path('flo')

ws.save_plot(lambda x: x)('coucou')

x = ws.load()('coucou')

print(x)
