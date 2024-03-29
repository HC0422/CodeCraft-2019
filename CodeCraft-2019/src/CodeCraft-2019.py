import logging
import sys

import MatrixBuilding
import DataProcessing
import official

logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    #logging.info("car_path is %s" % (car_path))
    #logging.info("road_path is %s" % (road_path))
    #logging.info("cross_path is %s" % (cross_path))
    #logging.info("answer_path is %s" % (answer_path))
    #n:路口数量, data：CrossLinkCross, CleanCrossRoadId, HashCrossId
    n,data,CleanCrossRoadId, HashCrossId = DataProcessing.readCross(cross_path)
    Matrix = MatrixBuilding.buildGraphFromFile(n,data)
    #OutputAnswer.createAnswer(car_path, CleanCrossRoadId, Matrix, answer_path, road_path)
    #A_car_a_times_end.createAnswer(car_path, CleanCrossRoadId, Matrix, answer_path, road_path)
    #Test_A_time_A_Cars.createAnswer(car_path, CleanCrossRoadId, Matrix, answer_path, road_path)
    official.createAnswer(car_path, CleanCrossRoadId, Matrix, answer_path, road_path, HashCrossId)
    #A_car_a_times_end.createAnswer(car_path, CleanCrossRoadId, Matrix, answer_path, road_path)
    #print(path)
# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()