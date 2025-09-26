from glayout.pdk.mappedpdk import MappedPDK
from glayout.pdk.gf180_mapped import gf180_mapped_pdk
from gdsfactory import Component
from glayout.util.comp_utils import move, movex, movey, prec_ref_center, evaluate_bbox, center_to_edge_distance
from glayout.util.port_utils import remove_ports_with_prefix, rename_ports_by_orientation
from glayout.primitives.fet import nmos
from glayout.primitives.fet import pmos
from glayout.primitives.guardring import tapring
from glayout.primitives.mimcap import mimcap
from glayout.primitives.mimcap import mimcap_array
from glayout.primitives.via_gen import via_stack
from glayout.primitives.via_gen import via_array
from two_transistor_interdigitized import two_nfet_interdigitized
from four_transistor_interdigitized import generic_4T_interdigitzed
from two_transistor_interdigitized import two_pfet_interdigitized
from glayout.routing.smart_route import smart_route
from glayout.routing.L_route import L_route
from glayout.routing.c_route import c_route
from glayout.routing.straight_route import straight_route
from typing import Literal, Optional
from glayout.spice.netlist import Netlist
from gdsfactory.components import text_freetype, rectangle
from glayout.primitives.via_gen import via_stack
from glayout.primitives.mimcap import mimcap
from polyres_2 import poly_resistor
from osc_core import osc_core
from v2i import v2i_stage
from op_buffer import op_buffer
from glayout.primitives.fet import nmos
def quad_osc(
        pdk: MappedPDK
        ) -> Component:
    
    pdk.activate()
    top_level = Component(name="quad_osc")

    v2i = v2i_stage(pdk)
    core = osc_core(pdk)
    buffer = op_buffer(pdk)

    v2i_ref = prec_ref_center(v2i)
    core_ref = prec_ref_center(core)
    buffer1_ref = prec_ref_center(buffer)
    buffer2_ref = prec_ref_center(buffer)
    buffer2_ref = rename_ports_by_orientation(buffer2_ref.mirror_x())

    top_level.add(v2i_ref)
    top_level.add(core_ref)
    top_level.add(buffer1_ref)
    top_level.add(buffer2_ref)

    dimensions_v2i = evaluate_bbox(v2i_ref)
    dimensions_core = evaluate_bbox(core_ref)
    dimensions_buffer = evaluate_bbox(buffer1_ref)
    
    v2i_ref.movey(core_ref.ymax + dimensions_v2i[1]/2 +7).movex(-dimensions_v2i[0]/2 -5)
    buffer1_ref.movey(core_ref.ymin - dimensions_buffer[1]/2).movex(core_ref.xmin - dimensions_buffer[0]/2 -10)
    buffer2_ref.movey(core_ref.ymin - dimensions_buffer[1]/2).movex(core_ref.xmax + dimensions_buffer[0]/2 +10)
    
    #connecting output of v2i to osc_core
    top_level << smart_route(pdk, v2i_ref.ports["iout_top_met_E"], core_ref.ports["iin_top_met_N"], hwidth=1.5, vwidth=1.5) 
    
    #connecting oscillator outputs to buffer
    top_level << smart_route(pdk, core_ref.ports["v4_bottom_lay_W"], buffer1_ref.ports["cap1_top_met_N"])
    top_level << smart_route(pdk, core_ref.ports["v2_bottom_lay_W"], buffer1_ref.ports["cap2_top_met_N"])
    top_level << smart_route(pdk, core_ref.ports["v3_bottom_lay_E"], buffer2_ref.ports["cap1_top_met_N"])
    top_level << smart_route(pdk, core_ref.ports["v1_bottom_lay_E"], buffer2_ref.ports["cap2_top_met_N"])

    switch = two_nfet_interdigitized(pdk, numcols=2, fingers=3, with_substrate_tap = False)
    switch_ref = prec_ref_center(switch)
    top_level.add(switch_ref)

    switch_ref.movey(v2i_ref.ymin-5).movex(v2i_ref.xmin - 15)
    top_level << smart_route(pdk, switch_ref.ports["A_gate_E"], switch_ref.ports["B_gate_E"])

    top_level << smart_route(pdk, v2i_ref.ports["vref_top_met_S"], switch_ref.ports["A_drain_E"])
    top_level << smart_route(pdk, v2i_ref.ports["vctrl_top_met_S"], switch_ref.ports["B_drain_E"])

    arrm2m3_2 = via_array(
        pdk,
        "met2",
        "met3",
        num_vias=(2,2),
        fullbottom=True
    )
    vref_via = prec_ref_center(arrm2m3_2)
    vctrl_via = prec_ref_center(arrm2m3_2)
    vctrl_via.move(switch_ref.ports["A_source_W"].center).movex(-10).movey(-3)
    vref_via.move(switch_ref.ports["B_source_W"].center).movex(-10).movey(3)
    top_level.add(vref_via)
    top_level.add(vctrl_via)

    top_level << smart_route(pdk, switch_ref.ports["A_source_W"], vctrl_via.ports["top_met_N"])
    top_level << smart_route(pdk, switch_ref.ports["B_source_W"], vref_via.ports["top_met_S"])

    top_level << smart_route(pdk, v2i_ref.ports["vdd1_bottom_lay_N"], buffer1_ref.ports["vdd_top_met_N"], width1=2, cwidth=2, extension=4)
    top_level << smart_route(pdk, v2i_ref.ports["vdd2_top_met_E"], buffer2_ref.ports["vdd_top_met_N"], vwidth=2, hwidth=2)

    top_level << smart_route(pdk, core_ref.ports["vss_top_met_S"], buffer1_ref.ports["vss_bottom_lay_E"], vwidth=2, hwidth=2)
    top_level << smart_route(pdk, buffer1_ref.ports["vss_bottom_lay_E"], buffer2_ref.ports["vss_bottom_lay_W"], width=2)

    vss_via = prec_ref_center(arrm2m3_2)
    vss_via.move(buffer2_ref.ports["vss_top_met_W"].center).movex(-15).movey(-20)
    top_level.add(vss_via)
    top_level << smart_route(pdk, buffer2_ref.ports["vss_bottom_lay_W"], vss_via.ports["top_met_N"], vwidth=2, hwidth=2)
    
    en_via = prec_ref_center(arrm2m3_2)
    en_via.move(switch_ref.ports["A_gate_W"].center).movex(-18)
    top_level.add(en_via)
    top_level << straight_route(pdk, switch_ref.ports["A_gate_W"], en_via.ports["bottom_lay_E"])

    return top_level

osc = quad_osc(gf180_mapped_pdk)
osc.show()
osc.name = "osc"
magic_drc_result = gf180_mapped_pdk.drc_magic(osc, osc.name)


