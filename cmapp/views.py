from django.http import JsonResponse
from django.shortcuts import HttpResponse
from cmapp.models import *
import json
from py2neo import Graph, NodeMatcher, Node, Relationship
import itertools
import requests

# 连接图数据库
graph = Graph("bolt://192.168.0.11:7687", auth=("neo4j", "neo4j"))
matcher = NodeMatcher(graph)


def node(request):

    response = {}

    if request.method == 'POST':

        branch_select = json.loads(request.body.decode()).get('branch_select')
        software_type_select = json.loads(request.body.decode()).get('software_type_select')
        node_search = json.loads(request.body.decode()).get('node_search')

        if node_search is not None:
            # print(node_search)

            # 查询此ip的相关信息
            node_query = "MATCH (n:node) WHERE n.pri_ip='" + node_search + "'  " \
                          "RETURN  " \
                          "n.name as name, " \
                          "n.pri_ip as pri_ip, " \
                          "n.cpu as cpu, " \
                          "n.mem as mem, " \
                          "n.device_sys as device_sys, " \
                          "n.device_sys_size as device_sys_size, " \
                          "n.device_data as device_data, " \
                          "n.device_data_size as device_data_size, " \
                          "n.os as os, " \
                          "n.status as status "

            node_result = graph.run(node_query).data()

            # 查询此IP属于主机类别
            node_type_query = "match (n:node) where n.pri_ip='" + node_search + "'  return labels(n) as node_type"
            node_type_result = graph.run(node_type_query).data()

            print(node_type_result)

            node_type = list()
            for i in node_type_result:
                node_type.append(i['node_type'])

            node_type_list = list(itertools.chain.from_iterable(node_type))
            node_type_list.remove("node")

            # 查询此ip属于哪主机
            master_query = "match(n:node{pri_ip:'" + node_search + "'})-[:Belong_TO]->(p:master) return p.pri_ip as name"
            master_result = graph.run(master_query).data()

            master_list = list()
            for i in master_result:
                master_list.append(i['name'])

            # 查询此ip属于哪分支
            branch_query = "match (n:node{pri_ip:'" + node_search + "'})-[:Belong_TO]->(p:branch) return p.name as name"
            branch_result = graph.run(branch_query).data()

            branch_list = list()
            for i in branch_result:
                branch_list.append(i['name'])

            # 查询此ip属于哪业务线
            business_line_query = "match (n:node{pri_ip:'" + node_search + "'})-[:Belong_TO]->(p:business_line) " \
                                  " return p.name as name"
            business_line_result = graph.run(business_line_query).data()

            business_line_list = list()
            for i in business_line_result:
                business_line_list.append(i['name'])

            # 返回结果
            response['node_search'] = node_result

            response['master_result'] = master_list
            response['branch_result'] = branch_list
            response['business_line_result'] = business_line_list
            response['node_type_result'] = node_type_list

        elif branch_select is not None and software_type_select is not None and node_search is None:
            # 返回首页查询
            # print(branch_select)
            # print(software_type_select)
            # print(node_search)

            query = "MATCH (branch{name:'" + branch_select + "'})<-[:Belong_TO]-(n:node)<-[:Perform_ON]-(software:" + software_type_select + ") " \
                    "RETURN DISTINCT " \
                    "n.name as name, " \
                    "n.pri_ip as pri_ip, " \
                    "n.cpu as cpu, n.mem as mem, " \
                    "n.device_sys as device_sys, " \
                    "n.device_sys_size as device_sys_size," \
                    "n.device_data as device_data, " \
                    "n.device_data_size as device_data_size, " \
                    "n.os as os, n.status as status "

            print(query)

            result = graph.run(query).data()
            response['node'] = result

        elif branch_select is None and software_type_select is None and node_search is None:
            # 提交新数据
            nodeForm = json.loads(request.body.decode()).get('nodeForm')
            # print(nodeForm)

            # 重复检查
            pri_id_check = len(graph.nodes.match("node", pri_ip=str(nodeForm['nodeForm_pri_ip'])))

            if pri_id_check == 1:
                # 如果有返回值就弹出窗口返回错误信息
                response['resultMsg'] = ['错误: pri_id 已经存在, 请重新输入!']
                response['resultCode'] = ['error']

            else:
                new_node = Node('node', str(nodeForm['nodeForm_node_type']),
                                name=str(nodeForm['nodeForm_name']),
                                pri_ip=str(nodeForm['nodeForm_pri_ip']),
                                cpu=str(nodeForm['nodeForm_cpu']),
                                mem=str(nodeForm['nodeForm_mem']),
                                device_sys=str(nodeForm['nodeForm_device_sys']),
                                device_sys_size=str(nodeForm['nodeForm_device_sys_size']),
                                device_data=str(nodeForm['nodeForm_device_data']),
                                device_data_size=str(nodeForm['nodeForm_device_data_size']),
                                os=str(nodeForm['nodeForm_os']),
                                status=str(nodeForm['nodeForm_status']))

                master = graph.nodes.match("master", name=str(nodeForm['nodeForm_master'][0])).first()
                branch = graph.nodes.match("branch", name=str(nodeForm['nodeForm_branch'][0])).first()
                business_line = graph.nodes.match("business_line", name=str(nodeForm['nodeForm_business_line'][0])).first()

                print(master)
                print(branch)
                print(business_line)

                r1 = Relationship(new_node, "Belong_TO", master)
                r2 = Relationship(new_node, "Belong_TO", branch)
                r3 = Relationship(new_node, "Belong_TO", business_line)

                try:
                    graph.create(new_node)
                    graph.create(r1)
                    graph.create(r2)
                    graph.create(r3)
                except BaseException as err:
                    err = "'错误:" + str(err) + "'"
                    response['resultMsg'] = [err]
                    response['resultCode'] = ['error']
                else:
                    response['resultMsg'] = ['成功写入!']
                    response['resultCode'] = ['success']
        return JsonResponse(response, safe=False)

    else:
        response['branch_options'] = show("branch")
        response['software_type_options'] = show_labels("software_type")
        response['master_options'] = show("master")
        response['business_line_options'] = show("business_line")
        response['node_type_options'] = show_labels("node_type")
        response['node_options'] = show("node")

        return JsonResponse(response, safe=False)


def software(request):
    response = {}
    if request.method == 'POST':
        branch_select = json.loads(request.body.decode()).get('branch_select')
        software_type_select = json.loads(request.body.decode()).get('software_type_select')
        software_search = json.loads(request.body.decode()).get('software_search')

        if software_search is not None:
            # 基本信息
            software_search_query = "MATCH (n:software) where n.name='" + str(software_search) +"' " \
                                    "RETURN  " \
                                    "n.name as name, " \
                                    "n.version as version, " \
                                    "n.port1 as port1, " \
                                    "n.port2 as port2, " \
                                    "n.git_path as git_path"

            software_search_query_result = graph.run(software_search_query).data()

            # 所属软件类别
            software_type_query = "MATCH (n:software) where " \
                                  "n.name='" + str(software_search) + "' RETURN labels(n) as software_type"
            software_type_query_result = graph.run(software_type_query).data()
            # print(software_type_query_result)
            software_type = list()
            for i in software_type_query_result:
                software_type.append(i['software_type'])

            software_type_list = list(itertools.chain.from_iterable(software_type))
            software_type_list.remove("software")  # 只取出类别
            # print(software_type_list)

            # 所属分支
            software_branch_query = "MATCH (n:software)-[r:Belong_TO]->(p:branch) WHERE " \
                                    "n.name='" + str(software_search) + "' RETURN p.name as name"
            # print(software_branch_query)
            software_branch_query_result = graph.run(software_branch_query).data()
            branch_list = list()
            for i in software_branch_query_result:
                branch_list.append(i['name'])

            # 部署的节点
            software_node_query = "MATCH (n:software)-[r:Perform_ON]->(p:node) WHERE " \
                                  "n.name='" + str(software_search) + "' RETURN DISTINCT p.pri_ip as name"
            # print(software_node_query)
            software_node_query_result = graph.run(software_node_query).data()
            node_list = list()
            for i in software_node_query_result:
                node_list.append(i['name'])

            # 依赖软件
            software_software_query = "MATCH (n:software)-[r:Depend_ON]->(p:software) WHERE " \
                                      "n.name='" + str(software_search) + "' RETURN DISTINCT p.name as name"
            # print(software_software_query)
            software_software_query_result = graph.run(software_software_query).data()
            software_list = list()
            for i in software_software_query_result:
                software_list.append(i['name'])

            # 依赖数据库
            software_databases_query = "MATCH (n:software)-[r:Depend_ON]->(p:databases) WHERE " \
                                       "n.name='" + str(software_search) + "' RETURN DISTINCT p.name as name"
            # print(software_databases_query)
            software_databases_query_result = graph.run(software_databases_query).data()
            databases_list = list()
            for i in software_databases_query_result:
                databases_list.append(i['name'])

            # 依赖的配置文件
            software_properties_query = "MATCH (n:software)-[r:Depend_ON]->(p:properties) WHERE " \
                                        "n.name='" + str(software_search) + "' RETURN DISTINCT p.name as name"

            software_properties_query_result = graph.run(software_properties_query).data()
            properties_list = list()
            for i in software_properties_query_result:
                properties_list.append(i['name'])

            response['software_search'] = software_search_query_result
            response['software_type'] = software_type_list
            response['software_branch'] = branch_list
            response['software_node'] = node_list
            response['software_software'] = software_list
            response['software_databases'] = databases_list
            response['software_properties'] = properties_list

            return JsonResponse(response, safe=False)

        elif software_search is None and branch_select is not None and software_type_select is not None:
            # 概览页查询
            query = "MATCH (n:software:" + software_type_select + ")-[r:Belong_TO]->(branch{name:'" + branch_select + "'}) \
                                        RETURN " \
                                        "n.name as name, " \
                                        "n.version as version, " \
                                        "n.port1 as port1, " \
                                        "n.port2 as port2, " \
                                        "n.git_path as git_path"

            result = graph.run(query).data()
            response['software'] = result

            return JsonResponse(response, safe=False)

        elif software_search is None and branch_select is None and software_type_select is None:
            softwareform = json.loads(request.body.decode()).get('softwareForm')
            name_check = "MATCH (n:software) WHERE n.name='" + str(softwareform['softwareForm_name']) + "' RETURN n"
            name_check_result = len(graph.run(name_check).data())

            print(name_check_result)

            if name_check_result == 0:
                new_software = Node('software', str(softwareform['softwareForm_software_type']),
                                    name=str(softwareform['softwareForm_name']),
                                    version=str(softwareform['softwareForm_version']),
                                    port1=str(softwareform['softwareForm_port1']),
                                    port2=str(softwareform['softwareForm_port2']),
                                    git_path=str(softwareform['softwareForm_git_path']))

                try:
                    graph.create(new_software)

                    # 部署到的分支
                    for branch_name in softwareform['softwareForm_branch']:
                        graph.create(Relationship(new_software, "Belong_TO",
                                                  graph.nodes.match("branch", name=branch_name).first()))

                    # 部署的节点
                    for node_name in softwareform['softwareForm_node']:
                        graph.create(Relationship(new_software, "Perform_ON",
                                                  graph.nodes.match("node", name=node_name).first()))

                    # 依赖数据库
                    for databases_name in softwareform['softwareForm_databases']:
                        graph.create(Relationship(new_software, "Depend_ON", graph.nodes.match("databases",
                                                                    name=databases_name).first()))

                    # 依赖软件
                    for software_name in softwareform['softwareForm_software']:
                        graph.create(Relationship(new_software, "Depend_ON",
                                                  graph.nodes.match("software", name=software_name).first()))

                    # 依赖配置文件
                    for properties_name in softwareform['softwareForm_properties']:
                        graph.create(Relationship(new_software, "Depend_ON",
                                                  graph.nodes.match("properties", name=properties_name).first()))

                except BaseException as err:
                    err = "'错误:" + str(err) + "'"
                    response['resultMsg'] = [err]
                    response['resultCode'] = ['error']
                else:
                    response['resultMsg'] = ['成功写入!']
                    response['resultCode'] = ['success']

                return JsonResponse(response, safe=False)
            else:
                response['resultMsg'] = ['此软件已存在!']
                response['resultCode'] = ['error']

            return JsonResponse(response, safe=False)

    else:
        # get 返回
        response['branch_options'] = show("branch")
        response['software_type_options'] = show_labels("software_type")
        response['node_options'] = show("node")
        response['software_options'] = show("software")
        # response['databases_options'] = show("databases")
        response['properties_options'] = show("properties")
        response['databases_mysql_options'] = show("databases_mysql")
        response['databases_mongodb_options'] = show("databases_mongodb")
        response['databases_type_options'] = show_labels("databases_type")

        return JsonResponse(response, safe=False)


def add_software_type(request):
    response = {}

    if request.method == 'POST':
        new_software_type_name = json.loads(request.body.decode()).get('single_input_text')
        print(new_software_type_name)
        new_software_type_check = "MATCH(n:software:" + str(new_software_type_name) + ") RETURN labels(n)"
        print(new_software_type_check)

        new_software_type_check_result = len(graph.run(new_software_type_check).data())

        if new_software_type_check_result == 0:

            new_software_type = Node('software', str(new_software_type_name), name=str(new_software_type_name))

            try:
                graph.create(new_software_type)
            except BaseException as err:
                err = "'错误:" + str(err) + "'"
                response['resultMsg'] = [err]
                response['resultCode'] = ['error']
            else:
                response['resultMsg'] = ['成功写入!']
                response['resultCode'] = ['success']

            return JsonResponse(response, safe=False)
        else:
            response['resultMsg'] = ['类别已存在!']
            response['resultCode'] = ['error']

            return JsonResponse(response, safe=False)


def add_new_database(request):
    response = {}
    if request.method == 'POST':
        form = json.loads(request.body.decode()).get('form')

        name_check = "MATCH (n:databases:" + form['form_databases_type'] + ") " \
                     "WHERE n.name='" + str(form['form_name']) + "' RETURN n"
        name_check_result = len(graph.run(name_check).data())

        if name_check_result == 0:

            database_add = Node('databases', str(form['form_databases_type']),
                                name=str(form['form_name']), user=str(form['form_user']))

            try:
                graph.create(database_add)
            except BaseException as err:
                err = "'错误:" + str(err) + "'"
                response['resultMsg'] = [err]
                response['resultCode'] = ['error']
            else:
                response['resultMsg'] = ['成功写入!']
                response['resultCode'] = ['success']

            return JsonResponse(response, safe=False)
        else:
            response['resultMsg'] = ['类别已存在!']
            response['resultCode'] = ['error']

            return JsonResponse(response, safe=False)


def add_new_properties(request):
    response = {}

    if request.method == 'POST':
        form = json.loads(request.body.decode()).get('form')

        name_check = "MATCH (n:properties) WHERE n.name='" + str(form['form_name']) + "' RETURN n"
        name_check_result = len(graph.run(name_check).data())

        if name_check_result == 0:

            properties_add = Node('properties',
                                  name=str(form['form_name']),
                                  branch=str(form['form_branch']),
                                  version=str(form['form_version']),
                                  path=str(form['form_path']))

            try:
                graph.create(properties_add)

            except BaseException as err:
                err = "'错误:" + str(err) + "'"
                response['resultMsg'] = [err]
                response['resultCode'] = ['error']
            else:
                response['resultMsg'] = ['成功写入!']
                response['resultCode'] = ['success']

            return JsonResponse(response, safe=False)
        else:
            response['resultMsg'] = ['配置文件已存在!']
            response['resultCode'] = ['error']

            return JsonResponse(response, safe=False)


def add_node_type(request):
    response = {}

    if request.method == 'POST':
        new_node_type_name = json.loads(request.body.decode()).get('single_input_text')
        new_node_type_check = "MATCH(n:node:" + str(new_node_type_name) + ") RETURN labels(n)"
        new_node_type_check_result = len(graph.run(new_node_type_check).data())

        if new_node_type_check_result == 0:

            new_node_type = Node('node', str(new_node_type_name), pri_ip=str(new_node_type_name))

            try:
                graph.create(new_node_type)
                # graph.run(new_node_type_add)
            except BaseException as err:
                err = "'错误:" + str(err) + "'"
                response['resultMsg'] = [err]
                response['resultCode'] = ['error']
            else:
                response['resultMsg'] = ['成功写入!']
                response['resultCode'] = ['success']

            return JsonResponse(response, safe=False)
        else:
            response['resultMsg'] = ['类别已存在!']
            response['resultCode'] = ['error']

            return JsonResponse(response, safe=False)


def add_new_branch(request):

    response = {}
    if request.method == 'POST':
        new_branch_name = json.loads(request.body.decode()).get('single_input_text')
        print(new_branch_name)

        new_branch_name_check = "match (n:branch) where n.name='" + str(new_branch_name) + "' return n"
        new_branch_name_check_result = len(graph.run(new_branch_name_check).data())

        if new_branch_name_check_result == 0:
            new_branch_name_add = Node('branch', name=str(new_branch_name))

            try:
                graph.create(new_branch_name_add)
            except BaseException as err:
                err = "'错误:" + str(err) + "'"
                response['resultMsg'] = [err]
                response['resultCode'] = ['error']
            else:
                response['resultMsg'] = ['成功写入!']
                response['resultCode'] = ['success']

            return JsonResponse(response, safe=False)

        else:
            response['resultMsg'] = ['分支名称已存在!']
            response['resultCode'] = ['error']

            return JsonResponse(response, safe=False)


def add_new_business_line(request):

    response = {}
    if request.method == 'POST':
        new_business_line_name = json.loads(request.body.decode()).get('single_input_text')
        print(new_business_line_name)

        new_business_line_name_check = "match (n:business_line) where n.name='" + str(new_business_line_name) + "' return n"
        new_business_line_name_check_result = len(graph.run(new_business_line_name_check).data())

        if new_business_line_name_check_result == 0:
            new_business_line_name_add = Node('business_line', name=str(new_business_line_name))

            try:
                graph.create(new_business_line_name_add)
            except BaseException as err:
                err = "'错误:" + str(err) + "'"
                response['resultMsg'] = [err]
                response['resultCode'] = ['error']
            else:
                response['resultMsg'] = ['成功写入!']
                response['resultCode'] = ['success']

            return JsonResponse(response, safe=False)

        else:
            response['resultMsg'] = ['业务线名称已存在!']
            response['resultCode'] = ['error']

            return JsonResponse(response, safe=False)


def add_cloud_master(request):

    response = {}
    if request.method == 'POST':
        cloud_account_name = json.loads(request.body.decode()).get('cloud_account_name')
        print(cloud_account_name)

        cloud_account_name_check = "match (n:master:cloud) where n.name='" + str(cloud_account_name) + "' return n"
        cloud_account_name_check_result = len(graph.run(cloud_account_name_check).data())

        if cloud_account_name_check_result == 0:
            cloud_account_name_add = Node('master', 'cloud', name=str(cloud_account_name))
            print(cloud_account_name_add)

            try:
                graph.create(cloud_account_name_add)
            except BaseException as err:
                err = "'错误:" + str(err) + "'"
                response['resultMsg'] = [err]
                response['resultCode'] = ['error']
            else:
                response['resultMsg'] = ['成功写入!']
                response['resultCode'] = ['success']

            return JsonResponse(response, safe=False)

        else:
            response['resultMsg'] = ['阿里云或云端帐号名称已存在!']
            response['resultCode'] = ['error']

            return JsonResponse(response, safe=False)


def add_local_master(request):

    response = {}
    if request.method == 'POST':
        localForm = json.loads(request.body.decode()).get('localForm')
        print(localForm)

        # 重复检查
        pri_id_check = len(graph.nodes.match("master", "local", pri_ip=str(localForm['localForm_pri_ip'])))


        if pri_id_check == 1:
            # 如果有返回值就弹出窗口返回错误信息
            response['resultMsg'] = ['错误: pri_id 已经存在, 请重新输入!']
            response['resultCode'] = ['error']

        else:
            new_master = Node("master", "local",
                            name=str(localForm['localForm_name']),
                            pri_ip=str(localForm['localForm_pri_ip']),
                            cpu=str(localForm['localForm_cpu']),
                            mem=str(localForm['localForm_mem']),
                            device_sys=str(localForm['localForm_device_sys']),
                            device_sys_size=str(localForm['localForm_device_sys_size']),
                            device_data=str(localForm['localForm_device_data']),
                            device_data_size=str(localForm['localForm_device_data_size']),
                            os=str(localForm['localForm_os']),
                            status=str(localForm['localForm_status']))
            try:
                graph.create(new_master)
            except BaseException as err:
                err = "'错误:" + str(err) + "'"
                response['resultMsg'] = [err]
                response['resultCode'] = ['error']
            else:
                response['resultMsg'] = ['成功写入!']
                response['resultCode'] = ['success']
    return JsonResponse(response, safe=False)


def properties(request):

    response = {}

    if request.method == 'POST':

        branch_select = json.loads(request.body.decode()).get('branch_select')
        software_type_select = json.loads(request.body.decode()).get('software_type_select')
        software_name_select = json.loads(request.body.decode()).get('software_name_select')

        if software_name_select is None:

            software_name_query = "MATCH (n:software:" + str(software_type_select) + ")-[r:Belong_TO]->(branch{name:'" + str(
                branch_select) + "'}) RETURN n.name as name"

            software_name_query_result = graph.run(software_name_query).data()

            lists = list()
            for result in software_name_query_result:
                lists.append(result['name'])

            seq = ('id', 'label', 'value')

            result_list = list()
            for i in lists:
                result_list.append(dict.fromkeys(seq, i))

            print(result_list)

            response['software_name_options'] = result_list

            return JsonResponse(response, safe=False)

        else:

            if branch_select == 'release':
                branch_select = 'rep2'

            if branch_select == 'pre':
                branch_select = 'pre2'

            new_url = "https://gitlab.mediportal.com.cn/ops/pcm/raw/master/cc/"+ str(software_name_select) +"/"+ str(software_name_select) +"-"+ str(branch_select) +".properties?private_token=MHJ8NBft-wJtpzpzrm6u"
            response = requests.get(new_url)

            # print(response.status_code)

            if response.status_code == requests.codes.ok:
                return HttpResponse(response, content_type="text/plain")
            # else:
            #     response['resultMsg'] = ['错误: 配置文件找不到!']
            #     response['resultCode'] = ['error']
            #
            #     return JsonResponse(response, safe=False)


def person(request):
    response = {}

    if request.method == 'POST':
        person_type_select = json.loads(request.body.decode()).get('person_type_select')
        person_search = json.loads(request.body.decode()).get('person_search')

        if person_search is None and person_type_select is not None:
            # 概览页
            query = "MATCH (n:person:" + str(person_type_select) + ") RETURN" \
                    " n.name as name," \
                    " n.phone as phone," \
                    " n.email as email"
            result = graph.run(query).data()

            response['person'] = result
            return JsonResponse(response, safe=False)

        elif person_search is not None and person_type_select is None:

            person_query = "MATCH (n:person) WHERE n.name='" + str(person_search) + "' " \
                           " RETURN " \
                           " n.name as name," \
                           " n.phone as phone," \
                           " n.email as email"

            person_result = graph.run(person_query).data()

            # 查询所在用户类型
            person_type_query = "MATCH (p:person) WHERE p.name = '" + str(
                person_search) + "' return labels(p) as person_type"
            person_type_query_result = graph.run(person_type_query).data()

            if person_type_query_result is not None:
                person_type = list()
                for i in person_type_query_result:
                    person_type.append(i['person_type'])

                person_type_list = list(itertools.chain.from_iterable(person_type))
                person_type_list.remove("person")


            # 如果查询所属分支
            person_branch_query = "match (n:person)-[:Manage_TO]-(p:branch) where n.name = '" + str(
                person_search) + "' return p.name as name"
            person_branch_result = graph.run(person_branch_query).data()

            if person_branch_result is not None:
                branch_list = list()
                for i in person_branch_result:
                    branch_list.append(i['name'])

            # 查询所开发软件
            person_software_query = "match (n:person)-[:Manage_TO]-(p:software) where n.name = '" + str(
                person_search) + "' return p.name as name"
            person_software_result = graph.run(person_software_query).data()

            if person_software_result is not None:
                software_list = list()
                for i in person_software_result:
                    software_list.append(i['name'])

            # 查询所管理的数据库存
            person_databases_query = "match (n:person)-[:Manage_TO]-(p:databases) where n.name = '" + str(
                person_search) + "' return p.name as name"
            person_databases_result = graph.run(person_databases_query).data()

            if person_databases_result is not None:
                databases_list = list()
                for i in person_databases_result:
                    databases_list.append(i['name'])

            response['person_type_result'] = person_type_list
            response['person_branch_result'] = branch_list
            response['person_software_result'] = software_list
            response['person_databases_result'] = databases_list
            response['person_result'] = person_result

            return JsonResponse(response, safe=False)

        elif person_search is None and person_type_select is None:
            # 数据提交处理
            personForm = json.loads(request.body.decode()).get('personForm')

            # 重复检查
            person_check = len(graph.nodes.match("person", name=str(personForm['personForm_name'])))

            if person_check == 1:

                response['resultMsg'] = ['错误: 此人员已经存在, 请重新输入!']
                response['resultCode'] = ['error']

                return JsonResponse(response, safe=False)

            else:
                new_person = Node('person', str(personForm['personForm_person_type']),
                                  name=str(personForm['personForm_name']),
                                  phone=str(personForm['personForm_phone']),
                                  email=str(personForm['personForm_email']))

                try:
                    graph.create(new_person)

                    # 管理的分支
                    for branch_name in personForm['personForm_branch']:
                        graph.create(Relationship(new_person, "Manage_TO",
                                                  graph.nodes.match("branch", name=branch_name).first()))

                    # 管理或开发的软件
                    for software_name in personForm['personForm_software']:
                        graph.create(Relationship(new_person, "Manage_TO",
                                                  graph.nodes.match("software", name=software_name).first()))

                except BaseException as err:
                    err = "'错误:" + str(err) + "'"
                    response['resultMsg'] = [err]
                    response['resultCode'] = ['error']
                else:
                    response['resultMsg'] = ['成功写入!']
                    response['resultCode'] = ['success']
            return JsonResponse(response, safe=False)

    else:

        response['branch_options'] = show("branch")
        response['software_options'] = show("software")
        response['databases_options'] = show("databases")
        response['person_type_options'] = show_labels("person_type")
        return JsonResponse(response, safe=False)



def add_person_type(request):
    response = {}

    if request.method == 'POST':
        new_person_name = json.loads(request.body.decode()).get('single_input_text')
        print(new_person_name)

        # person_check = "MATCH (n.person) WHERE n.name = '" + str(new_person_name) + "' RETURN n"
        person_check = len(graph.nodes.match("person", name=str(new_person_name)))

        if person_check == 0:

            new_person_type = Node('person', str(new_person_name), name=str(new_person_name))

            try:
                graph.create(new_person_type)
                # graph.run(new_node_type_add)
            except BaseException as err:
                err = "'错误:" + str(err) + "'"
                response['resultMsg'] = [err]
                response['resultCode'] = ['error']
            else:
                response['resultMsg'] = ['成功写入!']
                response['resultCode'] = ['success']

            return JsonResponse(response, safe=False)
        else:
            response['resultMsg'] = ['类别已存在!']
            response['resultCode'] = ['error']

        return JsonResponse(response, safe=False)

        # return JsonResponse(response, safe=False)

