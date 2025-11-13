from MaxCaptureAngle import *

print("Plotting Max Angle")

ExtractData("RaytracingResults/MaxCaptureAngle", ["MothEye", "Regular"])
PlotMaxCaptureAngle("RaytracingResults/MaxCaptureAngle", "MothEye")
PlotMaxCaptureAngle("RaytracingResults/MaxCaptureAngle", "Regular")
PlotMaxCaptureAngleComparison("RaytracingResults/MaxCaptureAngle", "MothEye", "Regular")
PlotMaxCaptureAngleFullComparison("RaytracingResults/MaxCaptureAngle", "MothEye", "Regular")

print("Finished Plotting Max Angle")

from InternalReflectionsWaves import *
print("Plotting Wave Internal Reflection")
ExtractData("RaytracingResults/InternalReflectionsWaves", ["Cone", "QD"])
PlotInternalReflections("RaytracingResults/InternalReflectionsWaves", "Cone")
PlotInternalReflections("RaytracingResults/InternalReflectionsWaves", "QD")
PlotInternalReflectionsComparison("RaytracingResults/InternalReflectionsWaves", "QD", "Cone")

print("Finished Plotting Wave Internal Reflection")

from RealLifeResults import *
print("Plotting Real Life Results")
ExtractData("RaytracingResults/RealLifeResults", ["Angle0", "Angle26"])
PlotInternalReflections("RaytracingResults/RealLifeResults", "Angle0")
PlotInternalReflections("RaytracingResults/RealLifeResults", "Angle26")

print("Finished Plotting Real Life Results")

from InternalReflectionsWaveguides import *
print("Plotting Internal Reflection Waveguides")

paths = ["Cone_Large_Regular", "Cone_Large_MothEye", "Cone_UnitCell_Regular", "Cone_UnitCell_MothEye", "QD_Large_Regular", "QD_Large_MothEye", "QD_UnitCell_Regular", "QD_UnitCell_MothEye"]

ExtractData("RaytracingResults/InternalReflections", ["Cone_Large_Regular", "Cone_Large_MothEye", "Cone_UnitCell_Regular", "Cone_UnitCell_MothEye", "QD_Large_Regular", "QD_Large_MothEye", "QD_UnitCell_Regular", "QD_UnitCell_MothEye"])

for path in paths:
    PlotInternalReflections("RaytracingResults/InternalReflections", path)
    
print("Finished Plotting Internal Reflection Waveguides")
