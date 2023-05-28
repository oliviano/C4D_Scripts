# simple code to save childs PSR & Color to CSV
# used as part of tools to import into TouchDesigner
# by Olivier Jean
# tested in r23
# https://github.com/oliviano/C4D_Scripts

import c4d
import csv
from c4d.modules import mograph as mo
from c4d import documents as docs

def get_descendants(op):
    """ Returns all descendants of op.
    """
    if not isinstance(op, c4d.GeListNode):
        return []

    res = []

    for child in op.GetChildren():
        res.append(child)
        res += get_descendants(child) # recursion happens here
    return res

def write_data_to_csv(data):
    file_path = op[c4d.ID_USERDATA,3]

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print("Data saved to file {}".format(file_path))



def main_iteration(list_of_objects):

    # we prepare dat container / list we clear data and insert a new header.
    data = []
    data.append(["i", "position.x", "position.y", "position.z", "rotation.x", "rotation.y", "rotation.z", "scale.x", "scale.y", "scale.z", "color.x", "color.y", "color.z"])
    index = 1

    #main iteration, we append our child params to data list variable
    for node in list_of_objects:
       position = node.GetAbsPos()
       rotation = node.GetAbsRot()
       #scale = node.GetAbsScale()
       scale = node.GetRad() # we use bounding box for our scale here.
       color = (1.0,1.0,1.0)

       # Add the data to the list
       data.append([index, position.x, position.y, position.z, rotation.x, rotation.y, rotation.z, scale.x, scale.y, scale.z, color[0], color[1], color[2] ])
       index = index + 1

    # Write the data to a CSV file
    write_data_to_csv(data)
    print("{} clone data processed".format(len(list_of_objects)))
    #print("some rouding error on the scale exports")

# Main function
def main():
    # Get the SPECIFIED USERDATA object
    obj = op[c4d.ID_USERDATA,2] #obj = doc.GetFirstObject()

    # Get the state of the button
    button_state = op[c4d.ID_USERDATA,6]

    # If the button is pressed, export the MoGraph data
    if button_state:
        main_iteration(get_descendants(obj))

# Execute main()
if __name__=='__main__':
    main()