(*#-#-#-#-#-#-#-#-#-#---Declaration---#-#-#-#-#-#-#-#-#-#-#-#-#*)

METHOD PRIVATE newOrderAvailable : BOOL
VAR_INPUT
END_VAR

(*#-#-#-#-#-#-#-#-#-#---Implementation---#-#-#-#-#-#-#-#-#-#-#-#-#*)

// orderTimer(IN:=NOT orderTimer.Q,PT:=T#1110S);
// 		IF orderTimer.Q THEN
// 			newOrderAvailable:=TRUE;
// 		ELSE
// 			newOrderAvailable:=FALSE;
// 		END_IF
IF GVL.OPCUA_Server.orderData.ulOrderNo <> uiLastOrder_ID THEN
	newOrderAvailable:=TRUE;
ELSE 
	newOrderAvailable:=FALSE;
END_IF
