v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 1130 -1080 1570 -1080 {lab=#net1}
N 1570 -1080 1570 -990 {lab=#net1}
N 1130 -1080 1130 -990 {lab=#net1}
N 620 -1100 670 -1100 {lab=vref}
N 620 -1060 670 -1060 {lab=vctrl}
N 740 -1190 740 -1130 {lab=vdd}
N 740 -1190 1050 -1190 {lab=vdd}
N 1050 -1190 1050 -990 {lab=vdd}
N 1110 -1190 1490 -1190 {lab=vdd}
N 1490 -1190 1490 -990 {lab=vdd}
N 1090 -850 1090 -810 {lab=vss}
N 1350 -810 1530 -810 {lab=vss}
N 1530 -850 1530 -810 {lab=vss}
N 1280 -950 1380 -950 {lab=v1-}
N 1320 -890 1380 -890 {lab=v1+}
N 890 -890 890 -830 {lab=v2-}
N 890 -890 940 -890 {lab=v2-}
N 890 -1030 890 -950 {lab=v2+}
N 890 -950 940 -950 {lab=v2+}
N 1280 -950 1280 -710 {lab=v1-}
N 1320 -890 1320 -710 {lab=v1+}
N 1680 -950 1840 -950 {lab=v2-}
N 1840 -830 1840 -710 {lab=v2-}
N 890 -830 1840 -830 {lab=v2-}
N 1880 -890 1880 -710 {lab=v2+}
N 890 -1030 1880 -1030 {lab=v2+}
N 1680 -890 1880 -890 {lab=v2+}
N 1150 -560 1240 -560 {lab=vss}
N 1360 -560 1450 -560 {lab=vdd}
N 1710 -560 1800 -560 {lab=vss}
N 1920 -560 2010 -560 {lab=vdd}
N 1280 -410 1280 -370 {lab=vout0}
N 1320 -410 1320 -370 {lab=vout180}
N 1840 -410 1840 -370 {lab=vout90}
N 1880 -410 1880 -370 {lab=vout270}
N 900 -1170 900 -1130 {lab=ibias}
N 390 -620 390 -590 {lab=GND}
N 510 -590 570 -590 {lab=GND}
N 570 -620 570 -590 {lab=GND}
N 450 -620 450 -590 {lab=GND}
N 510 -620 510 -590 {lab=GND}
N 390 -720 390 -680 {lab=vdd}
N 450 -720 450 -680 {lab=vss}
N 510 -720 510 -680 {lab=vref}
N 570 -720 570 -680 {lab=ibias}
N 600 -460 600 -430 {lab=GND}
N 600 -570 600 -520 {lab=vctrl}
N 1050 -1190 1110 -1190 {lab=vdd}
N 1090 -810 1350 -810 {lab=vss}
N 450 -590 480 -590 {lab=GND}
N 970 -1080 1130 -1080 {lab=#net1}
N 1240 -950 1280 -950 {lab=v1-}
N 1240 -890 1320 -890 {lab=v1+}
N 1840 -950 1840 -830 {lab=v2-}
N 1880 -1030 1880 -890 {lab=v2+}
N 390 -590 450 -590 {lab=GND}
N 480 -590 510 -590 {lab=GND}
C {single_delay.sym} 960 -970 0 0 {name=xdelay1}
C {single_delay.sym} 1400 -970 0 0 {name=xdelay2}
C {V2I.sym} 690 -1110 0 0 {name=xv2i}
C {opbuffer.sym} 1860 -560 1 0 {name=xbuffer2}
C {lab_pin.sym} 1110 -1190 1 0 {name=p10 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1450 -560 1 0 {name=p11 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 2010 -560 1 0 {name=p12 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1350 -810 3 0 {name=p13 sig_type=std_logic lab=vss}
C {lab_pin.sym} 1150 -560 1 0 {name=p14 sig_type=std_logic lab=vss}
C {lab_pin.sym} 1710 -560 1 0 {name=p15 sig_type=std_logic lab=vss}
C {lab_pin.sym} 620 -1100 0 0 {name=p16 sig_type=std_logic lab=vref}
C {lab_pin.sym} 620 -1060 0 0 {name=p17 sig_type=std_logic lab=vctrl}
C {lab_pin.sym} 1320 -370 3 0 {name=p18 sig_type=std_logic lab=vout180}
C {lab_pin.sym} 1280 -370 3 0 {name=p19 sig_type=std_logic lab=vout0}
C {lab_pin.sym} 1840 -370 3 0 {name=p20 sig_type=std_logic lab=vout90}
C {lab_pin.sym} 1880 -370 3 0 {name=p21 sig_type=std_logic lab=vout270}
C {title.sym} 400 -220 0 0 {name=l1 author="Silicon Souls"}
C {lab_pin.sym} 900 -1170 2 0 {name=p22 sig_type=std_logic lab=ibias}
C {vsource.sym} 390 -650 0 0 {name=V1 value=3.3 savecurrent=false}
C {vsource.sym} 450 -650 0 0 {name=V2 value=0 savecurrent=false}
C {vsource.sym} 510 -650 0 0 {name=V3 value=1.65 savecurrent=false}
C {isource.sym} 570 -650 0 0 {name=I0 value=500u}
C {gnd.sym} 480 -590 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 390 -720 1 0 {name=p1 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 450 -720 1 0 {name=p2 sig_type=std_logic lab=vss}
C {lab_pin.sym} 510 -720 1 0 {name=p3 sig_type=std_logic lab=vref}
C {lab_pin.sym} 570 -720 1 0 {name=p4 sig_type=std_logic lab=ibias}
C {vsource.sym} 600 -490 0 0 {name=V4 value=3.3 savecurrent=false}
C {gnd.sym} 600 -430 0 0 {name=l3 lab=GND}
C {lab_pin.sym} 600 -570 0 1 {name=p5 sig_type=std_logic lab=vctrl}
C {devices/code_shown.sym} 2270 -610 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice res_typical
"}
C {devices/code_shown.sym} 2890 -760 0 0 {name=NGSPICE only_toplevel=true
value="
.control
let start_v = 0.5
let stop_v  = 3.3
let step_v  = 0.05

let vctrl = start_v

let v_sweep = unitvec(57)
let freq_results = unitvec(57)
let i = 0

dowhile vctrl <= stop_v
	alter @V4[DC] = vctrl
	tran 10p 50n
	meas tran t1 WHEN v(vout0)=1.65 FALL=10
	meas tran t2 WHEN v(vout0)=1.65 FALL=11
	let freq = 1 / (t2 - t1)
	let v_sweep[i] = "$&vctrl"
	let freq_results[i] = freq
	print freq
	let vctrl = vctrl + step_v
	let i = i + 1
	reset
end
set nolegend
print freq_results 
.endc
"}
C {opbuffer.sym} 1300 -560 1 0 {name=xbuffer1}
C {lab_pin.sym} 1310 -950 1 0 {name=p6 sig_type=std_logic lab=v1-}
C {lab_pin.sym} 1340 -890 1 0 {name=p7 sig_type=std_logic lab=v1+}
C {lab_pin.sym} 1750 -950 1 0 {name=p8 sig_type=std_logic lab=v2-}
C {lab_pin.sym} 1750 -890 1 0 {name=p9 sig_type=std_logic lab=v2+}
C {capa.sym} 1250 -370 1 0 {name=C7
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1220 -370 1 0 {name=l21 lab=GND}
C {capa.sym} 1810 -370 1 0 {name=C1
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1780 -370 1 0 {name=l4 lab=GND}
C {capa.sym} 1910 -370 3 1 {name=C2
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1940 -370 3 1 {name=l5 lab=GND}
C {capa.sym} 1350 -370 3 1 {name=C3
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1380 -370 3 1 {name=l6 lab=GND}
