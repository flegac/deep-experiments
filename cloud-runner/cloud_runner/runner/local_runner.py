from cloud_runner.runner.project_runner import ProjectRunner


class LocalRunner(ProjectRunner):
    def __init__(self, script_path: str, params: dict):
        self.script_path = script_path
        self.params = params

    def run(self):
        with open(self.script_path) as _:
            script = _.read()
        print('running {}'.format(self.params))
        exec(script, {'params': _})
