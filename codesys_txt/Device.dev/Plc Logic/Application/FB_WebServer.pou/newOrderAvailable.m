(*#-#-#-#-#-#-#-#-#-#---Declaration---#-#-#-#-#-#-#-#-#-#-#-#-#*)
METHOD PRIVATE newOrderAvailable : BOOL
VAR_INPUT
END_VAR

(*#-#-#-#-#-#-#-#-#-#---Implementation---#-#-#-#-#-#-#-#-#-#-#-#-#*)
orderTimer(IN:=NOT orderTimer.Q,PT:=T#1130S);
		IF orderTimer.Q THEN
			newOrderAvailable:=TRUE;
		ELSE
			newOrderAvailable:=FALSE;
		END_IF