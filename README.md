# Smart door
## Door lock with Face Recognition (feat. Raspberry Pi 3b+)

### What does the code do?

With this code the Raspberry Pi will detect button input to do a face recognition test.

Then if the face is recognized it will switch on a relais to pull back the electromagnetic door lock lever which will enable you to open the door.

If you have entered the room you need to click the other button which is located on the inside of the room to close the lock again as soon as you have closed the door again.

When you want to get out again just press this button again and the lock will open.

To close the lock from the outside just press the button that is located on the outside.

During the whole time the code is running the connected LCD display will show useful information. Note that in order to interact with the LCD display I needed this lcddriver.py script which is made only for my specific display model so you might have to handle your display a little different.

### How I implemented it

Raspberry Pi + Camera + LCD Display on the outside of the door:

![outside](./PicturesOfMyDoorlockSetup/OutsideBox1.jpg=500x)
