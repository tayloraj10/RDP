# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 17:17:59 2017

@author: user
"""
from shapely.geometry import Point, LineString
from matplotlib import pyplot as plt
import fiona


def accept_geometry(path, feature_number):
    '''extracts a list of the coordinates for a specific feature within a spatial file

    Arguments:
    path - path of spatial file
    feature_number - the number of the feature you wish to extract
    '''
    poly_store = []
    with fiona.open(path, 'r') as features:
        for feature in features:
            poly_store.append(feature)

    extract_poly = poly_store[feature_number - 1]['geometry']['coordinates'][0]

    return extract_poly


def show_line(line):
    '''plots a list of points making a line or polygon

    Arguments:
    line - the list of points to be plotted
    '''
    ls = LineString(line)
    x, y = ls.xy
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, color='#6699cc', alpha=0.5,
            linewidth=3, solid_capstyle='round', zorder=2)
    fig.show()


def rdp(point_list, epsilon=1):
    '''python implementation of the Ramon-Douglas-Peucker Algorithm

    Arguments:
    point_list - list of points to run algorithm on
    epsilon - distance cutoff for the rdp algorithm, default is 1
    '''
    if len(point_list) < 3:
        return point_list
    # Find the point with the maximum distance
    dmax = 0
    index = 0
    end = len(point_list)
    for num in range(1, end - 1):
        linestring_list = [(point_list[0]), (point_list[-1])]
        d = Point(point_list[num]).distance(LineString(linestring_list))
        if d > dmax:
            index = num
            dmax = d
    # If max distance is greater than epsilon, recursively simplify
    result_list = []
    if dmax > epsilon:
        # Recursive call
        rec_results1 = rdp(point_list[:index + 1], epsilon)
        rec_results2 = rdp(point_list[index:], epsilon)
        result_list = rec_results1[:-1]+rec_results2
    else:
        result_list = ([point_list[0], point_list[-1]])

    return result_list


def did_change(point_list):
    '''prints whether the rdp algorithm modified a line

    Arguments:
    point_list - list of points to determine whether rdp had an effect
    '''
    if point_list == rdp(point_list):
        print("RDP didn't change the geometry")
    else:
        print("RDP changed the geometry")


def run_full(line, epsilon=1):
    '''plots input line, plots result of running rdp algorithm on input line, and prints whether rdp algorithm modified input line

    Arguments:
    line - list of points to run display and run rdp alogrithm on
    epsilon - distance cutoff for the rdp algorithm, default is 1
    '''
    show_line(line)
    show_line(rdp(line, epsilon))
    did_change(line)


def main():
    shapefile = 'Neighborhoods_Philadelphia/Neighborhoods_Philadelphia.shp'

    test_line = [(3, 0), (4, 2), (5, 2), (5.5, 3), (5, 4), (4, 5), (5, 6),
                 (7, 5), (7, 3), (8, 2.5), (8, 4), (9, 5), (8, 7), (7, 8), (6, 7),
                 (4, 7.75), (3.5, 7.5), (3, 8), (3, 8.5), (2.5, 9), (1, 9), (0, 8),
                 (2, 7), (1, 7), (0, 6), (1, 4), (2, 5), (2, 2), (3, 3), (2, 1)]

    try:
        test_poly = accept_geometry(shapefile, 4)
    except Exception as e:
        print(e)

    '''line tests'''
    # run_full(test_line, 0)
    run_full(test_line, 1)
    # run_full(test_line, 3)
    # run_full(test_line, 5)
    # run_full(test_line, 10)

    '''polygon tests'''
    # run_full(test_poly, 0)
    # run_full(test_poly, 300)
    # run_full(test_poly, 1000)
    # run_full(test_poly, 700)


if __name__ == '__main__':
    main()
