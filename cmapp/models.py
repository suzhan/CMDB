from django.db import models

# Create your models here.

from typing import Dict, Any
from py2neo import Graph, NodeMatcher

# 连接图数据库
graph = Graph("bolt://192.168.0.11:7687", auth=("neo4j", "neo4j"))

matcher = NodeMatcher(graph)


def show(args):

    if args == "software":
        args = "MATCH (n:software) RETURN DISTINCT n.name as name"
    elif args == "branch":
        args = "MATCH (n:branch) RETURN DISTINCT n.name as name"
    elif args == "business_line":
        args = "MATCH (n:business_line) RETURN DISTINCT n.name as name"
    elif args == "master":
        args = "MATCH (n:master) RETURN DISTINCT n.pri_ip as name"
    elif args == "node":
        args = "MATCH (n:node) RETURN DISTINCT n.pri_ip as name"
    elif args == "databases":
        args = "MATCH (n:databases) RETURN n.name as name"
    elif args == "properties":
        args = "MATCH (n:properties) RETURN DISTINCT n.name as name"
    elif args == "databases_mysql":
        args = "MATCH (n:databases:mysql) RETURN n.name as name"
    elif args == "databases_mongodb":
        args = "MATCH (n:databases:mongodb) RETURN n.name as name"

    results = graph.run(args).data()

    lists = list()
    for result in results:
        lists.append(result['name'])

    seq = ('id', 'label', 'value')

    result_list = list()
    for i in lists:
        result_list.append(dict.fromkeys(seq, i))

    return result_list




def show_labels(args):

    b = args
    if args == "person_type":
        args = "MATCH (n:person)  RETURN DISTINCT labels(n) as person_type"
    elif args == "software_type":
        args = "MATCH (n:software)  RETURN DISTINCT labels(n) as software_type"
    elif args == "node_type":
        args = "MATCH (n:node)  RETURN DISTINCT labels(n) as node_type"
    elif args == "databases_type":
        args = "MATCH (n:databases)  RETURN DISTINCT labels(n) as databases_type"

    type_result = graph.run(args).data()

    type_list = list()
    for mytype in type_result:
        print(mytype)
        type_list.append(mytype[b])

    blist = list()
    for i in type_list:
        blist.append(i[1])

    seq = ('id', 'label', 'value')

    result_list = list()
    for i in blist:
        result_list.append(dict.fromkeys(seq, i))

    return result_list


