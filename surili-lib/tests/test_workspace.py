from surili_core.workspace import Workspace


def test_workspace():
    ws = Workspace.from_path('generated/workspace')

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

    ws.delete()

