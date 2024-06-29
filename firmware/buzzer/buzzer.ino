#define R_PIN 22
#define L_PIN 23
#define BUFLEN 200
#define ID "EMDR Buzzer"

void setup() {
  Serial.begin(115200);
  pinMode(L_PIN, OUTPUT);
  pinMode(R_PIN, OUTPUT);
  test();
}

void buzz(char pin, int duration_ms) {
  digitalWrite(pin, HIGH);
  int waited = 0;
  while (waited < duration_ms && !Serial.available()) {
    delayMicroseconds(duration_ms * 10);
    waited += 10;
  }
  digitalWrite(pin, LOW);
}

void test() {
  buzz(L_PIN, 50);
  delayMicroseconds(1000 * 1000);
  buzz(R_PIN, 50);
}

void readln(char* buf) {
  char c = 0;
  int cntr = 0;
  while (c != '\n') {
    if (cntr >= BUFLEN - 1) {
      break;
    }
    if (Serial.available()) {
      c = Serial.read();
      if (c != '\r' && c != '\n') {
        *buf++ = c;
        cntr += 1;
      }
    }
  }
  *buf = 0;
}

void readcmd(char& cmd, int& val) {
  cmd = 0;
  val = 0;
  char buf[BUFLEN];
  char* s = buf;
  readln(buf);
  if (strlen(s)) {
    cmd = *s++;
  }
  if (strlen(s)) {
    val = atoi(s);  
  }
}

void loop() {
  char cmd;
  int val;
  while (true) {
    readcmd(cmd, val);
    switch (cmd) {
      // left cmd
      case 'l':
        buzz(L_PIN, val);
        break;
      // right cmd
      case 'r' :
        buzz(R_PIN, val);
        break;
      // id cmd
      case 'i':
        Serial.println(ID);
        break;
    }
  }
}
