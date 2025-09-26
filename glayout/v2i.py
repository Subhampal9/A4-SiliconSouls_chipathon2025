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

def v2i_stage(
        pdk: MappedPDK,
        p_params: tuple[float, float, int] = (5, 0.28, 5),
        n_params: tuple[float, float, int] = (1.25, 0.28, 5)
        ) -> Component:

    pdk.activate()
    top_level = Component(name="v2i_stage")

    v2i_p = two_pfet_interdigitized(pdk,numcols=2,with_substrate_tap=False, length=p_params[1], width=p_params[0], fingers=p_params[2], sd_rmult = 2)
    v2i_n = two_nfet_interdigitized(pdk,numcols=2,with_substrate_tap=False, length=n_params[1], width=n_params[0], fingers=n_params[2], sd_rmult = 2)
    v2i_out = two_pfet_interdigitized(pdk,numcols=2,with_substrate_tap=False, length=p_params[1], width=p_params[0], fingers=p_params[2], sd_rmult = 2)

    v2i_p_ref = prec_ref_center(v2i_p)
    v2i_n_ref = prec_ref_center(v2i_n)
    v2i_out_ref = prec_ref_center(v2i_out)
    
    top_level.add(v2i_p_ref)
    top_level.add(v2i_n_ref)
    top_level.add(v2i_out_ref)

    ref_dimensions_p = evaluate_bbox(v2i_p_ref)
    ref_dimensions_n = evaluate_bbox(v2i_n_ref)

    v2i_p_ref.movey(ref_dimensions_p[1]/2 + 2.5).movex(-ref_dimensions_p[0]/2 - 1.5)
    v2i_out_ref.movey(ref_dimensions_p[1]/2 + 2.5).movex(ref_dimensions_p[0]/2 + 1.5)
    v2i_n_ref.movey(v2i_p_ref.ymin - ref_dimensions_p[1]/2 - 2.5).movex(-ref_dimensions_p[0]/2 - 1.5)
    
    #dnwell = rectangle(size = ((ref_dimensions_n[0]+5),(ref_dimensions_n[1]+5)), layer=pdk.get_glayer("dnwell"), centered=True)
    #dnwell_ref = prec_ref_center(dnwell)
    #top_level.add(dnwell_ref)

    #dnwell_ref.movey(v2i_p_ref.ymin - ref_dimensions_p[1]/2 - 2.5).movex(-ref_dimensions_p[0]/2 - 1.5)
    
    nwell = rectangle(size = ((top_level.xmax-top_level.xmin+pdk.get_grule("nwell","active_diff")["min_enclosure"]),(ref_dimensions_p[1]+pdk.get_grule("nwell","active_diff")["min_enclosure"])), layer=pdk.get_glayer("nwell"), centered=True)
    nwell_ref = prec_ref_center(nwell)
    top_level.add(nwell_ref)
    nwell_ref.movey(v2i_p_ref.ymin + ref_dimensions_p[1]/2)
    
    #core p routing
    top_level << smart_route(pdk, v2i_p_ref.ports["A_source_E"], v2i_p_ref.ports["B_source_E"], cwidth = 0.5,extension = 1.5)
    top_level << straight_route(pdk, v2i_p_ref.ports["A_source_W"], v2i_p_ref.ports["welltie_W_top_met_E"])
    top_level << smart_route(pdk, v2i_p_ref.ports["A_gate_W"], v2i_p_ref.ports["A_drain_W"], cwidth = 0.5)
    top_level << smart_route(pdk, v2i_p_ref.ports["B_gate_E"], v2i_p_ref.ports["B_drain_E"], cwidth = 0.5)
    
    #out p routing
    top_level << smart_route(pdk, v2i_out_ref.ports["A_source_E"], v2i_out_ref.ports["B_source_E"], cwidth = 0.5, extension = 1.5)
    top_level << smart_route(pdk, v2i_out_ref.ports["A_drain_E"], v2i_out_ref.ports["B_drain_E"], cwidth = 0.5)
    top_level << smart_route(pdk, v2i_out_ref.ports["A_gate_E"], v2i_out_ref.ports["B_gate_E"], cwidth = 0.5)
    top_level << straight_route(pdk, v2i_out_ref.ports["A_source_W"], v2i_out_ref.ports["welltie_W_top_met_E"])
    
    #core n routing
    #top_level << straight_route(pdk, v2i_n_ref.ports["A_source_W"], v2i_n_ref.ports["welltie_W_top_met_E"])
    top_level << smart_route(pdk, v2i_n_ref.ports["A_source_E"], v2i_n_ref.ports["B_source_E"], cwidth = 0.5, extension = 1.5)

    #core-out connection
    top_level << straight_route(pdk, v2i_p_ref.ports["B_gate_E"], v2i_out_ref.ports["B_gate_W"])
    top_level << straight_route(pdk, v2i_p_ref.ports["welltie_tr_top_met_E"], v2i_out_ref.ports["welltie_tl_top_met_W"])

    #core p-n connection
    top_level << smart_route(pdk, v2i_p_ref.ports["A_gate_W"], v2i_n_ref.ports["A_drain_W"], cwidth = 0.5)
    top_level << smart_route(pdk, v2i_p_ref.ports["B_gate_E"], v2i_n_ref.ports["B_drain_E"], cwidth = 0.5)

    arrm3m4_2 = via_array(
        pdk,
        "met3",
        "met4",
        num_vias=(2,2),
        fullbottom=True
    )
    
    vdd1_int_via = prec_ref_center(arrm3m4_2)
    vdd1_int_via.movey(v2i_p_ref.ymax+1.5).movex(v2i_p_ref.xmin-1.5)
    vdd2_int_via = prec_ref_center(arrm3m4_2)
    vdd2_int_via.movey(v2i_out_ref.ymax+1.5).movex(v2i_out_ref.xmax+1.5)
    
    top_level.add(vdd1_int_via)
    top_level.add(vdd2_int_via)

    top_level << smart_route(pdk, v2i_p_ref.ports["B_source_W"], vdd1_int_via.ports["bottom_lay_S"])
    top_level << smart_route(pdk, v2i_out_ref.ports["B_source_E"], vdd2_int_via.ports["bottom_lay_S"])
    top_level << straight_route(pdk, vdd1_int_via.ports["top_met_E"], vdd2_int_via.ports["top_met_W"])
    
    top_level.add_ports(vdd1_int_via.get_ports_list(), prefix="vdd1_")
    top_level.add_ports(vdd2_int_via.get_ports_list(), prefix="vdd2_")
    
    arrm2m3_2 = via_array(
        pdk,
        "met2",
        "met3",
        num_vias=(2,2),
        fullbottom=True
    )

    iout_int_via = prec_ref_center(arrm2m3_2)
    iout_int_via.movex(v2i_out_ref.xmax+4.5).movey(v2i_out_ref.ports["B_drain_E"].center[1])
    top_level.add(iout_int_via)
    top_level << straight_route(pdk, v2i_out_ref.ports["B_drain_E"], iout_int_via.ports["bottom_lay_W"])

    ibias_int_via = prec_ref_center(arrm2m3_2)
    ibias_int_via.movex(v2i_n_ref.xmin-4.5).movey(v2i_n_ref.ports["B_source_E"].center[1])
    top_level.add(ibias_int_via)
    top_level << straight_route(pdk, v2i_n_ref.ports["B_source_W"], ibias_int_via.ports["bottom_lay_E"])
    
 
    vctrl_int_via = prec_ref_center(arrm3m4_2)
    vref_int_via = prec_ref_center(arrm3m4_2)
    vctrl_int_via.movex(v2i_n_ref.xmin-2.5).movey(v2i_n_ref.ymin-1.5)
    vref_int_via.movex(v2i_n_ref.xmax+2.5).movey(v2i_n_ref.ymin-1.5)
    
    top_level.add(vctrl_int_via)
    top_level.add(vref_int_via)

    top_level << smart_route(pdk, v2i_n_ref.ports["A_gate_W"], vctrl_int_via.ports["bottom_lay_N"])
    top_level << smart_route(pdk, v2i_n_ref.ports["B_gate_E"], vref_int_via.ports["bottom_lay_N"])

    top_level.add_ports(v2i_p_ref.get_ports_list(), prefix="v2ip")
    top_level.add_ports(v2i_n_ref.get_ports_list(), prefix="v2in")
    top_level.add_ports(v2i_out_ref.get_ports_list(), prefix="v2io")
    top_level.add_ports(vref_int_via.get_ports_list(), prefix="vref_")
    top_level.add_ports(vctrl_int_via.get_ports_list(), prefix="vctrl_")
    top_level.add_ports(iout_int_via.get_ports_list(), prefix="iout_")
    top_level.add_ports(ibias_int_via.get_ports_list(), prefix="ibias_")

    return top_level
#v2i = v2i_stage(gf180_mapped_pdk)
#v2i.show()
#v2i.name = "v2i_stage"
#magic_drc_result = gf180_mapped_pdk.drc_magic(v2i, v2i.name)




