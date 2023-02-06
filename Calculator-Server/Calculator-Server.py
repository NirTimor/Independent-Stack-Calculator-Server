from flask import Flask, request
from math import factorial
from datetime import datetime
import time
import logging
import os
# Following is the implementation of the server according to the instructions of the exercise
global requestsCounter  # Global counter for the requests
requestsCounter = 0
global LegalPerformance
LegalPerformance = 1
global StackCalculateResultByInt
StackCalculateResultByInt = 0
niroServer = Flask('__name__')  # created the Server
niroStack = []  # Global Stack for relevant operations
t2 = datetime.now()
currentTime = t2.strftime("%d-%m-%Y %H:%M:%S.%f")[:-3]
calculatedArguments = [False, False]
# ENUMS - divided the operations because special ones require one argument only , while the regular require 2
# this way will be better to check
specialOperations = {"abs", "fact"}  # special operations
regularOperations = {"plus", "minus", "times", "divide", "pow"}  # regular operations


def getLoggerLevelByString(level):
    if level == 10:
        return "DEBUG"
    elif level == 20:
        return "INFO"
    elif level == 30:
        return "WARNING"
    elif level == 40:
        return "ERROR"
    elif level == 50:
        return "CRITICAL"
    else:
        return "INVALID LEVEL"


def stackToString(niroStack):
    res = ', '.join(str(x) for x in reversed(niroStack))
    return res


# Description of the actions required from the server
# First is independent calculator which performs the full independent calculation
@niroServer.route("/independent/calculate", methods=["POST"])
def independentCalculate():
    start_time = time.time()
    global requestsCounter
    requestsCounter = requestsCounter + 1
    argumentsCommaSeperated = ""
    independentLogger = logging.getLogger("independent-logger")
    jsonRequest = request.get_json()
    resource = "/independent/calculate"
    verb = "POST"
    operator = jsonRequest['operation']  # get the operation from the json in the given request
    theArguments = jsonRequest['arguments']  # get an array of the arguments in the given request
    numberofArguments = len(theArguments)  # check how many arguments to know if we want to implement the operation
    incaseSensitiveOperator = operator.lower()  # we want it incase sensitive
    errorMessage1 = "Error: Not enough arguments to perform the operation "
    errorMessage2 = "Error: Too many arguments to perform the operation "
    errorMessage3 = "Error while performing operation Divide: division by 0"
    errorMessage4 = "Error: The operation require one argument "
    errorMessage5 = "Error: Too many arguments to perform the operation "
    errorMessage6 = "Error while performing operation Factorial"
    errorMessage7 = "Error: unknown operation."
    for element in theArguments:
        element_str = str(element)
        if argumentsCommaSeperated == "":
            argumentsCommaSeperated = element_str
        else:
            argumentsCommaSeperated += "," + element_str
    requestsLogger = logging.getLogger("request-logger")
    requestsLogger.info(f"Incoming request | #{requestsCounter} | resource: {resource} | HTTP Verb {verb}", extra={'request_number': requestsCounter, 'time': currentTime})
    if incaseSensitiveOperator in regularOperations:  # if we got a ''good'' operation,we want exactly 2 arguments
        if numberofArguments < 2:
            independentLogger.error(f"Server encountered an error ! message: {errorMessage1}", extra={'request_number': requestsCounter, 'time': currentTime})
            return {"error message": "Error: Not enough arguments to perform the operation " + operator}, 409
        elif numberofArguments > 2:
            independentLogger.error(f"Server encountered an error ! message: {errorMessage2}", extra={'request_number': requestsCounter, 'time': currentTime})
            return {"error message": "Error: Too many arguments to perform the operation " + operator}, 409
        else:  # this case is good , can make the operation
            n1 = theArguments[0]  # get first number to operate
            n2 = theArguments[1]  # get second number to operate
            if incaseSensitiveOperator == "plus":
                durationOfRequest = int((time.time() - start_time) * 1000)
                requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
                independentLogger.info(f"Performing operation {operator}. Result is {int(n1 + n2)}", extra={'request_number': requestsCounter, 'time': currentTime})
                independentLogger.debug(f"Performing operation: {operator}({argumentsCommaSeperated}) = {int(n1 + n2)}", extra={'request_number': requestsCounter, 'time': currentTime})
                return {"result": n1 + n2}, 200
            elif incaseSensitiveOperator == "minus":
                durationOfRequest = int((time.time() - start_time) * 1000)
                requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
                independentLogger.info(f"Performing operation {operator}. Result is {int(n1 - n2)}", extra={'request_number': requestsCounter, 'time': currentTime})
                independentLogger.debug(f"Performing operation: {operator}({argumentsCommaSeperated}) = {int(n1 - n2)}", extra={'request_number': requestsCounter, 'time': currentTime})
                return {"result": n1 - n2}, 200
            elif incaseSensitiveOperator == "times":
                durationOfRequest = int((time.time() - start_time) * 1000)
                requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
                independentLogger.info(f"Performing operation {operator}. Result is {int(n1 * n2)}", extra={'request_number': requestsCounter, 'time': currentTime})
                independentLogger.debug(f"Performing operation: {operator}({argumentsCommaSeperated}) = {int(n1 * n2)}", extra={'request_number': requestsCounter, 'time': currentTime})
                return {"result": n1 * n2}, 200
            elif incaseSensitiveOperator == "divide":
                if n2 == 0:  # cant divide by zero !!! send error with status 409
                    independentLogger.error(f"Server encountered an error ! message: {errorMessage3}", extra={'request_number': requestsCounter, 'time': currentTime})
                    return {"error message": "Error while performing operation Divide: division by 0"}, 409
                durationOfRequest = int((time.time() - start_time) * 1000)
                requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
                independentLogger.info(f"Performing operation {operator}. Result is {int(n1 / n2)}", extra={'request_number': requestsCounter, 'time': currentTime, 'time': currentTime})
                independentLogger.debug(f"Performing operation: {operator}({argumentsCommaSeperated}) = {int(n1 / n2)}", extra={'request_number': requestsCounter, 'time': currentTime})
                return {"result": int(n1 / n2)}, 200
            elif incaseSensitiveOperator == "pow":
                durationOfRequest = int((time.time() - start_time) * 1000)
                requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
                independentLogger.info(f"Performing operation {operator}. Result is {int(pow(n1, n2))}", extra={'request_number': requestsCounter, 'time': currentTime})
                independentLogger.debug(f"Performing operation: {operator}({argumentsCommaSeperated}) = {int(pow(n1, n2))}", extra={'request_number': requestsCounter, 'time': currentTime})
                return {"result": pow(n1, n2)}, 200
    elif incaseSensitiveOperator in specialOperations:  # if we got ''special'' operation, we want just one argument!
        if numberofArguments < 1:
            independentLogger.error(f"Server encountered an error ! message: {errorMessage4}", extra={'request_number': requestsCounter, 'time': currentTime})
            return {"error message": f"Error: Operation {operator} require one argument "}, 409
        elif numberofArguments > 1:
            independentLogger.error(f"Server encountered an error ! message: {errorMessage5}", extra={'request_number': requestsCounter, 'time': currentTime})
            return {"error message": "Error: Too many arguments to perform the operation " + operator}, 409
        else:
            x = theArguments[0]
            if incaseSensitiveOperator == "abs":
                durationOfRequest = int((time.time() - start_time) * 1000)
                requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
                independentLogger.info(f"Performing operation {operator}. Result is {int(abs(x))}", extra={'request_number': requestsCounter, 'time': currentTime})
                independentLogger.debug(f"Performing operation: {operator}({argumentsCommaSeperated}) = {int(abs(x))}", extra={'request_number': requestsCounter, 'time': currentTime})
                return {"result": abs(x)}, 200
            elif incaseSensitiveOperator == "fact":
                if x < 0:
                    independentLogger.error(f"Server encountered an error ! message: {errorMessage6}", extra={'request_number': requestsCounter, 'time': currentTime})
                    return {"error message": 'Error while performing operation Factorial: not supported for the '
                                             'negative number'}, 409
                else:
                    durationOfRequest = int((time.time() - start_time) * 1000)
                    requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
                    independentLogger.info(f"Performing operation {operator}. Result is {int(factorial(x))}", extra={'request_number': requestsCounter, 'time': currentTime})
                    independentLogger.debug(f"Performing operation: {operator}({argumentsCommaSeperated}) = {int(factorial(x))}", extra={'request_number': requestsCounter, 'time': currentTime})
                    return {"result": factorial(x)}, 200
    else:
        independentLogger.error(f"Server encountered an error ! message: {errorMessage7}", extra={'request_number': requestsCounter, 'time': currentTime})
        return {"error message": "Error: unknown operation:" + operator}, 409


# Second is to get the stack size , result status with 200
@niroServer.route('/stack/size', methods=["GET"])
def getStackSize():
    start_time = time.time()
    global requestsCounter
    requestsCounter = requestsCounter + 1
    resource = "/stack/size"
    stackByString = stackToString(niroStack)
    verb = "GET"
    requestsLogger = logging.getLogger("request-logger")
    stackLogger = logging.getLogger("stack-logger")
    requestsLogger.info(f"Incoming request | #{requestsCounter} | resource: {resource} | HTTP Verb {verb}", extra={'request_number': requestsCounter, 'time': currentTime})
    stackLogger.info("Stack size is " + str(len(niroStack)), extra={'request_number': requestsCounter, 'time': currentTime})
    stackLogger.debug("Stack content (first == top): [" + stackByString + "]", extra={'request_number': requestsCounter, 'time': currentTime})
    new_time = time.time()
    durationOfRequest = int((time.time() - start_time) * 1000)
    requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
    return {"result": len(niroStack)}, 200


# Third is to add arguments to niroStack,by PUT method
@niroServer.route('/stack/arguments', methods=["PUT"])
def addArgumentsToStack():
    start_time = time.time()
    global requestsCounter
    requestsCounter = requestsCounter + 1
    resource = "/stack/arguments"
    verb = "PUT"
    currSize = len(niroStack)
    requestsLogger = logging.getLogger("request-logger")
    requestsLogger.info(f"Incoming request | #{requestsCounter} | resource: {resource} | HTTP Verb {verb}", extra={'request_number': requestsCounter, 'time': currentTime})
    stackLogger = logging.getLogger("stack-logger")
    jsonRequest = request.get_json()  # get the request to json , so we can use it
    theArguments = jsonRequest['arguments']
    numberofArguments = len(theArguments)
    errorMessage1 = "Error: There are no arguments to add to the stack"
    errorMessage2 = "Error: invalid type of argument !  Integer only allowed."
    ArgumentsToAddByString = ""
    for element in theArguments:
        element_str = str(element)
        if ArgumentsToAddByString == "":
            ArgumentsToAddByString = element_str
        else:
            ArgumentsToAddByString += "," + element_str
    if numberofArguments == 0:  # if we got the request with no arguments, send error message
        stackLogger.error(f"Server encountered an error ! message: {errorMessage1}", extra={'request_number': requestsCounter, 'time': currentTime})
        return {"error message": "Error: There are no arguments to add to the stack"}, 409
    for argument in theArguments:
        if type(argument) != int:  # told it wouldn't happen , but checking anyway for good measure
            stackLogger.error(f"Server encountered an error ! message: {errorMessage2}", extra={'request_number': requestsCounter, 'time': currentTime})
            return {"error-message": "Error: invalid type of argument !  Integer only allowed."}, 409
        else:
            niroStack.append(argument)  # add the argument and return new size
    stackLogger.info(f"Adding total of {numberofArguments} argument(s) to the stack | Stack size: {len(niroStack)}", extra={'request_number': requestsCounter, 'time': currentTime})
    stackLogger.debug(f"Adding arguments: {ArgumentsToAddByString} | Stack size before {currSize} | stack size after {len(niroStack)}", extra={'request_number': requestsCounter, 'time': currentTime})
    durationOfRequest = int((time.time() - start_time) * 1000)
    requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
    return {"result": len(niroStack)}, 200


# Next is the func that implements the calculation with the stack . with given operation and len of arguments array
def stackCalculate(operator, numberofArguments):
    global StackCalculateResultByInt
    incaseSensitiveOperator = operator.lower()
    global LegalPerformance
    errorMessage1 = f"Error: cannot implement operation {operator}. "f"It requires 2"f" arguments and the stack has only {numberofArguments} arguments"
    errorMessage2 = "Error while performing operation Divide: division by 0"
    errorMessage3 = "Error while performing operation Factorial"
    errorMessage4 = "Error: Unknown operation"
    stackLogger = logging.getLogger("stack-logger")
    if incaseSensitiveOperator in regularOperations:
        if numberofArguments < 2:
            LegalPerformance = 0
            stackLogger.error(f"Server encountered an error ! message: {errorMessage1}", extra={'request_number': requestsCounter, 'time': currentTime})
            return {"error-message": f"Error: cannot implement operation {operator}. "
                                     f"It requires 2"f" arguments and the stack has only {numberofArguments} arguments"}, 409
        else:  # pop 2 arguments and make the operation
            n1 = niroStack.pop()
            n2 = niroStack.pop()
            calculatedArguments[0] = n1
            calculatedArguments[1] = n2
            if incaseSensitiveOperator == "plus":
                StackCalculateResultByInt = int(n1 + n2)
                return {"result": n1 + n2}, 200
            elif incaseSensitiveOperator == "minus":
                StackCalculateResultByInt = int(n1 - n2)
                return {"result": n1 - n2}, 200
            elif incaseSensitiveOperator == "times":
                StackCalculateResultByInt = int(n1 * n2)
                return {"result": n1 * n2}, 200
            elif incaseSensitiveOperator == "divide":
                if n2 == 0:
                    LegalPerformance = 0
                    stackLogger.error(f"Server encountered an error ! message: {errorMessage2}", extra={'request_number': requestsCounter, 'time': currentTime})
                    return {"error message": "Error while performing operation Divide: division by 0"}, 409
                StackCalculateResultByInt = int(n1 / n2)
                return {"result": int(n1 / n2)}, 200
            elif incaseSensitiveOperator == "pow":
                StackCalculateResultByInt = int(pow(n1, n2))
                return {"result": pow(n1, n2)}, 200
    elif incaseSensitiveOperator in specialOperations:
        if numberofArguments == 0:
            LegalPerformance = 0
            stackLogger.error(f"Server encountered an error ! message: {errorMessage1}", extra={'request_number': requestsCounter, 'time': currentTime})
            return {"error-message": f"Error: cannot implement the operation {operator}. It requires 1"
                                     f" arguments and the stack is empty"}, 409
        else:
            x = niroStack.pop()  # get the top from the stack
            calculatedArguments[0] = x
            if incaseSensitiveOperator == "abs":
                StackCalculateResultByInt = int(abs(x))
                return {"result": abs(x)}, 200
            elif incaseSensitiveOperator == "fact":
                if x < 0:
                    LegalPerformance = 0
                    stackLogger.error(f"Server encountered an error ! message: {errorMessage3}", extra={'request_number': requestsCounter, 'time': currentTime})
                    return {"error message": "Error while performing operation Factorial: not supported for the "
                                             "negative number"}, 409
                else:
                    StackCalculateResultByInt = int(factorial(x))
                    return {"result": factorial(x)}, 200
    else:
        LegalPerformance = 0
        stackLogger.error(f"Server encountered an error ! message: {errorMessage4}", extra={'request_number': requestsCounter, 'time': currentTime})
        return {"error-message": "Error: Unknown operation" + operator}, 409


# this func calls the stackCalculator to perform the operation given
@niroServer.route('/stack/operate', methods=["GET"])
def performTheOperate():
    start_time = time.time()
    global requestsCounter
    global LegalPerformance
    global StackCalculateResultByInt
    requestsCounter = requestsCounter + 1
    argumentsCommaSeperated = ""
    resource = "/stack/operate"
    verb = "GET"
    requestsLogger = logging.getLogger("request-logger")
    stackLogger = logging.getLogger("stack-logger")
    requestsLogger.info(f"Incoming request | #{requestsCounter} | resource: {resource} | HTTP Verb {verb}", extra={'request_number': requestsCounter, 'time': currentTime})
    stackLogger = logging.getLogger("stack-logger")
    numberofArguments = len(niroStack)  # get len of stack
    Parameters = request.args  # get arguments from the request
    operator = Parameters.get("operation", type=str)  # get the operator
    durationOfRequest = int((time.time() - start_time) * 1000)
    requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
    result = stackCalculate(operator, numberofArguments)  # need to return result from stackCalculate
    for element in calculatedArguments:
        if type(element) == int:
            element_str = str(element)
            if argumentsCommaSeperated == "":
                argumentsCommaSeperated = element_str
            else:
                argumentsCommaSeperated += "," + element_str
    for i in range(len(calculatedArguments)):
        calculatedArguments[i] = False
    if LegalPerformance == 1:
        stackLogger.info(f"Performing operation {operator}. Result is {StackCalculateResultByInt} | stack size: {len(niroStack)}", extra={'request_number': requestsCounter, 'time': currentTime})
        stackLogger.debug(f"Performing operation: {operator}({argumentsCommaSeperated}) = {StackCalculateResultByInt}", extra={'request_number': requestsCounter, 'time': currentTime})
    else:
        LegalPerformance = 1
    return result


# Next is func that removes arguments from niroStack , if any exists.
# A message error will be given if not enough exists
@niroServer.route('/stack/arguments', methods=["DELETE"])
def removeArgumentsFromStack():
    start_time = time.time()
    global requestsCounter
    requestsCounter = requestsCounter + 1
    resource = "/stack/arguments"
    verb = "DELETE"
    stackLogger = logging.getLogger("stack-logger")
    requestsLogger = logging.getLogger("request-logger")
    requestsLogger.info(f"Incoming request | #{requestsCounter} | resource: {resource} | HTTP Verb {verb}", extra={'request_number': requestsCounter, 'time': currentTime})
    Parameters = request.args
    countToDelete = Parameters.get("count", type=int)  # to get how many we need to delete from niroStack
    temp = countToDelete
    errorMessage1 = f"Error: cannot remove {countToDelete} from the stack. It has only {len(niroStack)} arguments"
    if countToDelete > len(niroStack):  # more to delete then existing in niroStack already
        stackLogger.error(f"Server encountered an error ! message: {errorMessage1}", extra={'request_number': requestsCounter, 'time': currentTime})
        return {"error-message": f"Error: cannot remove {countToDelete} from the stack. It has only {len(niroStack)} arguments"}, 409
    else:  # stack size is bigger , can implement the removing
        while countToDelete > 0:
            niroStack.pop()
            countToDelete = countToDelete - 1
    stackLogger.info(f"Removing total {temp} argument(s) from the stack | Stack size: {len(niroStack)}", extra={'request_number': requestsCounter, 'time': currentTime})
    durationOfRequest = int((time.time() - start_time) * 1000)
    requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
    return {"result": len(niroStack)}, 200


@niroServer.route('/logs/level', methods=["GET"])
def getCurrentloggerLever():
    start_time = time.time()
    global requestsCounter
    requestsCounter = requestsCounter + 1
    Parameters = request.args
    resource = "/logs/level"
    verb = "GET"
    requestsLogger = logging.getLogger("request-logger")
    requestsLogger.info(f"Incoming request | #{requestsCounter} | resource: {resource} | HTTP Verb {verb}", extra={'request_number': requestsCounter, 'time': currentTime})
    loggerName = Parameters.get("logger-name", type=str)
    if loggerName in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(loggerName)
        durationOfRequest = int((time.time() - start_time) * 1000)
        requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
        LevelOfLogger = getLoggerLevelByString(logger.level)
        return LevelOfLogger, 200
    else:
        new_time = time.time()
        durationOfRequest = int((time.time() - start_time) * 1000)
        requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
        return {"error-message": "Error: This logger does not exist!"}, 409


@niroServer.route('/logs/level', methods=["PUT"])
def setLoggerNewLevel():
    start_time = time.time()
    global requestsCounter
    requestsCounter = requestsCounter + 1
    resource = "/logs/level"
    verb = "PUT"
    Parameters = request.args
    loggerName = Parameters.get("logger-name", type=str)
    requestsLogger = logging.getLogger("request-logger")
    requestsLogger.info(f"Incoming request | #{requestsCounter} | resource: {resource} | HTTP Verb {verb}", extra={'request_number': requestsCounter, 'time': currentTime})
    NewLoggerLevel = Parameters.get("logger-level", type=str)
    if loggerName in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(loggerName)
        logger.setLevel(NewLoggerLevel)
        NewLevelOfLogger = getLoggerLevelByString(logger.level)
        durationOfRequest = int((time.time() - start_time) * 1000)
        requestsLogger.debug(f"request #{requestsCounter} duration: {durationOfRequest}ms", extra={'request_number': requestsCounter, 'time': currentTime})
        return NewLevelOfLogger, 200
    else:
        return {"error-message": "Error: This logger does not exist!"}, 409


def createLoggers():
    # Requests Logger
    requestsLogger = logging.getLogger("request-logger")
    requestsLogger.setLevel(logging.INFO)
    fileHandler1 = logging.FileHandler('logs/requests.log')
    screenHandler1 = logging.StreamHandler()
    formatter = logging.Formatter("%(time)s %(levelname)s: %(message)s | request #%(request_number)s")
    fileHandler1.setFormatter(formatter)
    screenHandler1.setFormatter(formatter)
    requestsLogger.addHandler(fileHandler1)
    requestsLogger.addHandler(screenHandler1)

    # Stack Logger
    stackLogger = logging.getLogger("stack-logger")
    stackLogger.setLevel(logging.INFO)
    fileHandler2 = logging.FileHandler('logs/stack.log')
    fileHandler2.setFormatter(formatter)
    stackLogger.propagate = False
    stackLogger.addHandler(fileHandler2)

    # Independent Logger
    independentLogger = logging.getLogger("independent-logger")
    independentLogger.setLevel(logging.DEBUG)
    independentLogger.propagate = False
    fileHandler3 = logging.FileHandler('logs/independent.log')
    fileHandler3.setFormatter(formatter)
    independentLogger.addHandler(fileHandler3)


def createFoldersAndFiles():
    folderName = "logs"
    filesNames = ["independent.log", "requests.log", "stack.log"]
    if not os.path.exists(folderName):
        os.makedirs('logs')
    for file in filesNames:
        file_path = f"{folderName}/{file}"
        with open(file_path, "w") as f:
            pass


# FOLLOWING MAIN RUNS THE SERVER WITH PORT 9583
#  runs on localhost
if __name__ == '__main__':
    createFoldersAndFiles()  # Creates logs folder , and 3 files inside it, if they do not exist yet
    createLoggers()  # Creates the loggers and their behavior
    niroServer.run(host="localhost", port=9583, debug=True)
