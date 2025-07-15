---
title: "Zephyr"
authors: "Radean Rashed & Alex Li"
description: "AI enabled quadcopter with autonomous navigation capabilities for intelligence, reconnaisance and surveillance missions."
created_at: "2025/7/10"
---

# July 14th: Initial research & modelling
By: Radean

Began to research the various components of a drone, identifying how we'd wire everything and get them to work. I began by laying out our software requirements, then searched for parts that would be able to fulfill them. The initial plan was to use an arduino to control the drone and a Raspberry Pi for the compute that we'd need, but after looking at various FPV drone guides and online tutorials, I came to realize that using a dedicated flight controller & ESC stack would be much more effective and still be capable of communicating with the Raspberry Pi. Based on the size of the drone and some rough weight calculations (Raspi is about 50g, flight controller stack is about 25g, assume 50g per motor) I also determined that we'd likely need 7inch props, informing the choice of motors and battery. Here is a rough diagram I made outlining the general flow of components in the system:

<img src="./Flowchart.png" width="100%" />

I also looked at some drone designs online and began modelling a basic chassis that would be capable of housing the various parts. I had to CAD my own version of the flight controller stack, as no online models were available, but I ended up being able to package everything in a way that leaves no space unused and should be fairly easy to access:
<img src="./First Chassis.png" width="100%" /> 

**Total time spent: 4h**