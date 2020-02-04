# Create a Script to Allow User to Add Devices
myFile = open("devices.txt", "a")
while True:
    newDevice = input("Enter device name: ")
    if newDevice == "exit":
        print("All done!")
        break
    myFile.write(newDevice + "\n")
myFile.close()
