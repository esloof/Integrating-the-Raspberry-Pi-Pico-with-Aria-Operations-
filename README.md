# Integrating-the-Raspberry-Pi-Pico-with-Aria-Operations-
I’ll describe how to build a management pack that integrates a Raspberry Pi Pico W with Aria Operations.

For the creation of the management pack, I’ll use the VMware Aria Operations Management Pack Builder. This appliance automates the complete process of programming the RP2040 input sensors via a REST API into a PAK file. Communications between Aria Operations and the Pi Pico will be done wireless using the Microdot framework. 

Creating a management pack for Aria Operations involves so many steps that I’ve decided to split this project into multiple blog articles. I’m using SimpleMind as a mind map tool to keep track of all the different components. All the source code will be hosted on GitHub. Please enhance or adjust this code to your own needs by forking or copying the code.

Before I started writing these articles, I’ve built a working prototype. The reason I’ve built this prototype was, to see if it's even possible to get everything to work. The prototype was also used during a recent training course delivery of the VMware vRealize Operations: Advanced Use Cases [v8.x].

The beta version of the Python code, including a working PAK file and some screenshots, are already available on GitHub. In upcoming articles, I’ll enhance the code and create new versions. Currently, the roadmap contains an API with authentication, dashboards, events, alerts, etc. Feel free to bring up any suggestions on my X channel or in the comments on GitHub.

https://www.ntpro.nl/blog/archives/3735-Integrating-the-Raspberry-Pi-Pico-with-Aria-Operations-Introduction.html
