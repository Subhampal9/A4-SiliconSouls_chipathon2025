import numpy as np
np.float_ = np.float64


from gdsfactory.components import rectangle
from gdsfactory import Component
from glayout.pdk.mappedpdk import MappedPDK
from glayout.primitives.via_gen import via_array
from glayout.routing.straight_route import straight_route
from glayout.routing.smart_route import smart_route
from glayout.routing.c_route import c_route
from glayout.routing.L_route import L_route
from glayout.util.comp_utils import prec_center,prec_ref_center, movey, align_comp_to_port, movex, evaluate_bbox
from glayout.util.port_utils import add_ports_perimeter
from glayout.pdk.sky130_mapped import sky130_mapped_pdk
from glayout.pdk.gf180_mapped import gf180_mapped_pdk
from glayout.spice import Netlist
from glayout.primitives.guardring import tapring

def poly_resistor_netlist(
    circuit_name: str,
    model: str,
    width: float,
    length: float,
    multipliers: int
) -> Netlist :

    ltop = (round(length, 2))*(1e-6)
    wtop = (round(width, 2))*(1e-6)
    mtop = multipliers

    #source_netlist=""".subckt {model} r0 r1 """+f'\n l={ltop} w={wtop} '

    #source_netlist += "\n.ends"

    source_netlist="""\n.subckt {circuit_name} {nodes} """+f'l={ltop} w={wtop} m={mtop}'+"""
XMAIN PLUS MINUS VSUBS {model} r_width={{w}} r_length={{l}} m={{m}}"""

    source_netlist += "\n.ends {circuit_name}"



    return Netlist(
        circuit_name=circuit_name,
        nodes=['PLUS', 'MINUS', 'VSUBS'],
        source_netlist=source_netlist,
        instance_format="X{name} {nodes} {circuit_name} l={length} w={width} m={multipliers}}",
        parameters={
            'model': model,
            'length': ltop,
            'width': wtop,
            'multipliers': mtop,
        }
    )

def poly_resistor(
    pdk: MappedPDK,
    length: float = 1.65,
    width: float = 1,
    fingers: int = 1,
    with_tie: bool = True,
    tie_layers: tuple[str,str] = ("met2","met1"),
) -> Component:
    #poly_res = (66, 13)
    sab = (49,0)
    res_mk = (110,5)
    resistor = (62,0)
    p_res = Component()
    contact_length = 0.46 + 0.05
    separation = 0.4 + width
    #Extend poly for contacts
    ex_length = length + 2*contact_length
    for i in range(0,(fingers+2)):
        #poly resistor rectangle
        p_rect = rectangle(size=(width,ex_length), layer=pdk.get_glayer("poly"), centered=True)
        p_rect_ref = prec_ref_center(p_rect)
        p_res.add(p_rect_ref)
        movex(p_rect_ref, (i)*separation)
        #Add li layer on top and bottom contacts
        li_top = rectangle(size=(width,contact_length), layer=pdk.get_glayer("met1"), centered=True)
        li_top_ref = prec_ref_center(li_top)
        p_res.add(li_top_ref)
        movey(li_top_ref, contact_length/2 + length/2+0.22)
        movex(li_top_ref, (i)*separation)

        li_bot = rectangle(size=(width,contact_length), layer=pdk.get_glayer("met1"), centered=True)
        li_bot_ref = prec_ref_center(li_bot)
        p_res.add(li_bot_ref)
        movey(li_bot_ref, - contact_length/2 - length/2-0.22)
        movex(li_bot_ref, (i)*separation)

        ##Add unsalicide layer
        unsal = rectangle(size=((width+0.56),(length+0.25)), layer=sab, centered=True)
        unsal_ref = prec_ref_center(unsal)
        p_res.add(unsal_ref)
        movex(unsal_ref, (i)*separation)
        
        ##Add RES_MK layer
        resmk = rectangle(size=((width+0.56),(length)), layer=res_mk, centered=True)
        resmk_ref = prec_ref_center(resmk)
        p_res.add(resmk_ref)
        movex(resmk_ref, (i)*separation)

        #Place poly to li via contact
        licon1 = via_array(pdk, "poly", "met1", size=(width,contact_length), fullbottom=True)
        licon1_ref = prec_ref_center(licon1)
        #p_res.add(licon1_ref)
        #movey(licon1_ref, contact_length/2 + length/2)

        licon2 = via_array(pdk, "poly", "met1", size=(width,contact_length), fullbottom=True)
        licon2_ref = prec_ref_center(licon2)
        p_res.add(licon2_ref)
        movey(licon2_ref, - contact_length/2 - length/2-0.22)
        movex(licon2_ref, (i)*separation)

        licon3 = via_array(pdk, "poly", "met1", size=(width,contact_length), fullbottom=True)
        licon3_ref = prec_ref_center(licon3)
        p_res.add(licon3_ref)
        movey(licon3_ref, contact_length/2 + length/2+0.22)
        movex(licon3_ref, (i)*separation)

        # place metal 1 layer on contacts
        met1_top = rectangle(size=(width,contact_length), layer=pdk.get_glayer("met1"), centered=True)
        met1_top_ref = prec_ref_center(met1_top)
        p_res.add(met1_top_ref)
        movey(met1_top_ref, contact_length/2 + length/2+0.22)
        movex(met1_top_ref, (i)*separation)

        met1_bot = rectangle(size=(width,contact_length), layer=pdk.get_glayer("met1"), centered=True)
        met1_bot_ref = prec_ref_center(met1_bot)
        p_res.add(met1_bot_ref)
        movey(met1_bot_ref, - contact_length/2 - length/2-0.22)
        movex(met1_bot_ref, (i)*separation)
       
        p_res.add_ports(met1_bot_ref.get_ports_list(), prefix=f"{i}_s_")
        p_res.add_ports(met1_top_ref.get_ports_list(), prefix=f"{i}_n_")


    
    # add plus layer
    plus = rectangle(size=((((fingers+2)*width)+((fingers+1)*separation)+0.4), (0.22+0.5)), layer=pdk.get_glayer("p+s/d"), centered=True)
    plus_ref_1 = prec_ref_center(plus)
    plus_ref_2 = prec_ref_center(plus)
    p_res.add(plus_ref_1)
    p_res.add(plus_ref_2)
    movey(plus_ref_1, contact_length/2 + length/2 + 0.22 - 0.05)
    movey(plus_ref_2, -contact_length/2 - length/2 - 0.22 + 0.05)
    movex(plus_ref_1, (fingers+1)*separation/2)
    movex(plus_ref_2, (fingers+1)*separation/2)

    final = Component()
    p_res_ref_1 = prec_ref_center(p_res)
    p_res_ref_2 = prec_ref_center(p_res)
    p_res_ref_1.movey(evaluate_bbox(p_res_ref_1)[1]/2 + 2)
    p_res_ref_2.movey(-evaluate_bbox(p_res_ref_2)[1]/2 - 2)
    final.add(p_res_ref_1)
    final.add(p_res_ref_2)
    final.add_ports(p_res_ref_1.get_ports_list(), prefix=f"top_")
    final.add_ports(p_res_ref_2.get_ports_list(), prefix=f"bot_")
    
    m1m2 = via_array(pdk, "met1", "met2", size=(width/2,contact_length), fullbottom=False)
    res1_a_via = prec_ref_center(m1m2)
    final.add(res1_a_via)
    res1_a_via.move(p_res_ref_1.ports["1_s_e4"].center).movex(-width).movey(-0.60)
    res1_b_via = prec_ref_center(m1m2)
    final.add(res1_b_via)
    res1_b_via.move(p_res_ref_2.ports["2_n_e2"].center).movex(-width/4).movey(0.60)
    res1_c_via = prec_ref_center(m1m2)
    final.add(res1_c_via)
    res1_c_via.move(p_res_ref_2.ports["3_n_e2"].center).movex(width/4).movey(0.60)
    res1_d_via = prec_ref_center(m1m2)
    final.add(res1_d_via)
    res1_d_via.move(p_res_ref_1.ports["4_s_e4"].center).movex(width).movey(-0.60)

    final << L_route(pdk, p_res_ref_1.ports["1_s_e4"], res1_a_via.ports["bottom_lay_E"], hwidth=0.23, vwidth=0.23, hglayer="met1", vglayer="met1")
    final << L_route(pdk, res1_a_via.ports["bottom_lay_S"], res1_b_via.ports["top_met_W"], hwidth=0.23, vwidth=0.28)
    final << straight_route(pdk, res1_b_via.ports["bottom_lay_S"], p_res_ref_2.ports["2_n_e2"], width=0.23, glayer1="met1")
    
    final << straight_route(pdk, p_res_ref_2.ports["2_s_e1"], p_res_ref_2.ports["3_s_e3"], width=0.25, glayer1="met1")

    final << L_route(pdk, p_res_ref_1.ports["4_s_e4"], res1_d_via.ports["bottom_lay_W"], hwidth=0.23, vwidth=0.23, hglayer="met1", vglayer="met1")
    final << L_route(pdk, res1_d_via.ports["bottom_lay_S"], res1_c_via.ports["top_met_E"], hwidth=0.23, vwidth=0.28)
    final << straight_route(pdk, res1_c_via.ports["bottom_lay_S"], p_res_ref_2.ports["3_n_e2"], width=0.23, glayer1="met1")

    res2_a_via = prec_ref_center(m1m2)
    final.add(res2_a_via)
    res2_a_via.move(p_res_ref_2.ports["1_n_e2"].center).movex(width/4).movey(1.4)
    res2_b_via = prec_ref_center(m1m2)
    final.add(res2_b_via)
    res2_b_via.move(p_res_ref_1.ports["2_s_e4"].center).movex(width/4).movey(-1.4)
    res2_c_via = prec_ref_center(m1m2)
    final.add(res2_c_via)
    res2_c_via.move(p_res_ref_1.ports["3_s_e4"].center).movex(-width/4).movey(-1.4)
    res2_d_via = prec_ref_center(m1m2)
    final.add(res2_d_via)
    res2_d_via.move(p_res_ref_2.ports["4_n_e2"].center).movex(-width/4).movey(1.4)

    final << straight_route(pdk, res2_a_via.ports["bottom_lay_S"], p_res_ref_2.ports["1_n_e2"], width=0.23, glayer1="met1")
    final << straight_route(pdk, res2_b_via.ports["bottom_lay_N"], p_res_ref_1.ports["2_s_e4"], width=0.23, glayer1="met1")
    final << L_route(pdk, res2_a_via.ports["bottom_lay_N"], res2_b_via.ports["top_met_W"], hwidth=0.23, vwidth=0.28)
    
    final << straight_route(pdk, p_res_ref_1.ports["2_n_e1"], p_res_ref_1.ports["3_n_e3"], width=0.25, glayer1="met1")
    
    final << straight_route(pdk, res2_c_via.ports["bottom_lay_N"], p_res_ref_1.ports["3_s_e4"], width=0.23, glayer1="met1")
    final << straight_route(pdk, res2_d_via.ports["bottom_lay_S"], p_res_ref_2.ports["4_n_e2"], width=0.23, glayer1="met1")
    final << L_route(pdk, res2_c_via.ports["top_met_W"], res2_d_via.ports["bottom_lay_S"], hwidth=0.23, vwidth=0.28)
    

    # add hres layer
    hres = rectangle(size=((((fingers+2)*width)+((fingers+1)*separation)+0.8),(2*evaluate_bbox(p_res_ref_1)[1]+4)), layer=resistor, centered=True)
    hres_ref = prec_ref_center(hres)
    final.add(hres_ref)
    
    if with_tie:
        tap_separation = max(
            pdk.util_max_metal_seperation(),
            pdk.get_grule("active_diff", "active_tap")["min_separation"],
        )
        tap_separation += pdk.get_grule("p+s/d", "active_tap")["min_enclosure"]+0.25
        tap_encloses = (
            2 * (tap_separation + final.xmax),
            2 * (tap_separation + final.ymax),
        )
        tiering_ref = final << tapring(
            pdk,
            enclosed_rectangle=tap_encloses,
            sdlayer="p+s/d",
            horizontal_glayer=tie_layers[0],
            vertical_glayer=tie_layers[1],
        )

    final.add_ports(tiering_ref.get_ports_list(), prefix="welltie_")
    final << straight_route(pdk, final.ports["top_0_n_e3"], final.ports["welltie_W_top_met_E"])
    final << straight_route(pdk, final.ports["top_0_s_e3"], final.ports["welltie_W_top_met_E"])
    final << straight_route(pdk, final.ports["top_5_n_e1"], final.ports["welltie_E_top_met_W"])
    final << straight_route(pdk, final.ports["top_5_n_e1"], final.ports["welltie_E_top_met_W"])
    final << straight_route(pdk, final.ports["bot_0_n_e3"], final.ports["welltie_W_top_met_E"])
    final << straight_route(pdk, final.ports["bot_0_s_e3"], final.ports["welltie_W_top_met_E"])
    final << straight_route(pdk, final.ports["bot_5_n_e1"], final.ports["welltie_E_top_met_W"])
    final << straight_route(pdk, final.ports["bot_5_s_e1"], final.ports["welltie_E_top_met_W"])
    
    arrm2m3_2 = via_array(
        pdk,
        "met1",
        "met2",
        num_vias=(2,1),
        fullbottom=True
    )
    res1_p_via = prec_ref_center(arrm2m3_2)
    res1_m_via = prec_ref_center(arrm2m3_2)
    res2_p_via = prec_ref_center(arrm2m3_2)
    res2_m_via = prec_ref_center(arrm2m3_2)

    res1_p_via.move(final.ports["top_1_n_e2"].center).movey(-0.25)
    res1_m_via.move(final.ports["top_4_n_e2"].center).movey(-0.25)
    res2_p_via.move(final.ports["bot_1_s_e4"].center).movey(0.25)
    res2_m_via.move(final.ports["bot_4_s_e4"].center).movey(0.25)

    final.add(res1_p_via)
    final.add(res1_m_via)
    final.add(res2_p_via)
    final.add(res2_m_via)

    final.add_ports(res1_p_via.get_ports_list(), prefix="one_p_")
    final.add_ports(res1_m_via.get_ports_list(), prefix="one_m_")
    final.add_ports(res2_p_via.get_ports_list(), prefix="two_p_")
    final.add_ports(res2_m_via.get_ports_list(), prefix="two_m_")
    # add pwell
    #p_res.add_padding(
    #    layers=(pdk.get_glayer("pwell"),),
    #    default=pdk.get_grule("pwell", "active_tap")["min_enclosure"],
    #)
    #p_res = add_ports_perimeter(p_res,layer=pdk.get_glayer("pwell"),prefix="well_")

    #print(i)
    if i%2 == 0:
        final.add_ports(met1_top_ref.get_ports_list(), prefix="PLUS_")
    else:
        final.add_ports(met1_bot_ref.get_ports_list(), prefix="PLUS_")
    
    final.add_ports(tiering_ref.get_ports_list(), prefix="tie_")
    
    #final << straight_route(pdk, p_res_ref_1.ports["0_n_e2"], tiering_ref.ports["N_bot_met_N"])
    
    final.info['netlist'] = poly_resistor_netlist(
        circuit_name="POLY_RES",
        model= 'ppolyf_u_1k',
        width=width,
        length=length,
        multipliers=1,
    )
    #print(final.get_ports_list())
    return final.flatten()

def add_polyres_labels(pdk: MappedPDK, p_res: Component, length, width, fingers):
    p_res.unlock()
    #met1_label = (68, 5)
    #met1_pin = (68, 16)
    move_info = list()
    separation = 0.4 + width
    contact_length = 0.46+0.05
    p_pin = p_res << rectangle(size=(0.1,0.1),layer=pdk.get_glayer("met2"),centered=True)
    if fingers%2 == 0:
        movey(p_pin, -contact_length/2 - length/2)
        movex(p_pin, (fingers-1)*separation)
    else:
        movey(p_pin, contact_length/2 + length/2)
        movex(p_pin, (fingers-1)*separation)

    m_pin = p_res << rectangle(size=(0.1,0.1),layer=pdk.get_glayer("met2"),centered=True)
    movey(m_pin, -contact_length/2 - length/2)

    #plus label
    p_label = rectangle(layer=pdk.get_glayer("met2_pin"), size=(0.1,0.1), centered=True).copy()
    p_label.add_label(text="PLUS",layer=pdk.get_glayer("met2_label"))
    move_info.append((p_label,p_pin.ports["e1"],None))

    m_label = rectangle(layer=pdk.get_glayer("met2_pin"), size=(0.1,0.1), centered=True).copy()
    m_label.add_label(text="MINUS",layer=pdk.get_glayer("met2_label"))
    move_info.append((m_label,m_pin.ports["e1"],None))

    sub_label = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.5,0.5),centered=True).copy()
    sub_label.add_label(text="VSUBS",layer=pdk.get_glayer("met2_label"))
    move_info.append((sub_label,p_res.ports["tie_N_top_met_N"], None))
    for comp, prt, alignment in move_info:
        alignment = ('c','b') if alignment is None else alignment
        compref = align_comp_to_port(comp, prt, alignment=alignment)
        p_res.add(compref)
    return p_res.flatten()


resistor = poly_resistor(gf180_mapped_pdk, length=10, width=1, fingers=4) 
resistor.show()
#resistor.name = "POLY_RES"
#magic_drc_result = gf180_mapped_pdk.drc_magic(resistor, resistor.name)
#lvs_result = gf180_mapped_pdk.lvs_netgen(resistor,resistor.name,copy_intermediate_files=True)
#print(resistor.info['netlist'].generate_netlist())
