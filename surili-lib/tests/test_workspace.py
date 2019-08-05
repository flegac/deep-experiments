from surili_core.workspace import Workspace


def test_workspace_basic():
    ws = Workspace.from_path('.') / 'generated/workspace' / 'coucou.tiz'
    print(ws.root)


def test_workspace():
    with Workspace.from_path('generated/workspace') as ws:
        ws.create_file('toto.json', {
            'x': 'data',
            'y': 'coco'
        }, force=True)
        try:
            ws.create_file('toto.json')
        except Exception as e:
            assert isinstance(e, ValueError)

        ws.get_ws('tata')
        ws.get_ws('titi')

        print(ws)
