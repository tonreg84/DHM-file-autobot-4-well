"""
DHM file autobot 4-well
Autor: tonreg, team UMI, CNP-CHUV Lausanne

Version 01 - 17.04.2024

This program is used to post-process data recorded during an experience with a LynceeTec DHM,
where four sequences are recorded simultaneously with the stage-control tool.

After doing the alignment of the four sequences with FIJI, this program converts the four aligned sequences from TIFF to "LynceeTec-bnr" file format and renames the files.
The tiff files habe to be in the main folder containing the subfolders "00001, 00002, 00003, and 00004" created by Koala.
"""
 
import os
import PySimpleGUI as simgui
from datetime import datetime
from Autobot_4well_tif2bnr import tif2bnr

thisdate=datetime.today().strftime('%Y%m%d')
unitlist=['M', 'mM', 'uM', 'nM']

# Window layout in 3 columns

#Input parameter
files_and_parameter = [
    [simgui.Text("Chose folder:"),
     simgui.In(size=(40, 1), enable_events=True, key="mainfolder"),
     simgui.FolderBrowse(),],
    [
     simgui.Text("Wavelength(nm):"),
     simgui.In(size=(5, 1), default_text='665.8', enable_events=False, key="wv"),
     simgui.Text("n_1:"),
     simgui.In(size=(5,1), default_text='1', enable_events=False, key="n_1"),
     simgui.Text("n_2:"),
     simgui.In(size=(5, 1), default_text='1.5', enable_events=False, key="n_2"),
     simgui.Text("Pixel size:"),
     simgui.In(size=(12, 1), default_text='1.1520307e-06', enable_events=False, key="pz"),
     ],
    [simgui.Text("Output file tags:"),],
    [simgui.Text("Date:"),
     simgui.In(size=(10, 1), default_text=thisdate, enable_events=False, key="date"),
     simgui.Text("Microscope:"),
     simgui.In(size=(3, 1),default_text='F', enable_events=False, key="micro"),
     simgui.Text("N° expérience:"),
     simgui.In(size=(6, 1), enable_events=False, key="exp"),],
    [
    simgui.Text("Lignee Q1:"),
    simgui.In(size=(6, 1), enable_events=False, key="lin1"),
    simgui.Text("Lignee Q2:"),
    simgui.In(size=(6, 1), enable_events=False, key="lin2"),
    simgui.Text("Lignee Q3:"),
    simgui.In(size=(6, 1), enable_events=False, key="lin3"),
    simgui.Text("Lignee Q4:"),
    simgui.In(size=(6, 1), enable_events=False, key="lin4"),
     ],
    [simgui.Text("Drogue:"),
     simgui.In(size=(6, 1), enable_events=False, key="drug"),
     simgui.Text("Concentration:"),
     simgui.In(size=(3, 1), enable_events=False, key="conc"),
     simgui.Combo(unitlist, default_value='uM', enable_events=True, size=(3, 1), key="unit"),
     simgui.Text("Bloqueur:"),
     simgui.In(size=(6, 1), enable_events=False, key="bloq"),],
    [
     simgui.Button("Autobots rollout!", enable_events=True, key='start'),
     simgui.Multiline(default_text='File conversion: selecting input', enable_events=True, size=(50, 3), key='info'),
    ],
    ]

# ----- Full layout -----
layout = [
    [
     simgui.Column(files_and_parameter)
    ]
]

window = simgui.Window("DHM file autobot", layout)

# Main programme
while True:
    event, values = window.read()
    if event == simgui.WIN_CLOSED:
        break
    
    #set parameters
    mainfolder=values['mainfolder']
      
    #start main program
    if event == 'start':
        if os.path.isfile(mainfolder+'/0_aligned.tif')==False or os.path.isfile(mainfolder+'/1_aligned.tif')==False or os.path.isfile(mainfolder+'/2_aligned.tif')==False or os.path.isfile(mainfolder+'/3_aligned.tif')==False:
            simgui.popup_auto_close('Error: TIF input files missing.')
            print(mainfolder+'/0_aligned.tif', os.path.isfile(mainfolder+'/0_aligned.tif'))
            print(mainfolder+'/1_aligned.tif', os.path.isfile(mainfolder+'/1_aligned.tif'))
            print(mainfolder+'/2_aligned.tif', os.path.isfile(mainfolder+'/2_aligned.tif'))
            print(mainfolder+'/3_aligned.tif', os.path.isfile(mainfolder+'/3_aligned.tif'))
        else:
            window['info'].update(value='File conversion: File conversion in progress.\n 0 of 4 sequences converted')
            
            output_file_name_A=mainfolder+'/'+thisdate+'_'+values['micro']+'_Exp'+values['exp']
            if values['bloq']=='':
                output_file_name_B='_'+values['drug']+'_'+values['conc']+values['unit']+'.bnr'
            else:          
                output_file_name_B='_'+values['drug']+'_'+values['conc']+values['unit']+'_'+values['bloq']+'.bnr'
            
            wv=float(values['wv'])
            n_1=float(values['n_1'])
            n_2=float(values['n_2'])
            pz=float(values['pz'])
            print(wv, n_1, n_2, pz)
            
            #Q1:
            input_file1=mainfolder+'/0_aligned.tif'
            timestampsfile1=mainfolder+'/00001_00001/timestamps.txt'
            output_file1=output_file_name_A+'_w001_'+values['lin1']+output_file_name_B
            tif2bnr(input_file1,timestampsfile1,wv,n_1,n_2,pz,output_file1)
            os.remove(input_file1)
            window['info'].update(value='File conversion: File conversion in progress.\n 1 of 4 sequences converted.')
            
            #Q2:
            input_file2=mainfolder+'/1_aligned.tif'
            timestampsfile2=mainfolder+'/00001_00002/timestamps.txt'
            output_file2=output_file_name_A+'_w002_'+values['lin2']+output_file_name_B
            tif2bnr(input_file2,timestampsfile2,wv,n_1,n_2,pz,output_file2)
            os.remove(input_file2)
            window['info'].update(value='File conversion: File conversion in progress.\n 2 of 4 sequences converted.')
            
            #Q3:
            input_file3=mainfolder+'/2_aligned.tif'
            timestampsfile3=mainfolder+'/00002_00001/timestamps.txt'
            output_file3=output_file_name_A+'_w003_'+values['lin3']+output_file_name_B
            tif2bnr(input_file3,timestampsfile3,wv,n_1,n_2,pz,output_file3)
            os.remove(input_file3)
            window['info'].update(value='File conversion: File conversion in progress.\n 3 of 4 sequences converted.')
                
            #Q4:
            input_file4=mainfolder+'/3_aligned.tif'
            timestampsfile4=mainfolder+'/00002_00002/timestamps.txt'
            output_file4=output_file_name_A+'_w004_'+values['lin4']+output_file_name_B
            tif2bnr(input_file4,timestampsfile4,wv,n_1,n_2,pz,output_file4)
            os.remove(input_file4)
            window['info'].update(value='File conversion: File conversion done.\n 4 of 4 sequences converted\nYou can select new input and new file names.')

window.close()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
