//Bibliotecas
#include <Servo.h>                           //Inclui a biblioteca do Servo
Servo servoBase;                             //Inclui um objeto Servo para controlar o ServoMotor

/*Janela de amostragem com comprimento para amostra  em mS -  Necessária para  obter 
valores de pico nas ondas sonoras emitidas pelo Drone. */
const int janelaDeAmostra = 40;                    
const int LDR = A2;            //Pino para leitura analógica correspondente a iluminação
const int lampada = 12;        //Pino para acionamento da lâmpada - Chaveada por transistor TIP120
unsigned int amostra;          //Variável para armazenar a somatória dos valores de pico do sinal provenientes dos MICS
float diferenca;               //Variável para armazenar valor da diferenças de valor analógico entre A0 e A1     
int tolerancia = 2;            //Variavévl de ajuste do valor mínimo de diferença para executar a movimentção do servo
//int pos = 90;                //Variável para armazenar posicção do servo-motor
int servoBasePos = 90;         //Variável para armazenar do Servo
int luz;                       //Variável para armazenar informações da intensidade luminosa
float nivelA0;                 //Variável para armazenar o mível do sinal analógico em A0
float nivelA1;                 //Variável para armazenar o mível do sinal analógico em A1
float soma_media_0 = 0;        //Variável para armazenar valor da soma dos sinais em A0 para cáculo das médias   
float soma_media_1 = 0;        //Variável para armazenar soma dos sinais em A0 para cáculo das médias 
float media_0 = 0;             //Variável para armazenar média dos sinais para minimizar ruídos 
float media_1 = 0;             //Variável para armazenar a média dos sinais para minimizar ruídos 
char serial;                   //Variável para armazenar valores proveniente da entrada serial
//OBS: Os pinos das entradas dos MICs estão descritos na função intensidadeSinal(int pinAI)
//************************************Void Setup*******************************************
void setup()
{
  Serial.begin(9600);          //Comunicação serial para a verificação
  servoBase.attach(3);         //Pino correpondente ao servo
  pinMode(12, OUTPUT);
  delay(50);
}
//******************************Void Loop - Loop principal*********************************
void loop() {
  switch (serial) {
    case 'm':
      manual();
      break;

    case 'a':
      automatico();
      break;

    default:
      automatico();
      break;
  }
}
//------------------------------Funções principais------------------------------------------
//----------------------------Automatico - rastreador --------------------------------------
autom_ilum();                     //Verificação da luz ambiente

soma_media_0 = 0;                 //reset das médias
soma_media_1 = 0;                 //reset das médias

for (int i = 0; i < 2; i++) {
  nivelA1 = intensidadeSinal(1);
  soma_media_1 += nivelA1;
  nivelA0 = intensidadeSinal(0);
  soma_media_0 += nivelA0;
}

media_0 = ((soma_media_0) / 2);
media_1 = ((soma_media_1) / 2);


diferenca = media_1 - media_0 * 1.3;

//Caso em que microfone em A0 recebe maior intensidade sonora
if (diferenca > tolerancia and  servoBasePos > 6) {   
  servoBasePos -= 5;                           
  servoBase.write(servoBasePos);                    //Movimentação do servo no sentido anti horario
  delay(10);
}
//Caso em que microfone em A1 recebe maior intensidade sonora
else if ((diferenca < 0) and (diferenca * (-1) > tolerancia) and servoBasePos < 174) {
  servoBasePos += 5;                           
  servoBase.write(servoBasePos);                    //Movimentação do servo no sentido horario
  delay(10);
}
//Verificação da porta serial para sair da rotina
if (Serial.available() > 0) {                
  serial = Serial.read();
  break;
}
}
}
//-----------------------------------Modo manual-----------------------------------------------------
void manual() {
  while (1) {
    if (Serial.available() > 0) {                      //Lê o último byte do buffer de entrada serial
      serial = Serial.read();
      if (serial == 'a' or serial == 'm') {
        break;
      }
      else if (serial == 'x' and servoBasePos < 178) { //Movimentação horária
        servoBasePos = servoBasePos + 5;
        servoBase.write(servoBasePos);
        delay(10);
      }
      else if (serial == 'z' and servoBasePos > 2) {   //Movimentação anti horária
        servoBasePos = servoBasePos - 5;
        servoBase.write(servoBasePos);
        delay(10);
      }
      else if (serial == 'l') {                        //Liga lampada
        digitalWrite(lampada, HIGH);
      }
      else if (serial == 'd') {                        //Desliga lampada
        digitalWrite(lampada, LOW);
      }
    }
  }
}
//---------------------------------Medição de intensidade--------------------------------------------------
float intensidadeSinal(int pinAI) {                  //AI corresponde a entrada analógica que está inserido o microfone
  unsigned long tempo = millis();                    //Valor inicial do intervalo de amostra - A ser comparado
  float picoAPico = 0;                               //Nivel de pico a pico

  unsigned int sinalMax = 0;                         //Valor máximo do sinal
  unsigned int sinalMin = 1024;                      //Valor minimo do sinal


  while (millis() - tempo < janelaDeAmostra)         // coleta dados de amostra a cada 50 mS
  {
    amostra = analogRead(pinAI);                     //leitura do sinal do microfone na entrada analógica 1
    if (amostra < 1024)                              //Retirada de leituras desnecessárias
    {
      if (amostra > sinalMax)
      {
        sinalMax = amostra;                          // Guardar somente valores de nivel máximo na deteccão
      }
      else if (amostra < sinalMin)
      {
        sinalMin = amostra;                          // Guardar somente valores de nivel minimo na deteccão
      }
    }
  }
  picoAPico = sinalMax - sinalMin;                   // max - min = amplitude de pico a pico

  return picoAPico ;
}

//-------------------------------Acionamento  automático da ilumincação-------------------------------------------
void autom_ilum() {
  luz = analogRead(LDR);                                                                
  //Condição baseada na leitura intensidade luminosa e sonora do ambiente
  if (luz > 1000 or (intensidadeSinal(0) + intensidadeSinal(1)) > 5) {
    digitalWrite(lampada, HIGH);
  }
  else {
    digitalWrite(lampada, LOW);
  }
  delay(5);
}



