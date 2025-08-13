v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
P 4 1 1290 -640 {}
N 680 -910 730 -910 {lab=vi+}
N 680 -910 680 -730 {lab=vi+}
N 680 -730 730 -730 {lab=vi+}
N 1530 -910 1580 -910 {lab=vi-}
N 1580 -910 1580 -730 {lab=vi-}
N 1530 -730 1580 -730 {lab=vi-}
N 770 -880 770 -760 {lab=vo-}
N 1490 -880 1490 -760 {lab=vo+}
N 770 -980 770 -940 {lab=ictrl}
N 990 -980 990 -940 {lab=ictrl}
N 1270 -980 1270 -940 {lab=ictrl}
N 770 -980 990 -980 {lab=ictrl}
N 990 -980 1270 -980 {lab=ictrl}
N 1270 -980 1490 -980 {lab=ictrl}
N 1490 -980 1490 -940 {lab=ictrl}
N 1490 -700 1490 -660 {lab=vss}
N 1270 -700 1270 -660 {lab=vss}
N 990 -700 990 -660 {lab=vss}
N 1270 -660 1490 -660 {lab=vss}
N 990 -660 1270 -660 {lab=vss}
N 770 -660 990 -660 {lab=vss}
N 770 -700 770 -660 {lab=vss}
N 830 -880 990 -880 {lab=vo-}
N 830 -880 830 -860 {lab=vo-}
N 770 -860 830 -860 {lab=vo-}
N 1270 -880 1430 -880 {lab=vo+}
N 1430 -880 1430 -860 {lab=vo+}
N 1430 -860 1490 -860 {lab=vo+}
N 1270 -760 1430 -760 {lab=vo+}
N 1430 -780 1430 -760 {lab=vo+}
N 1430 -780 1490 -780 {lab=vo+}
N 830 -760 990 -760 {lab=vo-}
N 830 -780 830 -760 {lab=vo-}
N 770 -780 830 -780 {lab=vo-}
N 1030 -910 1080 -910 {lab=vo+}
N 1080 -910 1170 -840 {lab=vo+}
N 1170 -840 1490 -840 {lab=vo+}
N 1180 -910 1230 -910 {lab=vo-}
N 1080 -840 1180 -910 {lab=vo-}
N 770 -840 1080 -840 {lab=vo-}
N 1030 -730 1080 -730 {lab=vo+}
N 1080 -730 1170 -800 {lab=vo+}
N 1170 -800 1490 -800 {lab=vo+}
N 1170 -730 1230 -730 {lab=vo-}
N 1090 -800 1170 -730 {lab=vo-}
N 770 -800 1090 -800 {lab=vo-}
N 1110 -1040 1110 -980 {lab=ictrl}
N 1270 -910 1310 -910 {lab=vdd}
N 1450 -910 1490 -910 {lab=vdd}
N 940 -910 990 -910 {lab=vdd}
N 770 -910 820 -910 {lab=vdd}
N 770 -730 820 -730 {lab=vss}
N 820 -730 820 -660 {lab=vss}
N 940 -730 990 -730 {lab=vss}
N 940 -730 940 -660 {lab=vss}
N 1300 -730 1300 -660 {lab=vss}
N 1450 -730 1490 -730 {lab=vss}
N 1450 -730 1450 -660 {lab=vss}
N 1270 -730 1300 -730 {lab=vss}
N 1490 -820 1690 -820 {lab=vo+}
N 570 -820 770 -820 {lab=vo-}
C {title.sym} 380 -270 0 0 {name=l2 author="Silicon Souls"}
C {symbols/pfet_03v3.sym} 750 -910 0 0 {name=M1
L=0.28u
W=6.48u
nf=2
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {symbols/pfet_03v3.sym} 1010 -910 0 1 {name=M2
L=0.28u
W=4.32u
nf=2
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {symbols/pfet_03v3.sym} 1250 -910 0 0 {name=M3
L=0.28u
W=4.32u
nf=2
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {symbols/pfet_03v3.sym} 1510 -910 0 1 {name=M4
L=0.28u
W=6.48u
nf=2
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} 750 -730 0 0 {name=M5
L=0.28u
W=2.16u
nf=2
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} 1010 -730 0 1 {name=M6
L=0.28u
W=1.44u
nf=2
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} 1250 -730 0 0 {name=M7
L=0.28u
W=1.44u
nf=2
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} 1510 -730 0 1 {name=M8
L=0.28u
W=2.16u
nf=2
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {lab_pin.sym} 820 -910 2 0 {name=p17 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 940 -910 2 1 {name=p18 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1450 -910 2 1 {name=p19 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1310 -910 2 0 {name=p20 sig_type=std_logic lab=vdd}
C {iopin.sym} 1110 -1040 3 0 {name=p1 lab=ictrl}
C {iopin.sym} 1120 -660 1 0 {name=p2 lab=vss}
C {iopin.sym} 380 -970 0 0 {name=p3 lab=vdd}
C {ipin.sym} 680 -870 0 0 {name=p4 lab=vi+}
C {ipin.sym} 1580 -870 0 1 {name=p5 lab=vi-}
C {opin.sym} 570 -820 2 0 {name=p6 lab=vo-}
C {opin.sym} 1690 -820 2 1 {name=p7 lab=vo+}
