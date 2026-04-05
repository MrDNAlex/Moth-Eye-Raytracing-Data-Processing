from MaxCaptureAngle import *

print("Plotting Max Angle")

ExtractData("Initial-Raytracing/MaxCaptureAngle", ["MothEye", "Regular"])
PlotMaxCaptureAngle("Initial-Raytracing/MaxCaptureAngle", "MothEye")
PlotMaxCaptureAngle("Initial-Raytracing/MaxCaptureAngle", "Regular")
PlotMaxCaptureAngleComparison("Initial-Raytracing/MaxCaptureAngle", "MothEye", "Regular")
PlotMaxCaptureAngleFullComparison("Initial-Raytracing/MaxCaptureAngle", "MothEye", "Regular")
PlotMaxCaptureAngleFullComparisonLinear("Initial-Raytracing/MaxCaptureAngle", "MothEye", "Regular")
PlotMaxCaptureAngleFullComparisonApproximated("Initial-Raytracing/MaxCaptureAngle", "MothEye", "Regular")

print("Finished Plotting Max Angle")

from InternalReflectionsWaves import *
print("Plotting Wave Internal Reflection")
ExtractData("Initial-Raytracing/InternalReflectionsWaves", ["Cone", "QD"])
PlotInternalReflections("Initial-Raytracing/InternalReflectionsWaves", "Cone")
PlotInternalReflections("Initial-Raytracing/InternalReflectionsWaves", "QD")
PlotInternalReflectionsComparison("Initial-Raytracing/InternalReflectionsWaves", "QD", "Cone")

print("Finished Plotting Wave Internal Reflection")

from RealLifeResults import *
print("Plotting Real Life Results")
ExtractData("Initial-Raytracing/RealLifeResults", ["Angle0", "Angle26"])
PlotInternalReflections("Initial-Raytracing/RealLifeResults", "Angle0")
PlotInternalReflections("Initial-Raytracing/RealLifeResults", "Angle26")

print("Finished Plotting Real Life Results")

from InternalReflectionsWaveguides import *
print("Plotting Internal Reflection Waveguides")

paths = {
    "Cone_Large_Regular" : "Cone QD and Linear GRIN\n(Isolated Device-Scale Structure)",
    "Cone_Large_MothEye": "Cone QD and Approximated GRIN\n(Isolated Device-Scale Structure)",
    "Cone_UnitCell_Regular": "Cone QD and Linear GRIN\n(Single Repeating Unit Cell)",
    "Cone_UnitCell_MothEye": "Cone QD and Approximated GRIN\n(Single Repeating Unit Cell)",
    "QD_Large_Regular" : "Circular QD and Linear GRIN\n(Isolated Device-Scale Structure)",
    "QD_Large_MothEye": "Circular QD and Approximated GRIN\n(Isolated Device-Scale Structure)",
    "QD_UnitCell_Regular": "Circular QD and Linear GRIN\n(Single Repeating Unit Cell)",
    "QD_UnitCell_MothEye": "Circular QD and Approximated GRIN\n(Single Repeating Unit Cell)",
}

ExtractData("Initial-Raytracing/InternalReflections", list(paths.keys()))

for path in paths.keys():
    PlotInternalReflections("Initial-Raytracing/InternalReflections", path)
    
print("Finished Plotting Internal Reflection Waveguides")
