(*#-#-#-#-#-#-#-#-#-#---Declaration---#-#-#-#-#-#-#-#-#-#-#-#-#*)
METHOD PRIVATE getOrder : typ_OrderData
VAR_INPUT
END_VAR

(*#-#-#-#-#-#-#-#-#-#---Implementation---#-#-#-#-#-#-#-#-#-#-#-#-#*)
// getOrder.ulOrderNo:=getOrder.ulOrderNo+1;
// 		//random(IN_diMin:=1,In_diMax:=100);
// 		o_type:=random2.di_Result;
// 		IF o_type=0 THEN
// 			o_type:=1;
// 		END_IF
// 		getOrder.uiQty:=o_type;
// 		random1(IN_diMin:=1,In_diMax:=100);
// 		b_type:=random1.di_Result;
// 		b:=b_type;
// 		getOrder.eType:=TO_STRING(b_Type);
// 		FOR i:=1 TO 4 BY 1 DO
// 			random2();
// 			a_type:=random2.di_Result;
// 			ARR2[i]:=a_type;
// 			IF ARR2[i]=ARR2[i-1] THEN
// 				a_type:=6;
// 			ELSE
// 				a_type:=random2.di_Result;
// 			END_IF
// 			getOrder.aeAccessories[i]:=TO_STRING(a_Type);
// 		END_FOR