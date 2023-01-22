import maya.cmds as cmds

cmds.window("Auto Rigger")
cmds.rowColumnLayout(nc = 2)

cmds.button(l = "Create Locators", w = 200, c = "createLocators()") # <- The End is calling function
cmds.button(l = "Delete Locators", w = 200, c = "deleteLocators()")

cmds.text("Spine Count", l = "Spine Count")
spineCount = cmds.intField(minValue = 1, maxValue = 10, value = 4)
editMode = True
cmds.button(l = "Edit Mode", w = 200, c = "lockAll(editMode)")

cmds.showWindow()




def createLocators():
    if cmds.objExists("Loc_Master"):
        print ("Loc_Master already exists")
    else:
        cmds.group(em = True, name = ("Loc_Master"))
    root = cmds.spaceLocator(n = ("Loc_Root"))
    cmds.scale(0.1,0.1,0.1, root)
    cmds.move(0,1,0, root)
    cmds.parent(root, "Loc_Master")
    
    createSpine()
    
def createArms(side):
    if side == 1: #Left
        if cmds.objExists("L_Arm_GRP"): # checking if it already exists 
            print ("L_Arm Exists")
        else:
            l_Arm = cmds.group(em = True, name = "L_Arm_GRP") # Creates the group
            cmds.parent(l_Arm, "Loc_Spine_" + str(cmds.intField(spineCount, query = True, value = True) - 1)) # parents the group to the spine based on the spine count 
             
            l_upperArm = cmds.spaceLocator(n = "Loc_L_UpperArm") 
            cmds.scale(0.1,0.1,0.1, l_upperArm)
            cmds.parent(l_upperArm, l_Arm)
            
            l_Elbow = cmds.spaceLocator(n = "Loc_L_Elbow") 
            cmds.scale(0.1,0.1,0.1, l_Elbow)
            cmds.parent(l_Elbow, l_upperArm)
            
            l_Wrist = cmds.spaceLocator(n = "Loc_L_Wrist") 
            cmds.scale(0.1,0.1,0.1, l_Wrist)
            cmds.parent(l_Wrist, l_Elbow)
            
            
            # moving to bottom, causes all of the locators above to be moved to the right spot 
            cmds.move(0.35 * side, 1 + (0.25 * cmds.intField(spineCount, query = True, value = True)), 0, l_Arm) # moves the left arm to the left side of the rig
            
            
            # Move Left Elbow
            cmds.move(0.6 * side, 1.4, -0.2, l_Elbow)
            
            # Move R Wrist
            cmds.move(0.8 * side, 1, 0, l_Wrist)
            
    else: #Right
        if cmds.objExists("r_Arm_GRP"):
            print ("r_Arm Exists")
        else:
            # R_Arm
            r_Arm = cmds.group(em = True, name = "R_Arm_GRP")
            cmds.parent(r_Arm, "Loc_Spine_" + str(cmds.intField(spineCount, query = True, value = True) - 1))
            #R_UpperArm
            r_upperArm = cmds.spaceLocator(n = "Loc_R_UpperArm") 
            cmds.scale(0.1,0.1,0.1, r_upperArm)
            cmds.parent(r_upperArm, r_Arm)
            
            r_Elbow = cmds.spaceLocator(n = "Loc_R_Elbow") 
            cmds.scale(0.1,0.1,0.1, r_Elbow)
            cmds.parent(r_Elbow, r_upperArm)
            
            
            r_Wrist = cmds.spaceLocator(n = "Loc_R_Wrist") 
            cmds.scale(0.1,0.1,0.1, r_Wrist)
            cmds.parent(r_Wrist, r_Elbow)
            
            # moving to bottom, causes all of the locators above to be moved to the right spot 
            cmds.move(0.35 * side, 1 + (0.25 * cmds.intField(spineCount, query = True, value = True)), 0, r_Arm)
            
            # Move Right Elbow
            cmds.move(0.6 * side, 1.4, -0.2, r_Elbow)
            # Move Right Wrist
            cmds.move(0.8 * side, 1, 0, r_Wrist)
            
            
            
    
    
def lockAll(lock):
    global editMode
    
    axis = ['x', 'y', 'z']
    attr = ['t', 'r', 's']
    
    nodes = cmds.listRelatives('Loc_*' ,allParents = True)
    
    
    for axe in axis:
        for att in attr:
            for node in nodes:
                cmds.setAttr(node+'.'+att+axe, lock = lock)
    if editMode == False:
        editMode = True;    
    else:
        editMode = False;
    print ("Lock All")
        
    
    
def createSpine():
    
    for i in range(0, cmds.intField(spineCount, query = True, value = True)):
        spine = cmds.spaceLocator(n = "Loc_Spine_" + str(i))
        cmds.scale(0.1,0.1,0.1, spine)
        if i == 0:
            cmds.parent(spine, "Loc_Root")
        else:
            cmds.parent(spine, "Loc_Spine_" + str(i - 1))
            
        cmds.move(0,1.25 + (0.25 * i), 0, spine)
        print (i)
                
    createArms(1)
    createArms(-1) 

    

    
def deleteLocators():
    print ("Delete")
    nodes = cmds.ls("Loc_*")
    cmds.delete(nodes)





    
    