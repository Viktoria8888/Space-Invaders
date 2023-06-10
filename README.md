---
title: Project OOP
---
**Author: Wiktoria Kaszpruk (Viktoriia Kashpruk)
Index:    337014**
Date: 10.06.23
## Programming project for OOP course
### UML Diagram:
![](https://hackmd.io/_uploads/BJ8HHyfPh.png)



There are a few more helper classes in my project, but I didn't include them since they're not as important
### What is the project about?
**Brief description**
My project involves implementing a simple 2D game using Python, titled **"Space Invaders".** The objective of the game is to shoot down all enemies by moving a spaceship and firing bullets from it. The user has a limited number of bullets, which are replenished over time. The player wins if they manage to destroy 42 enemies without losing all their lives. There's also an option to restore lives and continue the game.

In addition to this, I've added another "game", if you can call it that, which presents algebra problems from an exam on a screen. The solution can be displayed if the user chooses to do so. Why did I decide to implement such an additional 'game'? Primarily, it's to learn more about algebra and science modules in Python, or, in other words, to combine business with pleasure.

Usually, in modern games, if a player loses, they have the option to watch some ads to restore their lives. I've chosen an alternative form of 'punishment': math problems.

To solve the math problems, I've implemented functions that can provide the solutions. However, it turned out that displaying the results can be quite problematic. For instance, labels in Pygame do not accept the newline character '\n'. As a result, to display four vectors as a solution, I would need to create four separate label objects, which is quite cumbersome and inconvenient. Another issue with the display arises after Gram-Schmidt orthogonalization or expanding to basis; the vector values become unreadable due to machine rounding. That is why I have decided not to include some math problems, although the functions that solve them can be easily found in Solutions.py
## How to play?
Make sure to install all the modules needed:
```
$ pip install pygame
$ pip install numpy
# pip install sympy
```
1) $ python3 game.py
Then such screen should appear (with music):

![](https://hackmd.io/_uploads/rJV2iJzv2.png)

2) Click on either of two options:
    Let's try **"Space invaders"** first

![](https://hackmd.io/_uploads/ByNG6yGv3.png)
* You can use **"<-"** and **"->"** to move the ship.
* Click "SPACE" to fire the bullet.
* To win you should reach the score of **42**.
* With each score increase the spawning speed of enemies will also go up.
* To come back to Menu click "ESC" on your keyboard.
* If the vertical bar on the left is **red** it means you cannot fire bullets for some time.
* If you lose all of your lives, which are displayed on the top right - you lose.

**Have a nice time playing!**

2) Let's choose "Play with algebra"
There is some language mix up but I decided not to change it to avoid math vocabulary confusion.

![](https://hackmd.io/_uploads/S1KfegMvn.png)

You can see the solution by clicking "Show the solution" and then if your own solution was correct click "Correct" button and "Wrong" in other case.
To come back to menu click "Wrong" after "Show the solution" button.


## Difficulties that arised during the course of the project
1) ~~**The enemies slow down when the ship starts moving.**~~
In the end, I was unable to resolve this problem. The root cause might lie in the 'while' loop and in Pygame as a module. There is a considerable amount of collision checking and other side effects in the game that cause it to slow down. So, I have decided to keep this bug as a feature.
**It later turned out that the problem was with the operating system**
2) **Collision checking**
Regarding the previous point, in my game, I add the enemies that are spawned and the bullets that are fired to separate lists. I then check for collisions by iterating through these lists and using the Euclidean distance formula $\sqrt {\left( {x_1 - x_2 } \right)^2 + \left( {y_1 - y_2 } \right)^2 }$.
This method is quite inefficient because it has a time complexity of O($n^2$). However, I later discovered that the Pygame module contains a fantastic feature called "Sprite," which can group objects together and check collisions between elements in the group using a more efficient algorithm. Unfortunately, it was too late for me to change the entire implementation, so I chose to leave everything as is.

3) **Displaying labels/buttons and other object on the screen**
Positioning objects correctly, such as in the middle of the screen or fitting the images and scaling them, so they fit the screen, proved to be quite challenging. This issue isn't so much a problem with the programming, but rather the design aspect of the project.

4) **Explosion animation**
This was one of the hardest parts to implement, so I used the code and the picture frames from another game.The link can be found on "Credits" section.

4) **How the game looks on different operating systems**
This game was created on Ubuntu OS but when switched to Windows the game screen looked too scaled and I do not know how to resolve the issue. So it is recommended to use Linux for this game

## What the project has taught me?
1) **Object-oriented programming concepts**
To be frank, during the course of this project, I've learned much more about programming than I did during the entire semester. This experience once again highlighted the importance of practice. As the saying goes, practice makes perfect.

2) **Numpy and Sympy Modules**
This project gave me a chance to get a grasp on these modules and to appreciate their power and capabilities.

3) **Basics of Game Engines**
Although Pygame is a straightforward module to use – which is precisely why it was chosen in the first place, it offers significant learning opportunities for beginners.

