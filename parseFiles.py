from SGFSerializer import SGFSerializer

sgf = SGFSerializer("/home/david/goData", "/home/david/csvValueData", 9, True)

sgf.convertFiles(1000000)
