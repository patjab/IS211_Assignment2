import urllib.request, datetime, logging, argparse, urllib.error

def downloadData(url):
    page = urllib.request.urlopen(url)


    return page


def processData(pageContent):

    dictBirthdays = {}
    lineCounter = 0

    LOG_FILENAME = 'error.log'
    assignment2 = logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)

    for line in pageContent:

        lineAsString = line.decode()

        categorizedStrings = lineAsString.split(",")
        categorizedBDay = categorizedStrings[2].split("/")
        isValidDate = False
        birthday = None

        if ( categorizedStrings[0].isdigit() ):
            #if not correct will yield not 3, if yields 3 possibly correct
            bdayComponents = categorizedBDay.__len__()

            if ( bdayComponents != 3 ):
                isValidDate = False

            elif ( bdayComponents == 3  ):

                inRange = int(categorizedBDay[2]) > 999 and int(categorizedBDay[2]) < 10000 and int(categorizedBDay[1]) > 0 and int(categorizedBDay[1]) < 13 and int(categorizedBDay[0]) > 0 and int(categorizedBDay[0]) < 32

                if ( inRange ):
                    isThirtyOneDayMonth = int(categorizedBDay[1]) == 1 or int(categorizedBDay[1]) == 3 or int(categorizedBDay[1]) == 5 or int(categorizedBDay[1]) == 7 or int(categorizedBDay[1]) == 8 or int(categorizedBDay[1]) == 10 or int(categorizedBDay[1]) == 12
                    isThirtyDayMonth =  int(categorizedBDay[1]) == 4 or int(categorizedBDay[1]) == 6 or int(categorizedBDay[1]) == 9 or int(categorizedBDay[1]) == 11
                    isFebruary = int(categorizedBDay[1]) == 2
                    isLeapYear = (int(categorizedBDay[2]) % 4 == 0) and (int(categorizedBDay[2]) % 100 != 0 or (int(categorizedBDay[2]) % 100 == 0 and int(categorizedBDay[2]) % 400 == 0))

                    if ( isThirtyOneDayMonth or (isThirtyDayMonth and categorizedBDay[0] != 31) ):
                        birthday = datetime.date(int(categorizedBDay[2]), int(categorizedBDay[1]), int(categorizedBDay[0]))
                        isValidDate = True

                    elif ( isFebruary ):
                        if ( (isLeapYear and int(categorizedBDay[0]) < 30 ) or ( (not isLeapYear) and int(categorizedBDay[0]) < 29 )):
                            birthday = datetime.date(int(categorizedBDay[2]), int(categorizedBDay[1]), int(categorizedBDay[0]))
                            isValidDate = True

        #since lineCounter = 0 is the header, it is not a technical error
        if ( lineCounter != 0 ):
            dictBirthdays[int(categorizedStrings[0])] = (categorizedStrings[1], birthday)

            if ( not isValidDate):
                logging.error("Error processing line # %i for ID # %i", lineCounter, int(categorizedStrings[0]))

        lineCounter += 1

    return dictBirthdays


def displayPerson(id, personData):

    if ( (id in personData.keys()) and (personData[id][1] != None)):
        name = personData[id][0]
        birthyear = personData[id][1].year
        birthmonth = personData[id][1].month
        birthday = personData[id][1].day

        print("Person #", id, "is", name, "with a birthday of", birthyear, "-", birthmonth, "-", birthday)

    else:
        print("No user found with that id")

def main():

    csvData = None

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Read a file at this URL")
    args = parser.parse_args()
    if args.url == None:
        print("URL is required. Program exiting.")
        exit()
    elif args.url:
            try:
                csvData = downloadData(args.url)
            except urllib.error.HTTPError:
                print("HTTPError: Server not found. Please check the address and try again.")
                quit()
            except urllib.error.URLError:
                print("URLError: No network connection found. Please check your connection and try again.")
                quit()


    personData = processData(csvData)


    while True:
        idNum = input("Enter an ID # : ")

        try:
            if ( int(idNum) <= 0 ):
                break
            elif ( int(idNum) > 0 ):
                displayPerson(int(idNum), personData)
        except:
            2+2





if __name__ == '__main__': main()


