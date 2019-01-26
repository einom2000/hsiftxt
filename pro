// Serial test script
#include <Keyboard.h>
#include <MouseTo.h>
#include <Mouse.h>
int buttonPin = 9;  // Set a button to any pin
int setPoint = 55;
String readString;
int r = 0;
int t = 0;

void setup()
{
  pinMode(buttonPin, INPUT); // Set the button as an input
  digitalWrite(buttonPin, HIGH); // Pull the button high
  Serial.begin(9600);  // initialize serial communications at 9600 bps
  Keyboard.begin();
  Mouse.begin();
  MouseTo.setCorrectionFactor(1);
}

void loop()
{
  if (digitalRead(buttonPin) == 0)
  {
    // serial read section
    while (Serial.available()) // this will be skipped if no data present, leading to
                             // the code sitting in the delay function below
    {
      delay(30);  //delay to allow buffer to fill
      if (Serial.available() > 0)
      {
        char c = Serial.read();  //gets one byte from serial buffer
        readString += c; //makes the string readString
       }
     }
     if (readString.length() > 0)
     {
        char key_in = readString.charAt(0);
        if (key_in == 's')
        {
          Keyboard.write((char) 32);  //(char) 32
          Serial.print("Done!");
          readString = "";
          key_in = "";
        }
        else if (key_in == 'r')  //'r' for right mouse double click
        {
          r = random(1, 1);
          t = random(80, 120);
          Mouse.click(MOUSE_RIGHT);
          delay(r * t);
          Mouse.click(MOUSE_RIGHT);
          Serial.print("Done!");
          readString = "";
          key_in = "";
        }
        else if (key_in == 'l')  //'l' for left click
        {
          Mouse.click();
          Serial.print("Done!");
          readString = "";
          key_in = "";
        }
        else if (key_in == 't')  //'t' for right click
        {
          Mouse.click(MOUSE_RIGHT);
          Serial.print("Done!");
          readString = "";
          key_in = "";
        }
        else if (key_in == 'M' )  // mouse move command  or cuold be less than 57 to trigger the mouse
        {
          int commaIndex = readString.indexOf(',');
          String positionX = readString.substring(1, commaIndex);
          String positionY = readString.substring(commaIndex + 1);
          int x = atoi(positionX.c_str());
          int y = atoi(positionY.c_str());
          MouseTo.setTarget(x, y);
          while (MouseTo.move() == false) {}
          Serial.print("Done!");
          readString ="";
          key_in = "";
        }
        else if (key_in == 'N' )  // mouse relative move
        {
          int commaIndex = readString.indexOf(',');
          String positionX = readString.substring(1, commaIndex);
          String positionY = readString.substring(commaIndex + 1);
          int x = atoi(positionX.c_str());
          int y = atoi(positionY.c_str());
          Mouse.move(x , y);
          Serial.print("Done!");
          readString ="";
          key_in = "";
        }
        else if (key_in == '=') // do nothing
        {
          Serial.print("Done!");
          readString = "";
          key_in = "";
         }
        else
        {
          Keyboard.write(key_in); // other key command
          Serial.print("Done!");
          //Serial.println(readString); //see what was received
          readString = "";
          key_in = "";
         }
      }

     delay(500);
  }
}