from hyper_search.train_parameters import TrainParameters

params = TrainParameters.from_yaml('./resources/params.yaml')

print(params)

params.to_yaml('./resources/copy.yaml')
