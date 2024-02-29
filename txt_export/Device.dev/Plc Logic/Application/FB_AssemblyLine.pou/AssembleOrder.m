(*#-#-#-#-#-#-#-#-#-#---Declaration---#-#-#-#-#-#-#-#-#-#-#-#-#*)
METHOD AssembleOrder : BOOL
VAR_INPUT
	pOrderData: POINTER TO TYP_OrderData;
END_VAR

(*#-#-#-#-#-#-#-#-#-#---Implementation---#-#-#-#-#-#-#-#-#-#-#-#-#*)
IF Busy THEN
	AssembleOrder:=FALSE;
ELSE
	counter:=counter+1;
	c:=pOrderData^.eType;	
	IF c='BMX' THEN
		IF pOrderData^.uiQty<=STOCK_BMX THEN
			STOCK_BMX:=STOCK_BMX-pOrderData^.uiQty;
		ELSE
			Flag:=1;
		END_IF		
	END_IF
	IF c='Electric' THEN
		IF pOrderData^.uiQty<=STOCK_Electric THEN
			STOCK_Electric:=STOCK_Electric-pOrderData^.uiQty;
		ELSE
			Flag:=1;
		END_IF		
	END_IF
	IF c='Folding' THEN
		IF pOrderData^.uiQty<=STOCK_Folding THEN
			STOCK_Folding:=STOCK_Folding-pOrderData^.uiQty;
		ELSE
			Flag:=1;
		END_IF		
	END_IF
	IF c='Road' THEN
		IF pOrderData^.uiQty<=STOCK_Road THEN
			STOCK_Road:=STOCK_Road-pOrderData^.uiQty;
		ELSE
			Flag:=1;
		END_IF		
	END_IF
	FOR k:=1 TO 4 BY 1 DO
		b:=pOrderData^.aeAccessories[k];
		IF b='GPS' THEN
			IF STOCK_GPS>=pOrderData^.uiQty THEN
				STOCK_GPS:=STOCK_GPS-pOrderData^.uiQty;
			ELSE
				Flag:=1;
											
			END_IF
		ELSIF b='Lights' THEN
			IF STOCK_LIGHTS>=pOrderData^.uiQty THEN
				STOCK_LIGHTS:=STOCK_LIGHTS-pOrderData^.uiQty;
			ELSE
				Flag:=1;
											
			END_IF
		ELSIF b='Bell' THEN
			IF STOCK_BELL>=pOrderData^.uiQty THEN
				STOCK_BELL:=STOCK_BELL-pOrderData^.uiQty;
			ELSE
				Flag:=1;
											
			END_IF
		ELSIF b='Lock' THEN
			IF STOCK_LOCK>=pOrderData^.uiQty THEN
				STOCK_LOCK:=STOCK_LOCK-pOrderData^.uiQty;
			ELSE
				Flag:=1;
											
			END_IF
		ELSIF b='Speedometer' THEN
			IF STOCK_SPEEDO>=pOrderData^.uiQty THEN
				STOCK_SPEEDO:=STOCK_SPEEDO-pOrderData^.uiQty;
			ELSE
				Flag:=1;
											
			END_IF
		END_IF
	END_FOR
	k:=1;						
	IF Flag<>1 THEN
		Flag:=0;
		OrderData := pOrderData^;
		newOrder := TRUE;
		AssembleOrder:=TRUE;
	ELSE		
		AssembleOrder:=FALSE;
	END_IF
	

END_IF