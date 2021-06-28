from collections import defaultdict

def add(text):
    orderID = text[0]
    price = text[2]
    side = text[3]
    quantity = int(text[4])

    mbpKey = price + side
    mboKey = orderID + side

    # Key hasn't been entered yet
    if mbpBook[mbpKey] == []:
        mbpBook[mbpKey] = [quantity, 1]
        output.write("Key: " + mbpKey + ", Action: Add, Quantity: " + str(mbpBook[mbpKey][0]) + ", Orders: " + str(mbpBook[mbpKey][1]) + "\n")
    else:
        previous = mbpBook[mbpKey]
        mbpBook[mbpKey] = [quantity + previous[0], previous[1] + 1]
        output.write("Key: " + mbpKey + ", Action: Update, Quantity: " + str(mbpBook[mbpKey][0]) + ", Orders: " + str(mbpBook[mbpKey][1]) + "\n")

    # mboBook[1] points to the mbpBook
    mboBook[mboKey] = [quantity, mbpKey]

def delete(text):
    orderID = text[0]
    side = text[3]
    mboKey = orderID + side

    mbpKey = mboBook[mboKey][1]
    quantity = mboBook[mboKey][0]
    del mboBook[mboKey]

    if mbpBook[mbpKey][1] == 1:
        del mbpBook[mbpKey]
        output.write("Key: " + mbpKey + ", Action: Delete, Quantity: None, Orders: None\n")
    else:
        mbpBook[mbpKey][0] -= quantity
        mbpBook[mbpKey][1] -= 1
        output.write("Key: " + mbpKey + ", Action: Update, Quantity: " + str(mbpBook[mbpKey][0]) + ", Orders: " + str(mbpBook[mbpKey][1]) + "\n")

def update(text):
    orderID = text[0]
    side = text[3]
    difference = int(text[4])

    if difference > 0:
        difference *= -1
    mboKey = orderID + side

    mbpKey = mboBook[mboKey][1]
    if mboBook[mboKey][0] + difference <= 0:
        del mboBook[mboKey]
        mbpBook[mbpKey][0] += difference
        mbpBook[mbpKey][1] -= 1
        if mbpBook[mbpKey][1] == 0:
            del mbpBook[mbpKey]
            output.write("Key: " + mbpKey + ", Action: Delete, Quantity: None, Orders: None\n")
        else:
            output.write("Key: " + mbpKey + ", Action: Update, Quantity: " + str(mbpBook[mbpKey][0]) + ", Orders: " + str(mbpBook[mbpKey][1]) + "\n")
    else:
        mboBook[mboKey][0] += difference
        mbpBook[mbpKey][0] += difference
        output.write("Key: " + mbpKey + ", Action: Update, Quantity: " + str(mbpBook[mbpKey][0]) + ", Orders: " + str(mbpBook[mbpKey][1]) + "\n")

file = open("NCM_Raw_MBO_Data.txt", "r")
output = open("output.txt", "w")
mbpBook = defaultdict(list)
mboBook = defaultdict(list)    
while True:
    text = file.readline().strip("\n").split(",")

    # End of File
    if text == ['']:
        break

    if text[1] == 'Add':
        add(text)
    elif text[1] == 'Delete':
        delete(text)
    elif text[1] == 'Update':
        update(text)

file.close()
output.close()