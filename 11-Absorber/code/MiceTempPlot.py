import libMausCpp
import random
import ROOT
import os
import datetime
from ROOT import *
import numpy as np
from array import array

n = 935
filename = "TempValuesPlot.dat"

resolution = 0.1
Pressure_sensor = 0.014
Sensor_accuracy = 0.009
Sensor_stability = 0.012
Sensor_magnetic = 0.008
Cal_Temp = 20.0
Boil_Temp = 21.692
No_sensors = 8.0

#Program

phase_one = array("d")
phase_two = array("d")
phase_three = array("d")
phase_four = array("d")
phase_five = array("d")
phase_six = array("d")
phase_seven = array("d")
phase_eight = array("d")

phase_mean = array("d")
phase_error = array("d")
phase_pressure = array("d")

Z = array("d")

other_error = ((No_sensors * (((((resolution/Cal_Temp) ** 2.0 + (Pressure_sensor/Boil_Temp) ** 2.0 + (((2 * (resolution ** 2.0)) ** 0.5)/Cal_Temp) ** 2.0) ** 0.5) * Cal_Temp) **2.0 + (Sensor_magnetic) ** 2.0 + (Sensor_stability) ** 2.0 + (Sensor_accuracy) ** 2.0)) ** 0.5)/No_sensors

input_file = open(filename,'r')
for i in range(n):
    phase_vector = input_file.readline()
    phase_vector = phase_vector[phase_vector.find('[')+1: phase_vector.find(']')]
    phase_vector = [float(x) for x in phase_vector.split('\t') if x]
    phase_one.append(phase_vector[0])
    phase_two.append(phase_vector[1])
    phase_three.append(phase_vector[2])
    phase_four.append(phase_vector[3])
    phase_five.append(phase_vector[4])
    phase_six.append(phase_vector[5])
    phase_seven.append(phase_vector[6])
    phase_eight.append(phase_vector[7])
    Z.append(float(i))
    phase_pressure.append(phase_vector[9])

    phase_mean.append((phase_vector[0] + phase_vector[1] + phase_vector[2] + phase_vector[3] + phase_vector[4] + phase_vector[5] + phase_vector[6] + phase_vector[7])/8.0)
    phase_error.append((((np.std([phase_vector[0], phase_vector[1], phase_vector[2], phase_vector[3], phase_vector[4], phase_vector[5], phase_vector[6], phase_vector[7]]))/No_sensors) ** 2.0 + other_error ** 2.0) ** 0.5)
    #phase_error.append(0.07)

c1 = TCanvas("c1", " ", 900, 600)

ex = array("d")
ey = array("d")
ex1 = array("d")
ey1 = array("d")
for i in range(n):
    ex.append(1.0)
    ey.append(0.2)
    ex1.append(1.0)
    ey1.append(0.005)
da = array("d")
start_time = TDatime(2017,9,19,00,00,00)
new = start_time.Convert()
end_time = TDatime(2017,10,28,00,00,00)
end = end_time.Convert()
new = 0
for i in range(n):
    da.append(new + i * 60 * 60)

gr1 = TGraphErrors(n, da, phase_one, ex1, ey1)
gr2 = TGraphErrors(n, da, phase_two, ex1, ey1)
gr3 = TGraphErrors(n, da, phase_three, ex1, ey1)
gr4 = TGraphErrors(n, da, phase_four, ex1, ey1)
gr5 = TGraphErrors(n, da, phase_five, ex1, ey1)
gr6 = TGraphErrors(n, da, phase_six, ex1, ey1)
gr7 = TGraphErrors(n, da, phase_seven, ex1, ey1)
gr8 = TGraphErrors(n, da, phase_eight, ex1, ey1)

gr1.SetFillColor(kGray+1)
gr1.SetFillStyle(1001)
gr2.SetFillColor(kGreen+1)
gr2.SetFillStyle(1001)
gr3.SetFillColor(kRed)
gr3.SetFillStyle(1001)
gr4.SetFillColor(kAzure+7)
gr4.SetFillStyle(1001)
gr5.SetFillColor(kGray+2)
gr5.SetFillStyle(1001)
gr6.SetFillColor(kGreen+2)
gr6.SetFillStyle(1001)
gr7.SetFillColor(kRed+1)
gr7.SetFillStyle(1001)
gr8.SetFillColor(kAzure+8)
gr8.SetFillStyle(1001)
mg = TMultiGraph()
mg.Add(gr1)
mg.Add(gr2)
mg.Add(gr3)
mg.Add(gr4)
mg.Add(gr5)
mg.Add(gr6)
mg.Add(gr7)
mg.Add(gr8)
mg.Draw("a3")
mg.GetYaxis().SetRangeUser(20.3, 21.3)
mg.GetXaxis().SetLimits(-100000, 2400000)
mg.GetXaxis().SetTimeDisplay(1)
mg.GetXaxis().SetTimeFormat("%d/%m/%Y%F2017-09-19 00:00:00")
mg.GetYaxis().SetTitle("Temperature (K)")
#mg.GetXaxis().SetTitle("Time (days)")
mg.GetHistogram().SetTitle("Liquid Hydrogen Temperature during liquefaction and steady-state")
mg.Draw("a3")
c1.Update()

legend2 = TLegend(0.8,0.55,0.9,0.9)
legend2.AddEntry(gr1, "LSA", "f")
legend2.AddEntry(gr5, "TSA", "f")
legend2.AddEntry(gr2, "LSB", "f")
legend2.AddEntry(gr6, "TSB", "f")
legend2.AddEntry(gr3, "LSD", "f")
legend2.AddEntry(gr7, "TSD", "f")
legend2.AddEntry(gr4, "LSE", "f")
legend2.AddEntry(gr8, "TSE", "f")
legend2.Draw()


ita = 1
itb = 672

da2 = array("d")
phase_mean2 = array("d")
ex12 = array("d")
ey12 = array("d")
ex2 = array("d")
phase_error2 = array("d")
phase_pressure2 = array("d")

for i in range(ita,itb):
    da2.append(da[i])
    phase_mean2.append(phase_mean[i])
    ex12.append(ex1[i])
    ey12.append(ey1[i])
    ex2.append(ex[i])
    phase_error2.append(phase_error[i])
    phase_pressure2.append(phase_pressure[i])

n = itb - ita
c2 = TCanvas("c2", " ", 900, 600)
grs = TGraphErrors(n, da2, phase_mean2, ex12, ey12)
grs.SetFillColor(2)
grs.SetFillStyle(1001)

grs2 = TGraphErrors(n, da2, phase_mean2, ex2, phase_error2)
grs2.SetFillColor(2)
grs2.SetFillStyle(3001)

grs3 = TGraphErrors(n, da2, phase_pressure2, ex12, ey12)
grs3.SetFillColor(1)
grs3.SetFillStyle(1001)


mg2 = TMultiGraph()
mg2.Add(grs2)
mg2.Add(grs)
mg2.Add(grs3)
mg2.Draw("a3")
mg2.GetYaxis().SetRangeUser(20.3, 21.3)
mg2.GetXaxis().SetTimeDisplay(1)
mg2.GetXaxis().SetTimeFormat("%d/%m/%Y%F2017-09-19 00:00:00")
mg2.GetYaxis().SetTitle("Temperature (K)")
#mg2.GetXaxis().SetTitle("Time (days)")
mg2.GetHistogram().SetTitle("Liquid Hydrogen Temperature during liquefaction and steady-state")
mg2.Draw("a3")
c2.Update()

legend1 = TLegend(0.55,0.75,0.9,0.9)
legend1.AddEntry(grs, "Corrected temperature", "f")
legend1.AddEntry(grs2, "Corrected temperature error", "f")
legend1.AddEntry(grs3, "Boiling temperature at that pressure", "f")
legend1.Draw()
c2.Update()

ita = 168
itb = 648

da3 = array("d")
phase_mean3 = array("d")
ex13 = array("d")
ey13 = array("d")
ex3 = array("d")
phase_error3 = array("d")
phase_pressure3 = array("d")

for i in range(ita,itb):
    da3.append(da[i])
    phase_mean3.append(phase_mean[i])
    ex13.append(ex1[i])
    ey13.append(ey1[i])
    ex3.append(ex[i])
    phase_error3.append(phase_error[i])
    phase_pressure3.append(phase_pressure[i])

n = itb - ita
c3 = TCanvas("c3", " ", 900, 600)
grs4 = TGraphErrors(n, da3, phase_mean3, ex13, ey13)
grs4.SetFillColor(2)
grs4.SetFillStyle(1001)

grs5 = TGraphErrors(n, da3, phase_mean3, ex3, phase_error3)
grs5.SetFillColor(2)
grs5.SetFillStyle(3001)

grs6 = TGraphErrors(n, da3, phase_pressure3, ex13, ey13)
grs6.SetFillColor(1)
grs6.SetFillStyle(1001)



mg3 = TMultiGraph()
mg3.Add(grs5)
mg3.Add(grs4)
mg3.Add(grs6)
mg3.Draw("a3")
mg3.GetYaxis().SetRangeUser(20.3, 20.9)
mg3.GetXaxis().SetTimeDisplay(1)
mg3.GetXaxis().SetTimeFormat("%d/%m/%Y%F2017-09-19 00:00:00")#("%d\/%m%F2017-09-19 00:00:00")
mg3.GetXaxis().SetNdivisions(5,kFALSE)
mg3.GetYaxis().SetTitle("Temperature (K)")
#mg3.GetXaxis().SetTitle("Time (days)")
mg3.GetHistogram().SetTitle("Liquid Hydrogen Temperature during steady-state")
mg3.Draw("a3")
c3.Update()

legend = TLegend(0.55,0.75,0.9,0.9)
legend.AddEntry(grs4, "Corrected temperature", "f")
legend.AddEntry(grs5, "Corrected temperature error", "f")
legend.AddEntry(grs6, "Boiling temperature at that pressure", "f")
legend.Draw()

c3.SaveAs("LH2_temperature_calibrated_steady.pdf")
c3.SaveAs("LH2_temperature_calibrated_steady.png")

raw_input("Enter Sandman")
