(*#-#-#-#-#-#-#-#-#-#---Declaration---#-#-#-#-#-#-#-#-#-#-#-#-#*)
//FB_Init is always available implicitly and it is used primarily for initialization.
//The return value is not evaluated. For a specific influence, you can also declare the
//methods explicitly and provide additional code there with the standard initialization
//code. You can evaluate the return value.
METHOD FB_Init: BOOL
VAR_INPUT
    bInitRetains: BOOL; // TRUE: the retain variables are initialized (reset warm / reset cold)
    bInCopyCode: BOOL;  // TRUE: the instance will be copied to the copy code afterward (online change)   
	pFB_Server: POINTER TO FB_WebSERVER; 
	apFB_AssemblyLine: ARRAY[0..4] OF POINTER TO FB_AssemblyLine;  
END_VAR
(*#-#-#-#-#-#-#-#-#-#---Implementation---#-#-#-#-#-#-#-#-#-#-#-#-#*)
THIS^.pFB_Server := pFB_Server;
THIS^.apFB_AssemblyLine := apFB_AssemblyLine;