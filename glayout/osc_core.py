from glayout.pdk.mappedpdk import MappedPDK
from glayout.pdk.gf180_mapped import gf180_mapped_pdk
from gdsfactory import Component
from glayout.util.comp_utils import move, movex, movey, prec_ref_center, evaluate_bbox, center_to_edge_distance, align_comp_to_port
from glayout.util.port_utils import remove_ports_with_prefix
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
from glayout.primitives.via_gen import via_stack, via_array
from gdsfactory.component_reference import ComponentReference
from delay_stage import delay_stage, delay_stage_netlist

def osc_core(
        pdk: MappedPDK,
        inv_params: tuple[tuple[float,float], float, tuple[int,int]] = ((3.24,1.08), 0.28, (2,2)),
        ccinv_params: tuple[tuple[float,float], float, tuple[int,int]] = ((2.16,0.72), 0.28, (2,2))
        ) -> Component:

    pdk.activate()
    top_level = Component(name="osc_core")

    single_stage = delay_stage(pdk,
                               inv_params,
                               ccinv_params
                               )
    stage_one = prec_ref_center(single_stage)
    stage_two = prec_ref_center(single_stage)
    top_level.add(stage_one)
    top_level.add(stage_two)

    ref_dimensions = evaluate_bbox(stage_one)

    stage_one.movex(-ref_dimensions[0]/2 - pdk.util_max_metal_seperation() - 6)
    stage_two.movex(ref_dimensions[0]/2 + pdk.util_max_metal_seperation() + 6)
    
    via23 = via_array(pdk, "met2", "met3", size=(2,2))
    via23_1_outp = prec_ref_center(via23)
    via23_1_outm = prec_ref_center(via23)
    via23_1_inp = prec_ref_center(via23)
    via23_1_inm = prec_ref_center(via23)
    via23_2_outp = prec_ref_center(via23)
    via23_2_outm = prec_ref_center(via23)
    via23_2_inp = prec_ref_center(via23)
    via23_2_inm = prec_ref_center(via23)
    
    top_level.add(via23_1_inp)
    top_level.add(via23_1_inm)
    top_level.add(via23_2_inp)
    top_level.add(via23_2_inm)
    top_level.add(via23_1_outp)
    top_level.add(via23_1_outm)
    top_level.add(via23_2_outp)
    top_level.add(via23_2_outm)
    
    via23_1_inp.movex(stage_one.ports["inv_bottom_A_gate_W"].center[0]).movey(2.5)
    via23_1_inm.movex(stage_one.ports["inv_bottom_B_gate_W"].center[0]-2)
    via23_2_inp.movex(stage_two.ports["inv_bottom_A_gate_E"].center[0]).movey(-1.5)
    via23_2_inm.movex(stage_two.ports["inv_bottom_B_gate_E"].center[0]+2).movey(-4)

    top_level << smart_route(pdk, stage_one.ports["inv_bottom_A_gate_W"], via23_1_inp.ports["top_met_N"], hwidth=0.5, vwidth=0.5)
    top_level << smart_route(pdk, stage_one.ports["inv_bottom_B_gate_W"], via23_1_inm.ports["top_met_N"], hwidth=0.5, vwidth=0.5)
    top_level << smart_route(pdk, stage_two.ports["inv_bottom_A_gate_E"], via23_2_inp.ports["top_met_N"], hwidth=0.5, vwidth=0.5)
    top_level << smart_route(pdk, stage_two.ports["inv_bottom_B_gate_E"], via23_2_inm.ports["top_met_N"], hwidth=0.5, vwidth=0.5)

    via23_1_outp.move(stage_one.ports["inv_top_B_drain_E"].center).movex(12)
    via23_1_outm.move(stage_one.ports["inv_top_A_drain_E"].center).movex(14.5)
    via23_2_outp.move(stage_two.ports["inv_top_B_drain_W"].center).movex(-10)
    via23_2_outm.move(stage_two.ports["inv_top_A_drain_W"].center).movex(-12.5)

    top_level << straight_route(pdk, stage_one.ports["inv_top_A_drain_E"], via23_1_outm.ports["bottom_lay_W"])
    top_level << straight_route(pdk, stage_one.ports["inv_top_B_drain_E"], via23_1_outp.ports["bottom_lay_W"])
    top_level << straight_route(pdk, stage_two.ports["inv_top_A_drain_W"], via23_2_outm.ports["bottom_lay_E"])
    top_level << straight_route(pdk, stage_two.ports["inv_top_B_drain_W"], via23_2_outp.ports["bottom_lay_E"])

    top_level << smart_route(pdk, via23_1_outp.ports["top_met_S"], via23_2_inm.ports["bottom_lay_W"])
    top_level << smart_route(pdk, via23_1_outm.ports["top_met_S"], via23_2_inp.ports["bottom_lay_W"])
    top_level << smart_route(pdk, via23_1_inp.ports["bottom_lay_E"], via23_2_outp.ports["top_met_S"])
    top_level << smart_route(pdk, via23_1_inm.ports["bottom_lay_E"], via23_2_outm.ports["top_met_S"])

    top_level << straight_route(pdk, stage_one.ports["inv_bottom_B_source_E"], stage_two.ports["inv_bottom_B_source_W"])
    top_level << straight_route(pdk, stage_one.ports["ccinv_bottom_B_source_E"], stage_two.ports["ccinv_bottom_B_source_W"])
    top_level << smart_route(pdk, stage_two.ports["inv_bottom_B_source_E"], stage_two.ports["ccinv_bottom_B_source_E"], extension=10)

    via23_vss = prec_ref_center(via23)
    
    top_level.add(via23_vss)

    via23_vss.movey(stage_one.ports["ccinv_bottom_B_source_W"].center[1]).movex(stage_one.xmin-2.5)
    top_level << straight_route(pdk, stage_one.ports["ccinv_bottom_B_source_W"], via23_vss.ports["bottom_lay_E"])

    via23_ibias_int1 = prec_ref_center(via23)
    via23_ibias_int2 = prec_ref_center(via23)
    via23_ibias = prec_ref_center(via23)
    top_level.add(via23_ibias_int1) 
    top_level.add(via23_ibias_int2) 
    top_level.add(via23_ibias) 

    via23_ibias_int1.movey(stage_one.ymax +2).movex(stage_one.ports["inv_top_B_source_W"].center[0] -2) 
    via23_ibias_int2.movey(stage_one.ymax +2).movex(stage_two.ports["inv_top_B_source_W"].center[0] -2) 
    via23_ibias.movey(stage_one.ymax +2) 

    top_level << smart_route(pdk, stage_one.ports["inv_top_B_source_W"], via23_ibias_int1.ports["top_met_S"])
    top_level << smart_route(pdk, stage_two.ports["inv_top_B_source_W"], via23_ibias_int2.ports["top_met_S"])
    top_level << straight_route(pdk, via23_ibias.ports["bottom_lay_E"], via23_ibias_int2.ports["bottom_lay_W"])
    top_level << straight_route(pdk, via23_ibias.ports["bottom_lay_W"], via23_ibias_int1.ports["bottom_lay_E"])
    
    top_level.add_ports(via23_ibias.get_ports_list(), prefix="iin_")
    top_level.add_ports(via23_1_inp.get_ports_list(), prefix="v4_")
    top_level.add_ports(via23_1_inm.get_ports_list(), prefix="v2_")
    top_level.add_ports(via23_2_inp.get_ports_list(), prefix="v3_")
    top_level.add_ports(via23_2_inm.get_ports_list(), prefix="v1_")
    top_level.add_ports(via23_vss.get_ports_list(), prefix="vss_")

    return top_level

#core = osc_core(gf180_mapped_pdk)
#core.show()
#core.name = "osc_core"
#magic_drc_result = gf180_mapped_pdk.drc_magic(core, core.name)



