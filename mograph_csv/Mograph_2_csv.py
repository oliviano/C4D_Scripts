# simple code to save clones PSR & Color to CSV
# used as part of tools to import into TouchDesigner
# by Olivier Jean
# tested in r23
# https://github.com/oliviano/C4D_Scripts

import c4d
import csv
from c4d.modules import mograph as mo

#Preset / Hardcoded file path
#file_path = c4d.documents.GetActiveDocument().GetDocumentPath() + "/mograph_data.csv"

def write_data_to_csv(file_name, data):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def export_mograph_data(cloner):
    # User data file path
    file_path = op[c4d.ID_USERDATA,3]

    # Get the Cloner object
    # cloner = op[c4d.ID_USERDATA,2]

    if not cloner:
        print('No Cloner object linked')
        return

    if not isinstance(cloner, c4d.BaseObject) or cloner.GetType() != 1018544:  # 1018544 is the ID for the Cloner object
        print('Linked object is not a Cloner object')
        return

    # Get the MoData from the Cloner object
    md = mo.GeGetMoData(cloner)
    if md is None:
        return

    # Get the arrays for position, scale, rotation and color
    clones_matrix = md.GetArray(c4d.MODATA_MATRIX)
    clones_colors = md.GetArray(c4d.MODATA_COLOR)

    # Prepare the data
    data = []
    data.append(["i", "position.x", "position.y", "position.z", "rotation.x", "rotation.y", "rotation.z", "scale.x", "scale.y", "scale.z", "color.x", "color.y", "color.z"])
    for i in range(md.GetCount()):
        # positions
        position = clones_matrix[i].off
        #print(position)

        # rotations
        myrot = c4d.utils.MatrixToHPB(clones_matrix[i],9) # we have to play with rotation order, check SDK ( xyz is int 5, HPB is 9)
        myRx = c4d.utils.RadToDeg(myrot.x)
        myRy = c4d.utils.RadToDeg(myrot.y)
        myRz = c4d.utils.RadToDeg(myrot.z)
        #print( myRx, myRy, myRz)

        #scale
        sx = clones_matrix[i].GetScale().x # Get scale x
        sy = clones_matrix[i].GetScale().y # Get scale y
        sz = clones_matrix[i].GetScale().z # Get scale z
        #print(sx, sy, sz)

        # color
        color = clones_colors[i]

        # Add the data to the list
        data.append([i, position.x, position.y, position.z, myRx, myRy, myRz, sx, sy, sz, color.x, color.y, color.z])

    # Write the data to a CSV file
    write_data_to_csv(file_path, data)
    print("{} clone data saved to file {}".format(md.GetCount(),file_path))
    #print("some rouding error on the scale exports")

def main():

    # Get the Cloner object
    cloner = op[c4d.ID_USERDATA,2]

    # Get the state of the button
    button_state = op[c4d.ID_USERDATA,6]

    # If the button is pressed, export the MoGraph data
    if button_state:
        export_mograph_data(cloner)


# Execute main()
if __name__=='__main__':
    main()