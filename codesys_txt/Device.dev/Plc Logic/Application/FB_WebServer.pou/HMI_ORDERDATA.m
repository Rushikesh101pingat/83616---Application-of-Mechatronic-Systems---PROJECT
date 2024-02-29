(*#-#-#-#-#-#-#-#-#-#---Declaration---#-#-#-#-#-#-#-#-#-#-#-#-#*)
METHOD HMI_ORDERDATA : typ_OrderData
VAR_INPUT
END_VAR

(*#-#-#-#-#-#-#-#-#-#---Implementation---#-#-#-#-#-#-#-#-#-#-#-#-#*)
o_type:=random2.di_Result;
HMI_ORDERDATA.uiQty:=HMI_qty;
HMI_ORDERDATA.eType:=TO_STRING(HMI_b_Type);
HMI_ORDERDATA.aeAccessories[1]:=TO_STRING(HMI_a1_Type);
HMI_ORDERDATA.aeAccessories[2]:=TO_STRING(HMI_a2_Type);
HMI_ORDERDATA.aeAccessories[3]:=TO_STRING(HMI_a3_Type);
HMI_ORDERDATA.aeAccessories[4]:=TO_STRING(HMI_a4_Type);
