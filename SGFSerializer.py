import sgf

with open("Games/game0.sgf",'r') as f:
    collection = sgf.parse(f.read())
    print(collection.children[0].nodes[0].properties['RE'])
    print(collection.children[0])
with open("Games/collection0.sgf", 'w') as f:
    collection.output(f)
    print('1234')