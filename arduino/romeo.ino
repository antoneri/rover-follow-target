int E1 = 5; // M1 speed
int E2 = 6; // M2 speed
int M1 = 4; // M1 direction
int M2 = 7; // M1 direction

void stop(void) {
	digitalWrite(E1, LOW);
	digitalWrite(E2, LOW);
}

void forward(char a, char b) {
	analogWrite(E1, a);
	digitalWrite(M1, HIGH);
	analogWrite(E2, b);
	digitalWrite(M2, HIGH);
}

void backward(char a, char b) {
	analogWrite(E1, a);
	digitalWrite(M1, LOW);   
	analogWrite(E2, b);    
	digitalWrite(M2, LOW);
}

void left (char a, char b) {
	analogWrite(E1, a);
	digitalWrite(M1, LOW);    
	analogWrite(E2, b);    
	digitalWrite(M2, HIGH);
}

void right (char a, char b) {
	analogWrite(E1, a);
	digitalWrite(M1, HIGH);    
	analogWrite(E2, b);    
	digitalWrite(M2, LOW);
}

void setup(void) { 
	int i;
	for (i = 4; i <= 7; i++) {
		pinMode(i, OUTPUT);
	}
	
	Serial.begin(9600);
	Serial.print("ready");
}

void loop(void) {
	if (Serial.available()) {
		char val = Serial.read();
		if (val != -1) {
			switch(val) {
			case 'w':
				forward(255, 255);
				break;
			case 's':
				backward(255, 255);
				break;
			case 'a':
				left(255, 255);
				break;
			case 'd':
				right(255, 255);
				break;
			case 'x':
				stop();
				break;
			}
		} else {
			stop();
		}
	}
}
