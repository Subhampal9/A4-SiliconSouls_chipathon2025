v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 1140 -1010 1580 -1010 {lab=#net1}
N 1580 -1010 1580 -920 {lab=#net1}
N 1140 -1010 1140 -920 {lab=#net1}
N 630 -1030 680 -1030 {lab=vref}
N 630 -990 680 -990 {lab=vctrl}
N 750 -1120 750 -1060 {lab=vdd}
N 750 -1120 1060 -1120 {lab=vdd}
N 1060 -1120 1060 -920 {lab=vdd}
N 1120 -1120 1500 -1120 {lab=vdd}
N 1500 -1120 1500 -920 {lab=vdd}
N 1100 -780 1100 -740 {lab=vss}
N 1360 -740 1540 -740 {lab=vss}
N 1540 -780 1540 -740 {lab=vss}
N 1290 -880 1390 -880 {lab=v1-}
N 1330 -820 1390 -820 {lab=v1+}
N 900 -820 900 -760 {lab=v2-}
N 900 -820 950 -820 {lab=v2-}
N 900 -960 900 -880 {lab=v2+}
N 900 -880 950 -880 {lab=v2+}
N 1290 -880 1290 -640 {lab=v1-}
N 1330 -820 1330 -640 {lab=v1+}
N 1690 -880 1850 -880 {lab=v2-}
N 1850 -760 1850 -640 {lab=v2-}
N 900 -760 1850 -760 {lab=v2-}
N 1890 -820 1890 -640 {lab=v2+}
N 900 -960 1890 -960 {lab=v2+}
N 1690 -820 1890 -820 {lab=v2+}
N 1160 -490 1250 -490 {lab=vss}
N 1370 -490 1460 -490 {lab=vdd}
N 1720 -490 1810 -490 {lab=vss}
N 1930 -490 2020 -490 {lab=vdd}
N 1290 -340 1290 -300 {lab=vout0}
N 1330 -340 1330 -300 {lab=vout180}
N 1850 -340 1850 -300 {lab=vout90}
N 1890 -340 1890 -300 {lab=vout270}
N 910 -1100 910 -1060 {lab=ibias}
N 400 -550 400 -520 {lab=GND}
N 520 -520 580 -520 {lab=GND}
N 580 -550 580 -520 {lab=GND}
N 460 -550 460 -520 {lab=GND}
N 520 -550 520 -520 {lab=GND}
N 400 -650 400 -610 {lab=vdd}
N 460 -650 460 -610 {lab=vss}
N 520 -650 520 -610 {lab=vref}
N 580 -650 580 -610 {lab=ibias}
N 610 -390 610 -360 {lab=GND}
N 610 -500 610 -450 {lab=vctrl}
N 1060 -1120 1120 -1120 {lab=vdd}
N 1100 -740 1360 -740 {lab=vss}
N 460 -520 490 -520 {lab=GND}
N 980 -1010 1140 -1010 {lab=#net1}
N 1250 -880 1290 -880 {lab=v1-}
N 1250 -820 1330 -820 {lab=v1+}
N 1850 -880 1850 -760 {lab=v2-}
N 1890 -960 1890 -820 {lab=v2+}
N 400 -520 460 -520 {lab=GND}
N 490 -520 520 -520 {lab=GND}
C {single_delay.sym} 970 -900 0 0 {name=xdelay1}
C {single_delay.sym} 1410 -900 0 0 {name=xdelay2}
C {V2I.sym} 700 -1040 0 0 {name=xv2i}
C {opbuffer.sym} 1870 -490 1 0 {name=xbuffer2}
C {lab_pin.sym} 1120 -1120 1 0 {name=p10 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1460 -490 1 0 {name=p11 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 2020 -490 1 0 {name=p12 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1360 -740 3 0 {name=p13 sig_type=std_logic lab=vss}
C {lab_pin.sym} 1160 -490 1 0 {name=p14 sig_type=std_logic lab=vss}
C {lab_pin.sym} 1720 -490 1 0 {name=p15 sig_type=std_logic lab=vss}
C {lab_pin.sym} 630 -1030 0 0 {name=p16 sig_type=std_logic lab=vref}
C {lab_pin.sym} 630 -990 0 0 {name=p17 sig_type=std_logic lab=vctrl}
C {lab_pin.sym} 1330 -300 3 0 {name=p18 sig_type=std_logic lab=vout180}
C {lab_pin.sym} 1290 -300 3 0 {name=p19 sig_type=std_logic lab=vout0}
C {lab_pin.sym} 1850 -300 3 0 {name=p20 sig_type=std_logic lab=vout90}
C {lab_pin.sym} 1890 -300 3 0 {name=p21 sig_type=std_logic lab=vout270}
C {title.sym} 410 -150 0 0 {name=l1 author="Silicon Souls"}
C {lab_pin.sym} 910 -1100 2 0 {name=p22 sig_type=std_logic lab=ibias}
C {vsource.sym} 400 -580 0 0 {name=V1 value=3.3 savecurrent=false}
C {vsource.sym} 460 -580 0 0 {name=V2 value=0 savecurrent=false}
C {vsource.sym} 520 -580 0 0 {name=V3 value=1.65 savecurrent=false}
C {isource.sym} 580 -580 0 0 {name=I0 value=500u}
C {gnd.sym} 490 -520 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 400 -650 1 0 {name=p1 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 460 -650 1 0 {name=p2 sig_type=std_logic lab=vss}
C {lab_pin.sym} 520 -650 1 0 {name=p3 sig_type=std_logic lab=vref}
C {lab_pin.sym} 580 -650 1 0 {name=p4 sig_type=std_logic lab=ibias}
C {vsource.sym} 610 -420 0 0 {name=V4 value=0.5 savecurrent=false}
C {gnd.sym} 610 -360 0 0 {name=l3 lab=GND}
C {lab_pin.sym} 610 -500 0 1 {name=p5 sig_type=std_logic lab=vctrl}
C {opbuffer.sym} 1310 -490 1 0 {name=xbuffer1}
C {lab_pin.sym} 1320 -880 1 0 {name=p6 sig_type=std_logic lab=v1-}
C {lab_pin.sym} 1350 -820 1 0 {name=p7 sig_type=std_logic lab=v1+}
C {lab_pin.sym} 1760 -880 1 0 {name=p8 sig_type=std_logic lab=v2-}
C {lab_pin.sym} 1760 -820 1 0 {name=p9 sig_type=std_logic lab=v2+}
C {capa.sym} 1260 -300 1 0 {name=C7
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1230 -300 1 0 {name=l21 lab=GND}
C {capa.sym} 1820 -300 1 0 {name=C1
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1790 -300 1 0 {name=l4 lab=GND}
C {capa.sym} 1920 -300 3 1 {name=C2
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1950 -300 3 1 {name=l5 lab=GND}
C {capa.sym} 1360 -300 3 1 {name=C3
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1390 -300 3 1 {name=l6 lab=GND}
C {devices/code_shown.sym} 2790 -620 0 0 {name=NGSPICE only_toplevel=true
value="
.control
let start_v = 0.5
let stop_v  = 3.3
let step_v  = 0.05

let vctrl = start_v

let v_sweep = unitvec(57)
let power_results = unitvec(57)
let i = 0

dowhile vctrl <= stop_v
	alter @V4[DC] = vctrl
	tran 10p 50n
	meas tran irms RMS v(v1#branch) from=40n to=50n
	let power_rms = irms * 3.3
	let v_sweep[i] = "$&vctrl"
	let power_results[i] = power_rms
	print power_rms
	let vctrl = vctrl + step_v
	let i = i + 1
	reset
end
set nolegend
print power_results
set filetype=ascii
write /foss/designs/vco_des/xschem/power.txt power_results
.endc
"}
C {devices/code_shown.sym} 2170 -300 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include $::180MCU_MODELS/design.ngspice
.lib $::180MCU_MODELS/sm141064.ngspice typical
.lib $::180MCU_MODELS/sm141064.ngspice cap_mim
.lib $::180MCU_MODELS/sm141064.ngspice res_typical
.lib $::180MCU_MODELS/sm141064.ngspice mimcap_typical
"}
