import requests, csv, datetime, time

ALLY_CODES = {"NAME":"ALLY_CODE"} # populate dict with name:ally_code  

def getData(person):
    """
    str->Dict or None
    Gets the CR data from the server.
    """

    url = f"https://swgoh.gg/api/player/{ALLY_CODES[person]}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text) 
        return None

def log(data, filename):
    """
    Data, Filename->None
    Writes inputted data to the given file
    """
    with open(filename, "w") as file:
        file.write(str(data))
        file.close()


def writeTimeStamp(gp, note=""):
    """
    int,str->str
    Writes the current timestamp and GP to a CSV file, also writes an optional str to the end of the row. Returns current timestamp
    """
    with open('gp.csv', 'a', newline="") as file:
        csv.writer(file).writerow([gp,datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%d %H:%M:%S'),note])

    return datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%d %H:%M:%S')

def main():
    while True:
        # check if right time
        if datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%H:%M') == "13:31":
            # loop through list of allycodes
            for i in ALLY_CODES:
                # get raw data
                data = getData(i)
                log(data,"log.txt")

                # get gp
                playerdata = data.get("data")
                gp = playerdata["galactic_power"]

                # save gp to the csv
                timestamp = writeTimeStamp(gp, i)
                print(f'{i} has {gp} gp as of {timestamp}')
            time.sleep(80)
        
        print("Running")
        time.sleep(15)


# runs main
if __name__ == "__main__":
    main()