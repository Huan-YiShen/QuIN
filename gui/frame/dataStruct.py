class analysisFigures():
    init_fig = None # initial figure
    cropped_fig = None # fine turned for parabola fits
    pixel_ev = None # pixel vs. ev with cropped parabola
    angle_ev = None # angle vs. ev with cropped parabola 
    kpara_ev = None # k-parallel vs. ev with cropped parabola


class parabolaData():
    # data extracted from the 2D image directly
    base_x = [] # pixel index 
    base_y = [] # max eV for that pixel
    
    # x = pixel index of the parabola domain, base_x cropped
    # y = parabola fix for max eV over parabola domain
    parabola_x = [] 
    parabola_y = []

    # replace base_x and parabola_x
    base_angles = []
    parabola_angles = []

    # replace base_x and parabola_x
    base_kpara = []
    parabola_kpara = []
