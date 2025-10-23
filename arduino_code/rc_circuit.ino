// C++ code
//
const int pinoNoRC = A0;
int valorLido = 0;
float tensaoCapacitor = 0, tensaoResistor;
unsigned long time;
 
void setup(){ 
Serial.begin(9600); 
} 

void loop() { 
	time = millis(); 
	valorLido = analogRead(pinoNoRC); 
	tensaoResistor = (valorLido * 5.0 / 1023); // 5.0V / 1023 degraus = 0.0048876 
	tensaoCapacitor = abs(5.0 - tensaoResistor);
  
 	Serial.print(time); //imprime o conteúdo de time no MONITOR SERIAL
    Serial.print("ms | VR: "); 
  	Serial.print(tensaoResistor);
  	Serial.print("| VC: ");
  	Serial.println(tensaoCapacitor); 
  
	delay(400); 
}
