from MaxCaptureAngle import *
from InternalReflectionsWaves import *

PlotMaxCaptureAngle("RaytracingResults/MaxCaptureAngle", "MothEye")
PlotMaxCaptureAngle("RaytracingResults/MaxCaptureAngle", "Regular")

PlotMaxCaptureAngleComparison("RaytracingResults/MaxCaptureAngle", "MothEye", "Regular")
PlotMaxCaptureAngleFullComparison("RaytracingResults/MaxCaptureAngle", "MothEye", "Regular")

PlotInternalReflections("RaytracingResults/InternalReflectionsWaves", "Cone")
PlotInternalReflections("RaytracingResults/InternalReflectionsWaves", "QD")
PlotInternalReflectionsComparison("RaytracingResults/InternalReflectionsWaves", "QD", "Cone")