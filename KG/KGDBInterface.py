# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 11:34:47 2019

@author: 16413
"""
import os

from py2neo import Graph, Node, Relationship, walk
import jieba
import time


def load_data(filename='data.txt', amount=500):
    count = 0
    lines_dict = []
    name = ''
    with open(filename, encoding='utf-8') as f:
        while count < amount:
            line = f.readline()
            if not line:
                break
            else:
                line = line.split('	')
                if len(line) != 3:
                    pass
                else:
                    if line[0] == name:
                        attr_name = line[1]
                        attr_value = line[2]
                        lines_dict[count - 1][attr_name] = attr_value
                    else:
                        count += 1
                        name = line[0]
                        attr_name = line[1]
                        attr_value = line[2]
                        line_dict = {'name': name, attr_name: attr_value}
                        lines_dict.append(line_dict)
    f.close()
    return lines_dict


def create_nodes(lines_dict, gi, node_type='常识数据库'):
    for line_dict in lines_dict:
        node = Node(node_type, name='')
        for key in line_dict:
            if key == 'name':
                node['name'] = line_dict[key]
            else:
                node[key] = line_dict[key]
        gi.create(node)


def find_relationships(gi, match_result=None, node_type='常识数据库'):
    if match_result is None:
        match_result = gi.nodes.match(node_type)
    else:
        pass
    namelist = []
    relationships = []
    length = len(match_result)
    # make namelist for all nodes matched
    for i in range(0, length):
        namelist.append(match_result.skip(i).first()['name'])
    # match all properties of nodes with names of other nodes
    for i in range(0, length):
        node_temp = dict(match_result.skip(i).first())
        values = node_temp.values()
        temp_rel = []
        for value in values:
            value = value.replace('\n', '')
            for each in namelist:
                if each in value:
                    temp_rel.append(each)
                else:
                    pass
        relationships.append(temp_rel)
    # remove relationships between nodes and themselves

    for i in range(0, len(relationships)):
        for j in range(0, len(relationships[i])):
            if match_result.skip(i).first()['name'] in relationships[i]:
                relationships[i].remove(match_result.skip(i).first()['name'])
            else:
                pass
        # remove repetition
        relationships[i] = list(set(relationships[i]))
    return [match_result, relationships]


def create_relationships(gi, relationships, match_result=None):
    if match_result is None:
        match_result = gi.nodes.match(type)
    else:
        pass
    for i in range(0, len(relationships)):
        node_this = match_result.skip(i).first()
        for rel in relationships[i]:
            node_that = match_result.where(name=rel).first()
            rel_instance = Relationship(node_this, "REL", node_that)
            gi.create(rel_instance)
    return match_result


def search(gi, name='Carol', node_type='Tulpa', rel_type='LOVES', from_node=False):
    nodes = gi.nodes.match(node_type).where(name=name)
    node_matched = nodes.first()
    if rel_type is not None and node_matched is not None:
        if from_node:
            relationships = gi.match((node_matched,), r_type=rel_type)
        else:
            relationships = gi.match((None, node_matched), r_type=rel_type)
        relationship_matched = relationships.first()
        return node_matched, relationship_matched
    return node_matched, None


def key_in_dialog(gi, dialog_str=None, node_type='常识数据库', rel_type='REL'):
    if dialog_str is None:
        dialog_str = input('试着说点什么\n')
    seg_list = jieba.lcut(dialog_str, cut_all=True)
    for word in seg_list:
        node_searched, relationship_searched = search(gi, name=word, node_type=node_type, rel_type=rel_type)
        if node_searched is not None:
            break
    return node_searched, relationship_searched


def reply(gi, input_str):
    f_null = open(os.devnull, "w")
    if "?" in input_str or "？" in input_str:
        node, relationship = key_in_dialog(dialog_str=input_str, gi=gi)
        for each in walk(relationship):
            print(each, file=f_null)
            for each_key in each:
                print(each_key + " : " + each[each_key].replace('\n', ''))
            print("############")
    else:
        # seq2seq
        pass


graph_instance = Graph('http://localhost:7474', auth=('neo4j', '20160712'))