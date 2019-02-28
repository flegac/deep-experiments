install:
	(cd stream-lib && make)
	(cd surili-lib && make)
	(cd hyper-search && make)
	(cd mydeep-lib && make)
	(cd train-common && make)
	(cd kaggle-project && make)

uninstall:
	(cd stream-lib && make uninstall)
	(cd surili-lib && make uninstall)
	(cd hyper-search && make uninstall)
	(cd mydeep-lib && make uninstall)
	(cd train-common && make uninstall)
	(cd kaggle-project && make uninstall)
