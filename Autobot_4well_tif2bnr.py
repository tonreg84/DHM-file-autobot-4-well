def tif2bnr(input_file,timestampsfile,wv,n_1,n_2,pz,output_file):
#this function converts a tiff sequence (data from LynceeTec Koala) into a bnr sequence (LynceeTec format) and applies the inverse height conversion factor

#input_file: filepath of the tiff sequence
#timestampsfile: int32 array from 3rd column of Koala timestamps file
#output_file: destination of the bnr sequence file

    import numpy
    import tifffile
    
    #read timestamps from timestampsfile
    with open(timestampsfile, 'r') as infile:
        k=0
        timelist=[]
        for line in infile:
            # Split the line into a list of numbers
            numbers = line.split()
            time=numpy.single(float(numbers[3]))
            timelist.append(time)
            k=k+1          
        timestamps=numpy.array(timelist)
    nImages=len(timestamps) #sequence length
    
    #get first image from tiff stack
    phase_map = tifffile.imread(input_file, key=0)
    w = len(phase_map[0,:])
    h = len(phase_map[:,0])
    
    #write meta data to bnr file
    fileID=open(output_file,'w')
    numpy.array(nImages, dtype=numpy.int32).tofile(fileID)
    numpy.array(w, dtype=numpy.int32).tofile(fileID)
    numpy.array(h, dtype=numpy.int32).tofile(fileID)
    numpy.array(pz, dtype=numpy.float32).tofile(fileID)
    numpy.array(wv, dtype=numpy.float32).tofile(fileID)
    numpy.array(n_1, dtype=numpy.float32).tofile(fileID)
    numpy.array(n_2, dtype=numpy.float32).tofile(fileID)
    for k in range(0,nImages):
        numpy.array(timestamps[k], dtype=numpy.float32).tofile(fileID)

    #write images to bnr file
    for k in range(0,nImages):
        phase_map = tifffile.imread(input_file, key=k)/(wv/(2*3.14159*(n_2-n_1))) #wavelength/(2*3.14159*(n_1-n_2)) = 1/hcon*10^-9
        
        phase_map.astype(numpy.float32).tofile(fileID)

    fileID.close()