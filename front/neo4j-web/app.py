# coding=utf-8
from flask import Flask, jsonify, render_template
from neo4j import GraphDatabase
from flask import request
from py2neo import Graph,Node,Relationship

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","neo4j")) #认证连接数据库

app = Flask(__name__) #flask框架必备
graph = Graph()


def buildNodes(nodeRecord):
    data = {"id": str(nodeRecord.n._id), "label": next(iter(nodeRecord.n.labels))}
    data.update(nodeRecord.n.properties)

    return {"data": data}

def buildEdges(relationRecord):
    data = {"source": str(relationRecord.r.start_node.properties['id']),
            "target": str(relationRecord.r.end_node.properties['id']),
            "relationship": relationRecord.r.rel.type}

    return {"data": data}


@app.route('/')#建立路由，指向网页
def index():
    return render_template('search.html')


@app.route('/searchGraph')
def searchGraph():
    node = request.args.get('wd')
    print(node)
    with open("node.txt", "w") as f:
        f.write(node)
    return render_template('index.html', node=node)

#Laurence
@app.route('/graph')#两个路由指向同一个网页，返回图的节点和边的结构体
def get_graph():
    # nodes = list(map(buildNodes, graph.run('MATCH (n) RETURN n').data()))
    #
    # edges = list(map(buildEdges, graph.run('MATCH ()-[r]->() RETURN r').data()))
    # # elements = {"nodes": nodes, "edges": edges}

    with open("node.txt", "r", encoding='utf-8') as f:
        line = f.readlines()
    line = line[0].strip()
    print("1.{}".format(line))
    #
    # with driver.session() as session:
    #     # strAll = 'MATCH (p1{name:"Laurence Fishburne"})-[r1:ACTED_IN]->(m)<-[r2:DIRECTED]-(p2)  RETURN p1,m,p2,r1,r2'
    #     #
    #     # print(strAll)
    #     # results=session.run(strAll).values()
    #     # nodeList=[]
    #     # edgeList=[]
    #     # for result in results:
    #     #     nodeList.append(result[0])
    #     #     nodeList.append(result[1])
    #     #     nodeList.append(result[2])
    #     #     nodeList=list(set(nodeList))
    #     #     edgeList.append(result[3])
    #     #     edgeList.append(result[4])
    #     #
    #     # nodes = list(map(buildNodes, nodeList))
    #     # edges = list(map(buildEdges,edgeList))
    #
    #     strNode = "MATCH (n{name: 'Laurence Fishburne'})-[r]-(p) RETURN n,p,r LIMIT 25"
    #     # strNode = "MATCH (n:Movie{title: '" + line + "'})-[r]-(p) RETURN n,p LIMIT 25"
    #     print(strNode)
    #     # nodes = list(map(buildNodes,graph.run(strNode).data()))
    #
    #     nodes = []
    #     for node in graph.run(strNode).data():
    #         nodeResult = buildNodes(node)
    #         nodes.append(nodeResult)
    #
    #     strEdge = "MATCH (n{name: 'Laurence Fishburne'})-[r]-(p) RETURN r LIMIT 25"
    #     # strEdge = "MATCH (n:Movie{title: '" + line + "'})-[r]-(p) RETURN r LIMIT 25"
    #     print(strEdge)
    #
    #     # edges= list(map(buildEdges,graph.run(strEdge).data()))
    #     edges = []
    #     for edge in graph.run(strEdge).data():
    #         edgeResult = buildEdges(edge)
    #         edges.append(edgeResult)

    nodes = list(map(buildNodes, graph.cypher.execute('MATCH (n) RETURN n')))
    edges = list(map(buildEdges, graph.cypher.execute('MATCH ()-[r]->() RETURN r')))

    return jsonify(elements = {"nodes": nodes, "edges": edges})

if __name__ == '__main__':
    app.run(debug = True) #flask框架必备