v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 990 -670 990 -620 {lab=ibias}
N 990 -620 1250 -620 {lab=ibias}
N 1250 -670 1250 -620 {lab=ibias}
N 990 -700 1030 -700 {lab=ibias}
N 1030 -700 1030 -660 {lab=ibias}
N 990 -660 1030 -660 {lab=ibias}
N 1210 -700 1250 -700 {lab=ibias}
N 1210 -700 1210 -660 {lab=ibias}
N 1210 -660 1250 -660 {lab=ibias}
N 990 -1020 990 -990 {lab=vdd}
N 990 -1020 1250 -1020 {lab=vdd}
N 1250 -1020 1250 -990 {lab=vdd}
N 990 -960 1030 -960 {lab=vdd}
N 1030 -1010 1030 -960 {lab=vdd}
N 1030 -1020 1030 -1010 {lab=vdd}
N 1210 -960 1250 -960 {lab=vdd}
N 1210 -1020 1210 -960 {lab=vdd}
N 910 -960 950 -960 {lab=#net1}
N 910 -960 910 -910 {lab=#net1}
N 910 -910 990 -910 {lab=#net1}
N 1250 -910 1330 -910 {lab=#net2}
N 1330 -960 1330 -910 {lab=#net2}
N 1290 -960 1330 -960 {lab=#net2}
N 990 -930 990 -910 {lab=#net1}
N 990 -910 990 -860 {lab=#net1}
N 990 -800 990 -730 {lab=#net1}
N 1250 -930 1250 -910 {lab=#net2}
N 1120 -620 1120 -580 {lab=ibias}
N 850 -700 950 -700 {lab=vctrl}
N 1290 -700 1390 -700 {lab=vref}
N 1620 -1020 1620 -990 {lab=vdd}
N 1620 -960 1660 -960 {lab=vdd}
N 1660 -1020 1660 -960 {lab=vdd}
N 1620 -1020 1660 -1020 {lab=vdd}
N 990 -860 990 -800 {lab=#net1}
N 1250 -1020 1620 -1020 {lab=vdd}
N 1620 -810 1620 -740 {lab=ictrl}
N 1330 -960 1580 -960 {lab=#net2}
N 1620 -930 1620 -810 {lab=ictrl}
N 1250 -910 1250 -730 {lab=#net2}
C {symbols/nfet_03v3.sym} 970 -700 0 0 {name=M17
L=0.28u
W=2.5u
nf=5
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
C {symbols/nfet_03v3.sym} 1270 -700 0 1 {name=M18
L=0.28u
W=2.5u
nf=5
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
C {symbols/pfet_03v3.sym} 970 -960 0 0 {name=M19
L=0.5u
W=10u
nf=5
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
C {symbols/pfet_03v3.sym} 1270 -960 0 1 {name=M20
L=0.5u
W=10u
nf=5
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
C {symbols/pfet_03v3.sym} 1600 -960 0 0 {name=M21
L=0.5u
W=20u
nf=5
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
C {iopin.sym} 1120 -1020 3 0 {name=p1 lab=vdd}
C {iopin.sym} 1120 -580 0 0 {name=p2 lab=ibias}
C {ipin.sym} 1390 -700 0 1 {name=p3 lab=vref}
C {ipin.sym} 850 -700 2 1 {name=p4 lab=vctrl}
C {opin.sym} 1620 -740 1 0 {name=p5 lab=ictrl}
C {title.sym} 550 -240 0 0 {name=l1 author="Silicon souls"}
