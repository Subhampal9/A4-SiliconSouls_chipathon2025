from glayout.pdk.mappedpdk import MappedPDK
from glayout.pdk.gf180_mapped import gf180_mapped_pdk
from gdsfactory import Component
from glayout.util.comp_utils import move, movex, movey, prec_ref_center, evaluate_bbox, center_to_edge_distance
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
from glayout.primitives.via_gen import via_stack
from glayout.primitives.mimcap import mimcap
from polyres_2 import poly_resistor

def op_buffer(
        pdk: MappedPDK,
        cap_params: tuple[float,float] = (5,5),
        gain_params: tuple[tuple[float,float],float,tuple[int,int]] = ((2.2,1), 0.28, (1,1)),
        duty_params: tuple[tuple[float,float],float,tuple[int,int]] = ((12,5.3), 0.28, (1,1)),
        ccinv_params: tuple[tuple[float,float],float,tuple[int,int]] = ((1.125,0.5), 0.28, (1,1)),
        res_params: tuple[float,float] = (1,12.5)
        ) -> Component:

    pdk.activate()
    top_level = Component(name="op_buffer")

    cap = mimcap(pdk, 
                 size=cap_params
                 )
    gain_stage = generic_4T_interdigitzed(pdk,
                                    numcols=2,
                                    with_substrate_tap=False,
                                    length=gain_params[1],
                                    top_kwargs={"width": gain_params[0][0],
                                                "fingers": gain_params[2][0]},
                                    bottom_kwargs={"width": gain_params[0][1],
                                                   "fingers": gain_params[2][1]}
                                    )
    duty_stage = generic_4T_interdigitzed(pdk,
                                          numcols=4,
                                          with_substrate_tap=False,
                                          length=duty_params[1],
                                          top_kwargs={"width": duty_params[0][0],
                                                      "fingers": duty_params[2][0]},
                                          bottom_kwargs={"width": duty_params[0][1],
                                                         "fingers": duty_params[2][1]}
                                          )
    cc_invs = generic_4T_interdigitzed(pdk,
                                       numcols=2,
                                       with_substrate_tap=False,
                                       length=ccinv_params[1],
                                       top_kwargs={"width": ccinv_params[0][0],
                                                   "fingers": ccinv_params[2][0]},
                                       bottom_kwargs={"width": ccinv_params[0][1],
                                                      "fingers": ccinv_params[2][1]}
                                       )
    res = poly_resistor(pdk,
                        width = res_params[0],
                        length = res_params[1],
                        fingers = 4
                        )
    cap_a = prec_ref_center(cap)
    cap_b = prec_ref_center(cap)
    top_level.add(cap_a)
    top_level.add(cap_b)

    ref_dimensions_cap = evaluate_bbox(cap_a)

    cap_a.movex(-ref_dimensions_cap[0]/2 -2)
    cap_b.movex(ref_dimensions_cap[0]/2 +2)

    gain_ref = prec_ref_center(gain_stage)
    top_level.add(gain_ref)

    ref_dimensions_gain = evaluate_bbox(gain_ref)
    
    gain_ref.movey(cap_a.ymin - ref_dimensions_gain[1]/2 -2)
    
    top_level << smart_route(pdk, gain_ref.ports["top_A_source_E"], gain_ref.ports["top_B_source_E"])
    top_level << smart_route(pdk, gain_ref.ports["bottom_A_source_E"], gain_ref.ports["bottom_B_source_E"])
    top_level << smart_route(pdk, gain_ref.ports["top_B_gate_E"], gain_ref.ports["bottom_B_gate_E"], extension=8)
    top_level << smart_route(pdk, gain_ref.ports["top_A_gate_W"], gain_ref.ports["bottom_A_gate_W"])
    top_level << smart_route(pdk, gain_ref.ports["top_A_drain_W"], gain_ref.ports["bottom_A_drain_W"], extension=1)
    top_level << smart_route(pdk, gain_ref.ports["top_B_drain_E"], gain_ref.ports["bottom_B_drain_E"], extension=2)
    top_level << straight_route(pdk, gain_ref.ports["top_A_source_W"], gain_ref.ports["top_welltie_W_top_met_E"])
    top_level << straight_route(pdk, gain_ref.ports["bottom_A_source_W"], gain_ref.ports["bottom_welltie_W_top_met_E"])

    top_level << smart_route(pdk, cap_a.ports["bottom_met_W"], gain_ref.ports["top_A_gate_W"], width1=0.75, width2=0.5, cwidth=0.75)
    top_level << smart_route(pdk, cap_b.ports["bottom_met_E"], gain_ref.ports["top_B_gate_E"], width1=0.75, width2=0.5, cwidth=0.75)
    top_level.add_ports(cap_a.get_ports_list(), prefix="cap1_")
    top_level.add_ports(cap_b.get_ports_list(), prefix="cap2_")

    duty_ref = prec_ref_center(duty_stage)
    cc_invs_ref = prec_ref_center(cc_invs)

    top_level.add(duty_ref)
    top_level.add(cc_invs_ref)

    ref_dimensions_duty = evaluate_bbox(duty_ref)
    ref_dimensions_ccinv = evaluate_bbox(cc_invs_ref)

    duty_ref.movex(gain_ref.xmin - ref_dimensions_duty[0]/2 - 5)
    duty_ref.movey(gain_ref.ymax - ref_dimensions_duty[1]/2)
    cc_invs_ref.movex(duty_ref.xmin + ref_dimensions_ccinv[0]/2)
    cc_invs_ref.movey(duty_ref.ymax + ref_dimensions_ccinv[1]/2 +2)

    top_level << smart_route(pdk, duty_ref.ports["top_A_source_E"], duty_ref.ports["top_B_source_E"])
    top_level << smart_route(pdk, duty_ref.ports["bottom_A_source_E"], duty_ref.ports["bottom_B_source_E"])
    top_level << smart_route(pdk, duty_ref.ports["top_B_gate_E"], duty_ref.ports["bottom_B_gate_E"], extension=10)
    top_level << smart_route(pdk, duty_ref.ports["top_A_gate_W"], duty_ref.ports["bottom_A_gate_W"])
    top_level << smart_route(pdk, duty_ref.ports["top_A_drain_W"], duty_ref.ports["bottom_A_drain_W"], extension=1)
    top_level << smart_route(pdk, duty_ref.ports["top_B_drain_E"], duty_ref.ports["bottom_B_drain_E"], extension=2)
    top_level << straight_route(pdk, duty_ref.ports["top_A_source_W"], duty_ref.ports["top_welltie_W_top_met_E"])
    top_level << straight_route(pdk, duty_ref.ports["bottom_A_source_W"], duty_ref.ports["bottom_welltie_W_top_met_E"])
    
    top_level << smart_route(pdk, gain_ref.ports["bottom_A_drain_E"], duty_ref.ports["bottom_A_gate_E"], extension=2)
    top_level << smart_route(pdk, gain_ref.ports["bottom_B_drain_E"], duty_ref.ports["bottom_B_gate_E"], extension=5)

    top_level << smart_route(pdk, cc_invs_ref.ports["top_A_source_E"], cc_invs_ref.ports["top_B_source_E"])
    top_level << smart_route(pdk, cc_invs_ref.ports["bottom_A_source_E"], cc_invs_ref.ports["bottom_B_source_E"])
    top_level << smart_route(pdk, cc_invs_ref.ports["top_B_gate_E"], cc_invs_ref.ports["bottom_B_gate_E"], extension=7)
    top_level << smart_route(pdk, cc_invs_ref.ports["top_A_gate_W"], cc_invs_ref.ports["bottom_A_gate_W"])
    top_level << smart_route(pdk, cc_invs_ref.ports["top_A_drain_W"], cc_invs_ref.ports["bottom_A_drain_W"], extension=1)
    top_level << smart_route(pdk, cc_invs_ref.ports["top_B_drain_E"], cc_invs_ref.ports["bottom_B_drain_E"], extension=2)
    top_level << smart_route(pdk, cc_invs_ref.ports["top_B_drain_W"], cc_invs_ref.ports["bottom_A_gate_W"], extension=2)
    top_level << smart_route(pdk, cc_invs_ref.ports["top_A_drain_E"], cc_invs_ref.ports["bottom_B_gate_E"], extension=2)
    top_level << straight_route(pdk, cc_invs_ref.ports["top_A_source_W"], cc_invs_ref.ports["top_welltie_W_top_met_E"])
    top_level << straight_route(pdk, cc_invs_ref.ports["bottom_A_source_W"], cc_invs_ref.ports["bottom_welltie_W_top_met_E"])
    
    top_level << smart_route(pdk, duty_ref.ports["top_A_drain_W"], cc_invs_ref.ports["bottom_A_gate_W"], extension=10)
    top_level << smart_route(pdk, duty_ref.ports["top_B_drain_E"], cc_invs_ref.ports["bottom_B_gate_E"])

    res_ref= prec_ref_center(res)
    top_level.add(res_ref)

    ref_dimensions_res = evaluate_bbox(res_ref)

    res_ref.movey(duty_ref.ymin - ref_dimensions_res[1]/2)
    res_ref.movex((gain_ref.xmin + gain_ref.xmax)/2)

    top_level << smart_route(pdk, gain_ref.ports["bottom_A_gate_W"], res_ref.ports["one_p_bottom_lay_W"])
    top_level << smart_route(pdk, gain_ref.ports["bottom_A_drain_E"], res_ref.ports["one_m_bottom_lay_E"], extension=10)
    top_level << smart_route(pdk, gain_ref.ports["top_B_gate_W"], res_ref.ports["two_p_bottom_lay_W"], extension=8)
    top_level << smart_route(pdk, gain_ref.ports["bottom_B_drain_E"], res_ref.ports["two_m_bottom_lay_E"], extension=12)
    
    arrm2m3_2 = via_array(
        pdk,
        "met2",
        "met3",
        num_vias=(2,2),
        fullbottom=True
    )

    outp_int_via = prec_ref_center(arrm2m3_2)
    outm_int_via = prec_ref_center(arrm2m3_2)
    outp_int_via.movex(duty_ref.xmin-4.5).movey(duty_ref.ports["bottom_A_drain_W"].center[1])
    outm_int_via.movex(duty_ref.xmin-4.5).movey(duty_ref.ports["bottom_B_drain_W"].center[1])
    top_level.add(outp_int_via)
    top_level.add(outm_int_via)
    top_level << straight_route(pdk, duty_ref.ports["bottom_A_drain_W"], outp_int_via.ports["bottom_lay_E"])
    top_level << straight_route(pdk, duty_ref.ports["bottom_B_drain_W"], outm_int_via.ports["bottom_lay_E"])

    top_level << straight_route(pdk, gain_ref.ports["top_B_source_W"], duty_ref.ports["top_B_source_E"])
    top_level << smart_route(pdk, duty_ref.ports["top_B_source_W"], cc_invs_ref.ports["top_B_source_W"], extension=4.5)

    top_level << smart_route(pdk, gain_ref.ports["bottom_B_source_E"], duty_ref.ports["bottom_B_source_E"], extension=6.5)
    top_level << smart_route(pdk, duty_ref.ports["bottom_B_source_E"], cc_invs_ref.ports["bottom_B_source_E"], extension=4.5)
    
    vdd_int_via = prec_ref_center(arrm2m3_2)
    vdd_int_via.movex(cc_invs_ref.xmin-10).movey(cc_invs_ref.ports["top_B_source_W"].center[1])
    top_level.add(vdd_int_via)
    top_level << straight_route(pdk, cc_invs_ref.ports["top_B_source_W"], vdd_int_via.ports["bottom_lay_E"])

    vss_int_via = prec_ref_center(arrm2m3_2)
    vss_int_via.movex(gain_ref.xmax+15).movey(gain_ref.ports["bottom_B_source_E"].center[1])
    top_level.add(vss_int_via)
    top_level << straight_route(pdk, gain_ref.ports["bottom_B_source_E"], vss_int_via.ports["bottom_lay_W"])

    top_level.add_ports(outp_int_via.get_ports_list(), prefix="out1_")
    top_level.add_ports(outm_int_via.get_ports_list(), prefix="out2_")
    top_level.add_ports(vdd_int_via.get_ports_list(), prefix="vdd_")
    top_level.add_ports(vss_int_via.get_ports_list(), prefix="vss_")
    
    return top_level
#output_buffer = op_buffer(gf180_mapped_pdk)
#output_buffer.show()
#output_buffer.name = "op_buffer"
#magic_drc_result = gf180_mapped_pdk.drc_magic(output_buffer, output_buffer.name)





        
