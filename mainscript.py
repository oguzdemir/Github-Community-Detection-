import igraph
import cairocffi as cairo
import csv


class Vertex:
    def __init__(self,name,languages):
        self.name = name
        self.languages = languages


def purify():
    people = {}
    to_be_discarded = set()
    with open('users.csv','rb') as csvfile:
        reader = csv.reader(csvfile)
        v_index = 0
        for row in reader:
            proc_person = row[0].strip()
            people[proc_person] = set()

            followers = row[2][1:-1].split(",")
            for person in followers:
                if person not in people:
                    people[person] = set()
                people[person].add(proc_person)
                people[proc_person].add(person)

            following = row[3][1:len(row[1]) - 1].split(",")
            for person in following:
                if person not in people:
                    people[person] = set()
                people[person].add(proc_person)
                people[proc_person].add(person)

    for person in people:
        if len(people[person]) <= 1:
            to_be_discarded.add(person)

    return to_be_discarded


# adding a edge to the map.
# vertices are concatenated with alphabetical order and "|" char.
def addToMap(map, key1, key2, value):
    if key1< key2:
        key = key1 + '|' + key2
    else:
        key = key2 + '|' + key1
    if key in map:
        map[key] = map[key] + value
    else:
        map[key] = value


def main():
    discard = purify()
    vertexMap = {}
    g = igraph.Graph()
    edgeMap = {}
    with open('users.csv','rb') as csvfile:
        reader = csv.reader(csvfile)
        v_index = 0
        for row in reader:
            processingPerson = row[0].strip()
            if processingPerson in discard:
                continue

            languageSet = []
            languages = row[4][1:-1].split(",")
            for lang in languages:
                languageSet.append(lang)

            v = Vertex(processingPerson, languageSet)
            g.add_vertex(v)
            g.vs["name"][v_index] = processingPerson

            vertexMap[processingPerson] = v_index
            v_index += 1

            followers = row[2][1:-1].split(",")
            for person in followers:
                if person not in discard:
                    addToMap(edgeMap,processingPerson,person, 0.3)

            following = row[3][1:len(row[1]) - 1].split(",")
            for person in following:
                if person not in discard:
                    addToMap(edgeMap, processingPerson, person, 0.1)


    count = 0
    for key,value in edgeMap.iteritems():
        print count
        count += 1
        vertices = key.split("|")
        v1 = vertexMap.get(vertices[0])
        v2 = vertexMap.get(vertices[1])
        g.add_edge(v1,v2,weight = value)

    a = g.community_leading_eigenvector(weights='weight')


    print 'x';


if __name__ == "__main__":
    main()