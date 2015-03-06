from ij import IJ, WindowManager, ImagePlus, ImageStack
from ij.plugin import GaussianBlur3D, ImageCalculator, ZProjector
ImageCalculator
from script.imglib import ImgLib
from script.imglib.math import Compute, Divide, Multiply, Subtract


def getFimg(imp, Fst, Fen):
    
    proj = ZProjector(imp, startSlice=Fst, stopSlice=Fen)
    proj.setMethod(ZProjector.AVG_METHOD)
    proj.doProjection()
    imp_F = proj.getProjection()
    imp_F.setTitle("F")

    return imp_F


def getResponsePeriodMatrices(imp, imp_F, Rst, Ren):

    F = ImageStack(imp.width, imp.height)
    R = ImageStack(imp.width, imp.height)
    stack = imp.getImageStack()
    for n in range(Rst, Ren+1):
        F.addSlice(str(n-Ren), imp_F.getProcessor())
        ip = stack.getProcessor(n)
        fp = ip.toFloat(0, None)
        R.addSlice(str(n-Ren), fp)
    stack_F = ImgLib.wrap(ImagePlus("stack_F", F))
    stack_R = ImgLib.wrap(ImagePlus("stack_R", R))

    return stack_F, stack_R


def Viewer(imp, fname, Fst, Fen, Rst, Ren, dFoFmin, dFoFmax, NeedMovie=False):
    
    # sanity check
    nframes = imp.getNSlices()
    if nframes == 1: #should be a stack
        IJ.log('Not a valid stack!')
        return
    
    # close all previous results
    anat_name = 'Full frame average of ' + fname
    dFoF_name = 'dFoF map of ' + fname
    win_anat = WindowManager.getWindow(anat_name)
    win_dFoFavg = WindowManager.getWindow(dFoF_name)
    if win_anat:
        win_anat.close()
    if win_dFoFavg:
        win_dFoFavg.getImagePlus().close()

    # Getting F image as Imglib image
    img_F = getFimg(imp, Fst, Fen)

    ## 1: dF/F frame (single or frame averaged) on right
    # slice the Imglib image stack for the response period 
    stack_F, stack_R = getResponsePeriodMatrices(imp, img_F, Rst, Ren)
    # now compute raw dF/F in %
    dFoF = Compute.inFloats( Multiply(100.0, Divide( Subtract(stack_R, stack_F), stack_F) ) )
    # now take frame average
    proj_dFoFavg = ZProjector(ImgLib.wrap(dFoF), startSlice=1, stopSlice=Ren-Rst+1)
    proj_dFoFavg.setMethod(ZProjector.AVG_METHOD)
    proj_dFoFavg.doProjection()
    # 2D Gaussian Blur
    #ip_temp = ImagePlus(dFoF_name, proj_dFoFavg.getProjection().getImage()) # returns 8bit image
    imp_dFoFavg = proj_dFoFavg.getProjection() #32bit float
    IJ.run(imp_dFoFavg, "Gaussian Blur...", "sigma=1.2")
    imp_dFoFavg.setTitle(dFoF_name)
    imp_dFoFavg.show()
    # apply our color map and scale it to the user set range
    IJ.run(imp_dFoFavg, "clut2b", "")
    imp_dFoFavg.getProcessor().setMinAndMax(dFoFmin, dFoFmax)
    imp_dFoFavg.changes = False

    # 2: anatomy (all frame average) on left
    projAnat = ZProjector(imp, startSlice=1, stopSlice=nframes)
    projAnat.setMethod(ZProjector.AVG_METHOD)
    projAnat.doProjection()
    imp_Anat = projAnat.getProjection()
    imp_Anat.setTitle(anat_name)
    imp_Anat.show()
    IJ.run("Enhance Contrast", "saturated=0.35");

    # put two windows side by side
    target = WindowManager.getWindow(fname)
    pos = target.location()
    win_width = target.size.width
    Frame_anat = WindowManager.getWindow(anat_name)
    Frame_anat.setLocation(pos.x + 40, pos.y + 40)
    Frame_dFoF = WindowManager.getWindow(dFoF_name)
    Frame_dFoF.setLocation(pos.x + 40 + win_width, pos.y + 40)
    
    # 3 (optional) NeedMovie
    if NeedMovie:
        
        dFoFmovie_name = 'dFoF movie of ' + fname
        win_dFoFmovie = WindowManager.getWindow(dFoFmovie_name)
        if win_dFoFmovie:
            win_dFoFmovie.close()

        imp100 = IJ.createImage("x100", "8-bit", imp.width, imp.height, 1)
        ip = imp100.getProcessor()
        ip.set(100.0)

        # http://fiji.sc/Jython_Scripting  [Removing bleeding from one channel to another]
        calc = ImageCalculator()
        calc.calculate("Substract create 32-bit stack", imp, img_F)
        imp_dFoFmovie = WindowManager.getCurrentImage()
        calc.calculate("Divide stack", imp_dFoFmovie, img_F)
        calc.calculate("Multiply stack", imp_dFoFmovie, imp100)

        GB3 = GaussianBlur3D()
        GB3.blur(imp_dFoFmovie, 1.2, 1.2, 1.2)
        IJ.run(imp_dFoFmovie, "clut2b", "")
        
        imp_dFoFmovie.setTitle(dFoFmovie_name)
        Frame_movie = WindowManager.getWindow(dFoFmovie_name)
        Frame_movie.setLocation(pos.x + 40 + win_width*2, pos.y + 40)
        imp_dFoFmovie.show()


if __name__ == "__main__":
    imp = IJ.getImage()
    fname = imp.getTitle()
    Fst, Fen = 1, 100
    Rst, Ren = 460, 500
    dFoFmin, dFoFmax = -10, 40
    
    Viewer(imp, fname, Fst, Fen, Rst, Ren, dFoFmin, dFoFmax, 1)
    