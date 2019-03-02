from mydeep_lib.visualize.show_dataset import ShowDataset


class Visualize:
    @staticmethod
    def show_dataset(label='Dataset', scale=5):
        return ShowDataset(label, scale)

    @staticmethod
    def show_plot(plot):
        plot.plot()

    @staticmethod
    def save_plot(path):
        def apply(plot):
            plot.savefig('{}.pdf'.format(path))
            plot.savefig('{}.png'.format(path))

        return apply
