import os


def parseConfig(name):
    configData = dict()
    for line in open(name).readlines():
        if '=' in line:
            parsed = line.split('=')
            configData[parsed[0].strip()] = parsed[1].strip()
    return configData


def parseData(name):
    parsedData = dict([(i, []) for i in range(6)])
    first = True
    for line in open(name).readlines():
        if first:
            first = False
            continue
        sensors = dict([(i * 3 + 2, i) for i in range(6)])
        for i, item in enumerate(line.strip().split(';')):
            if i in sensors.keys():
                parsedData[sensors[i]].append(int(item))
    return parsedData


def findInputTime(sensorData, timeResizer):
    delta = 300
    percent = 3
    percentResizer = 100
    for i in range(len(sensorData)):
        if i + delta < len(sensorData) and abs(
                sensorData[i + delta] - sensorData[i]) > sensorData[i] * percent // percentResizer:
            return (2 * i + delta) * timeResizer // 2


def produceExperimentConfig(dir):
    for address, dirs, files in os.walk(dir):
        configData = parseConfig(address + os.sep + "board.config")
        periodMus = 40
        toMuMultiplier = 1_000_000
        if configData['fastMode'] == 'true':
            periodMus = 1
        period = periodMus * int(configData['periodTicks']) * int(configData['measurePeriodMultiplier'])

        parsedData = parseData(address + os.sep + "data.csv")

        inputTimes = [findInputTime(sensor, period) for sensor in parsedData.values() if sensor[0] != 0]

        inputTime = sum(inputTimes) / len(inputTimes) / toMuMultiplier

        experimentPath = address + os.sep + "experiment.config"
        if (os.path.isfile(experimentPath)):
            newFileContents = []
            for line in open(experimentPath, encoding='utf8'):
                if 'inputTime' not in line:
                    newFileContents.append(line)
                else:
                    parsed = line.strip().split(' = ')
                    parsed[1] = str(inputTime) + '\n'
                    newFileContents.append(' = '.join(parsed))
            open(experimentPath, 'w').write("".join(newFileContents))
        else:
            open(experimentPath, 'w').write("inputTime = " + str(inputTime))
        break


produceExperimentConfig(input().replace('\\', '/'))
