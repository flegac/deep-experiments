class CloudCluster(object):
    def __init__(self,
                 name: str,
                 cluster_size: int
                 ):
        self.name = name
        self.cluster_size = cluster_size

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()
