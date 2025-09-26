from glayout.pdk.mappedpdk import MappedPDK
from glayout.pdk.gf180_mapped import gf180_mapped_pdk
from gdsfactory import Component
from glayout.util.comp_utils import move, movex, movey, prec_ref_center, evaluate_bbox, center_to_edge_distance, align_comp_to_port
from glayout.util.snap_to_grid import component_snap_to_grid
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
from glayout.primitives.via_gen import via_stack, via_array
from gdsfactory.component_reference import ComponentReference

def add_delay_stage_labels(delay_in: Component,
                pdk: MappedPDK 
                ) -> Component:
	
    delay_in.unlock()
    # list that will contain all port/comp info
    move_info = list()
    # create labels and append to info list
    # vss
    vsslabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.5,0.5),centered=True).copy()
    vsslabel.add_label(text="VSS",layer=pdk.get_glayer("met2_label"))
    move_info.append((vsslabel,delay_in.ports["ccinv_bottom_B_source_E"],None))
    
    # vdd
    vddlabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.5,0.5),centered=True).copy()
    vddlabel.add_label(text="VDD",layer=pdk.get_glayer("met2_label"))
    move_info.append((vddlabel,delay_in.ports["inv_top_welltie_N_top_met_N"],None))
    
    # vsp
    vsplabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.5,0.5),centered=True).copy()
    vsplabel.add_label(text="VSP",layer=pdk.get_glayer("met2_label"))
    move_info.append((vsplabel,delay_in.ports["inv_top_A_source_W"],None))
    # vinp
    vinplabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
    vinplabel.add_label(text="VINP",layer=pdk.get_glayer("met2_label"))
    move_info.append((vinplabel,delay_in.ports["inv_bottom_A_gate_W"],None))
    # vinm
    vinmlabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
    vinmlabel.add_label(text="VINM",layer=pdk.get_glayer("met2_label"))
    move_info.append((vinmlabel,delay_in.ports["inv_bottom_B_gate_E"],None))
        
    # VOUTM
    voutmlabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.5,0.5),centered=True).copy()
    voutmlabel.add_label(text="VOUTM",layer=pdk.get_glayer("met2_label"))
    move_info.append((voutmlabel,delay_in.ports["inv_top_A_drain_N"], None))
    # VOUTP
    voutplabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.5,0.5),centered=True).copy()
    voutplabel.add_label(text="VOUTP",layer=pdk.get_glayer("met2_label"))
    move_info.append((voutplabel,delay_in.ports["inv_top_B_drain_N"], None))
    
    # move everything to position
    for comp, prt, alignment in move_info:
        alignment = ('c','c') if alignment is None else alignment
        compref = align_comp_to_port(comp, prt, alignment=alignment)
        delay_in.add(compref)
    return delay_in.flatten()

def delay_stage_netlist(inv_pair: ComponentReference, cc_invs: ComponentReference) -> Netlist:
    netlist = Netlist(circuit_name='delay_stage', nodes=['VDD', 'VSS', 'VSP', 'VINP', 'VINM', 'VOUTM', 'VOUTP'])
    netlist.connect_netlist(inv_pair.info['netlist'], [('VDD1', 'VSP'), ('VDD2', 'VSP'), ('VSS1', 'VOUTM'), ('VSS2', 'VOUTP'), ('VG1','VINP'), ('VG2','VINM'), ('VB1','VDD'), ('VDD3', 'VOUTM'), ('VDD4', 'VOUTP'), ('VSS3', 'VSS'), ('VSS4', 'VSS'), ('VG3','VINP'), ('VG4','VINM'), ('VB2','VSS')])
    netlist.connect_netlist(cc_invs.info['netlist'], [('VDD1', 'VSP'), ('VDD2', 'VSP'), ('VSS1', 'VOUTM'), ('VSS2', 'VOUTP'), ('VG1','VOUTP'), ('VG2','VOUTM'), ('VB1','VDD'), ('VDD3', 'VOUTM'), ('VDD4', 'VOUTP'), ('VSS3', 'VSS'), ('VSS4', 'VSS'), ('VG3','VOUTP'), ('VG4','VOUTM'), ('VB2','VSS')])
    
    return netlist

def delay_stage(
        pdk: MappedPDK,
        inv_params: tuple[tuple[float,float], float, tuple[int,int]] = ((2,1), 0.18, (1,1)),
        ccinv_params: tuple[tuple[float,float], float, tuple[int,int]] = ((2,1), 0.18, (1,1))
        ) -> Component:
    
    pdk.activate()
    top_level = Component(name="delay_stage")

    inv_pair = generic_4T_interdigitzed(pdk,
                                        numcols = 2,
                                        with_substrate_tap = False,
                                        length = inv_params[1],
                                        top_kwargs = {"width": inv_params[0][0], "fingers": inv_params[2][0]},
                                        bottom_kwargs = {"width": inv_params[0][1], "fingers": inv_params[2][1]}
                                        )
    cc_invs = generic_4T_interdigitzed(pdk,
                                        numcols = 2,
                                        with_substrate_tap = False,
                                        length = ccinv_params[1],
                                        top_kwargs = {"width": ccinv_params[0][0], "fingers": ccinv_params[2][0]},
                                        bottom_kwargs = {"width": ccinv_params[0][1], "fingers": ccinv_params[2][1]}
                                        )
    inv_pair_ref = prec_ref_center(inv_pair)
    cc_invs_ref = prec_ref_center(cc_invs)
    top_level.add(inv_pair_ref)
    top_level.add(cc_invs_ref)

    
    ref_dimensions_a = evaluate_bbox(inv_pair_ref)
    ref_dimensions_b = evaluate_bbox(cc_invs_ref)

    inv_pair_ref.movey(ref_dimensions_a[1]/2 + pdk.util_max_metal_seperation()+5)
    cc_invs_ref.movey(-ref_dimensions_b[1]/2 - pdk.util_max_metal_seperation()-5)
    top_level.add_ports(inv_pair_ref.get_ports_list(),prefix="inv_")
    top_level.add_ports(cc_invs_ref.get_ports_list(),prefix="ccinv_")

    top_level << smart_route(pdk, inv_pair_ref.ports["top_A_source_E"], inv_pair_ref.ports["top_B_source_E"])
    top_level << smart_route(pdk, inv_pair_ref.ports["bottom_A_source_E"], inv_pair_ref.ports["bottom_B_source_E"])
    top_level << smart_route(pdk, inv_pair_ref.ports["top_B_gate_E"], inv_pair_ref.ports["bottom_B_gate_E"], extension=3)
    top_level << smart_route(pdk, inv_pair_ref.ports["top_A_gate_W"], inv_pair_ref.ports["bottom_A_gate_W"], extension=3)
    top_level << smart_route(pdk, inv_pair_ref.ports["top_A_drain_W"], inv_pair_ref.ports["bottom_A_drain_W"], extension=1)
    top_level << smart_route(pdk, inv_pair_ref.ports["top_B_drain_E"], inv_pair_ref.ports["bottom_B_drain_E"], extension=5)
    top_level << straight_route(pdk, inv_pair_ref.ports["top_A_source_W"], inv_pair_ref.ports["top_welltie_W_top_met_E"], glayer1="met1")
    top_level << straight_route(pdk, inv_pair_ref.ports["bottom_A_source_W"], inv_pair_ref.ports["bottom_welltie_W_top_met_E"], glayer1="met1")

    top_level << smart_route(pdk, cc_invs_ref.ports["top_A_source_E"], cc_invs_ref.ports["top_B_source_E"])
    top_level << smart_route(pdk, cc_invs_ref.ports["bottom_A_source_E"], cc_invs_ref.ports["bottom_B_source_E"])
    top_level << smart_route(pdk, cc_invs_ref.ports["top_B_gate_E"], cc_invs_ref.ports["bottom_B_gate_E"], extension=2)
    top_level << smart_route(pdk, cc_invs_ref.ports["top_A_gate_W"], cc_invs_ref.ports["bottom_A_gate_W"])
    top_level << smart_route(pdk, cc_invs_ref.ports["top_A_drain_W"], cc_invs_ref.ports["bottom_A_drain_W"], extension=1)
    top_level << smart_route(pdk, cc_invs_ref.ports["top_B_drain_E"], cc_invs_ref.ports["bottom_B_drain_E"], extension=5)
    top_level << smart_route(pdk, cc_invs_ref.ports["top_B_drain_W"], cc_invs_ref.ports["bottom_A_gate_W"], extension=9)
    top_level << smart_route(pdk, cc_invs_ref.ports["top_A_drain_E"], cc_invs_ref.ports["bottom_B_gate_E"], extension=7.5)
    top_level << straight_route(pdk, cc_invs_ref.ports["top_A_source_W"], cc_invs_ref.ports["top_welltie_W_top_met_E"], glayer1="met1")
    top_level << straight_route(pdk, cc_invs_ref.ports["bottom_A_source_W"], cc_invs_ref.ports["bottom_welltie_W_top_met_E"], glayer1="met1")
    
    top_level << smart_route(pdk, inv_pair_ref.ports["bottom_B_drain_E"], cc_invs_ref.ports["top_B_gate_E"], extension = 6.5)
    top_level << smart_route(pdk, inv_pair_ref.ports["bottom_A_drain_E"], cc_invs_ref.ports["top_A_gate_E"], extension = 9)

    top_level << smart_route(pdk, inv_pair_ref.ports["top_welltie_tl_top_met_W"], cc_invs_ref.ports["top_welltie_tl_top_met_W"])
    
    top_level.info['netlist'] = delay_stage_netlist(inv_pair_ref, cc_invs_ref)

    return component_snap_to_grid(rename_ports_by_orientation(top_level)).flatten()

#delay = delay_stage(gf180_mapped_pdk)
#delay = add_delay_stage_labels(delay_stage(gf180_mapped_pdk), gf180_mapped_pdk)
#print(delay.info['netlist'].generate_netlist())
#delay.show()
#delay.name = "delay_stage"
#magic_drc_result = gf180_mapped_pdk.drc_magic(delay, delay.name)
#netgen_lvs_result = gf180_mapped_pdk.lvs_netgen(delay, delay.name)
