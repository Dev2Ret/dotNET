import os
import sys
import clr
from enum import Enum

import streamlit as st

st.header("DotNet Test")

if st.button("Click Me"):
    clr.AddReference("System.Runtime.InteropServices")

    from System.Runtime.InteropServices import Marshal
    clr.AddReference(R"C:\Program Files\Computers and Structures\SAP2000 23\SAP2000v1.dll")

    from SAP2000v1 import *
    Remote = False

    RemoteComputer = "SpareComputer-DT"

    AttachToInstance = True
    SpecifyPath = False

    ProgramPath = R"C:\Program Files\Computers and Structures\SAP2000 23\SAP2000v1.dll"

    APIPath = R"C:\Users\tkdlr\Downloads\CSi_SAP2000_API_Example"

    if not os.path.exists(APIPath):
        try:
            os.makedirs(APIPath)
        except OSError:
            pass

    ModelPath = APIPath + os.sep + 'Ceyhan_001.sdb'

    helper = cHelper(Helper())

    if AttachToInstance:
        try:
            if Remote:
                mySAPObject = cOAPI(helper.GetObjectHost(RemoteComputer, "CSI.SAP2000.API.SAPObject"))
            else:
                mySAPObject = cOAPI(helper.GetObject("CSI.SAP2000.API.SAPObject"))
        except:
            print("No running instance of the program found or failed to attach.")
            sys.exit(-1)

    else:
        if SpecifyPath:
            try:
                if Remote:
                    mySAPObject = cOAPI(helper.CreateObjectHost(RemoteComputer, ProgramPath))
                else:
                    mySAPObject = cOAPI(helper.CreateObject(ProgramPath))
            except:
                print("Cannot start a new instance of the program fomr " + ProgramPath)
                sys.exti(-1)
        else:
            try:
                if Remote:
                    mySAPObject = cOAPI(helper.CreateObjectProgIDHost(RemoteComputer, "CSI.SAP2000.API.SAPObject"))
                else:
                    mySAPObject = cOAPI(helper.CreateObjectProgID("CSI.SAP2000.API.SAPObject"))
            except:
                    print("Cannot start a new instance of the program.")
                    sys.exit(-1)

    mySAPObject.ApplicationStart()

    #create SapModel object
    SapModel = cSapModel(mySAPObject.SapModel)

    #initialize model
    SapModel.InitializeNewModel()

    #create new blank model
    File = cFile(SapModel.File)
    ret = File.NewBlank()

    #define material property
    mat_con = 2
    PropMaterial = cPropMaterial(SapModel.PropMaterial)
    ret = PropMaterial.SetMaterial('CONC', eMatType(mat_con))