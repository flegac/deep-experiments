from mydeep_api.monitoring.dataset_viewer import DatasetViewer


class Visualize:
    @staticmethod
    def show_dataset(label='Dataset', scale=5):
        return DatasetViewer(label, scale)

    @staticmethod
    def show_plot(plot):
        plot.plot()

    @staticmethod
    def save_plot(path):
        def apply(plot):
            plot.savefig('{}.pdf'.format(path))
            plot.savefig('{}.png'.format(path))

        return apply
