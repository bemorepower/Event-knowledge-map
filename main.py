# -*- coding: utf-8 -*-
from pyhanlp import *
from neo4jrestclient.client import GraphDatabase

###读取数据###
with open("data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()


##构造db##
db = GraphDatabase("http://localhost:7474",
                   username="neo4j",
                   password ="1998"
                   )

wordLabel = db.labels.create("词")

##遍历句子##
for line in lines:

    parseSentence = HanLP.parseDependency(line)

    print(parseSentence)

    ##构建字典保存语意实体
    nodeDict = {}
    relationList = []
    postagList = []

    for row in parseSentence:
        if row.CPOSTAG not in postagList:
            postagList.append(row.CPOSTAG)

        nodeDict[row.ID] = [row.LEMMA.strip(), row.CPOSTAG]
        relationList.append([row.HEAD.ID, row.ID, row.DEPREL])

    ##构建实体
    wordNodeDict = {}
    for wordNode in nodeDict:
        node = db.nodes.create(id=wordNode, word=nodeDict[wordNode][0], tag=nodeDict[wordNode][1])
        wordLabel.add(node)
        wordNodeDict[wordNode] = node

    ##构建关系
    for relation in relationList:
        try:
            sourceNode = wordNodeDict[relation[0]]
            targetNode = wordNodeDict[relation[1]]
            sourceNode.relationships.create(relation[2], targetNode)
        except Exception as e:
            pass



