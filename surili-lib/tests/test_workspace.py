from surili_core.workspace import Workspace


def test_workspace_basic():
    ws = Workspace.from_path('.') / 'generated/workspace' / 'coucou.tiz'
    print(ws.root)


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


def test_store():
    ws = Workspace.from_path(
        path='generated/workspace',
        storage_path='gs://deep-experiments'
    )
    ws.create_file('toto.json')
    ws.create_file('toto2.json')

    ws.to_storage('tests')
    ws.delete()

    ws.from_storage('tests')
    ws.delete()
