This is a fork of the original Waveshare library, where I've added RLE decompression support for the *epd1in4b* model, in order to enable storing 9 bitmaps (4 black/white/red images + a b/w one) inside the `PROGMEM` of an *Arduino Lilypad*for the *Multiznachok (мультизначок)* project.

![Bag with Multiznachock (мультизначок)](1.54inch_e-paper_b/arduino/doc-images/multiznachok.gif)

There's also a python script to convert pbm images to the [homebrew] RLE format support by the library.

For more information, see the [epd1in54bRLE/](1.54inch_e-paper_b/arduino) folder *(symbolic link to the only folder I've touched)*, and the `readme` file there.

KTHXBYE

----

Original readme file:


# Arduino libraries for Waveshare e-paper series
Arduino libraries for Waveshare e-paper series 1.54"/1.54" B/2.13"/2.13" B/2.7"/2.7" B/2.9"/2.9" B/4.2"/4.2 B/7.5"/ 7.5" B
## Hardware connection (e-Paper --> Arduino)
    3.3V --> 3V3
    GND  --> GND
    DIN  --> D11
    CLK  --> D13
    CS   --> D10
    DC   --> D9
    RST  --> D8
    BUSY --> D7
## Expected result
1.  Copy the libraries (e-paper/arduino/libraries) of Arduino demo code to 
    the libraries directory of Arduino IDE.
    (C:\users\username\documents\arduino\libraries by default. You can also 
    specify the location on 
    Arduino IDE --> File --> Preferences --> Sketchbook location).
2.  Open the project (arduino/epd-demo/epd-demo.ino)
3.  Compile and upload the program.
4.  The e-Paper will display strings, shapes and images.
*   The RAM of Arduino UNO is only 2K. However, these 3 e-paper displays: 
1.54" B/7.5"/7.5" B
cannot support partial update of the frame memory (that is, unable to completely 
update one frame by updating partial of it several times).
Therefore the Arduino examples for them can only display static images.
The following products are not affected:
1.54"/2.13"/2.13" B/2.7"/2.7" B/2.9"/2.9" B/4.2"/4.2 B.
## Supported models
1.54"/1.54" B/2.13"/2.13" B/2.7"/2.7" B/2.9"/2.9" B/4.2"/4.2 B/7.5"/ 7.5" B

![e-paper display](http://www.waveshare.com/img/devkit/general/e-Paper-Modules-CMP.jpg)
