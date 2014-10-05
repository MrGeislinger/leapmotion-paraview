Interface with 3D Data by Touchless Control via a Leap Motion Controller
===================


##Quick Summary of Project

ParaView (open-source data visualization application) with Leap Motion controller via touchless interaction. Based around Python, this application allows rotation, moving view, slicing and zooming visual data through touchless interaction. Originally a graduate class project (UCSC - CMPS 261: "Advanced Visualization", Alex Pang).


###Overview:
> Interacting with 3D data with a mouse is usally cumbersome and unnatural.  
> Paraview, an open source data analysis and visualization application, allows   
> for both programmatic interactions and mouse and keyboard interactions.   
> However, mouse interactivity with 3D objects and data sets can be difficult to  
> navigate.    
>  
>  
> The limitation that one must interactive with 3D objects via a 2D interface   
> makes it difficult to view the data we wish. This is where a touchless, 3D  
> controller is useful. Intead of relying on the interpretation of projecting  
> the mouse onto the data set, we can interact in 3D. Allowing for one to 
> to interact with the same dimensionality as the data.  
>  
> We have programmed the a Leap Motion Controller (by the company 
> [Leap Motion](https://www.leapmotion.com/)) to take inputs by a user's 
> hand(s) that are interpreted into interaction of the data. Specifically,
> there are 4 different interactions that the user can do via the Leap Motion
> controller: move the data, take a slice of the data, rotate the camera 
> focused on the datam and zoom in or out with the camera. 

> There is also a
> script where we allow slicing, zooming and rotating on the same data set.
> These actions are called when in the view of the Leap Motion Controller
> there is one hand present, two hands present where each has at least two
> fingers extended and two hands present but one is a closed fist. There is
> also an "empty" action when one or two hands are closed where the 
> controller won't interpret anything to modify the view of the data. Note 
> that none of these actually change the data loaded, only the view or 
> present new data ontop of the data already loaded.
> 



=================================================================

###Source Code 	
- [test_move.py](code/test_move.py)
- [test_rotate.py](code/test_rotate.py)
- [test_slice.py](code/test_slice.py)
- [test_zoom.py](code/test_zoom.py)
- [test_total.py](code/test_total.py)

=================================================================
###Paper
- [Interface with 3D Data by Touchless Control via a Leap Motion Controller](papers/paper.pdf)
- [Presentation](papers/presentation.pdf)


=================================================================


###User Guide
> To use this code, you must have [Paraview](http://www.paraview.org) installed   
> specifically use of `pvpython`. This is a precompiled version of python. Other   
> versions of Python with the Paraview libraries may function, but has not been   
> tested. One must connect the Leap Motion Controller to their computer, and go   
> into the directory with the Leap Motion libraries and run one of the   
> `test_type.py` files in pvpython where "type" is describing the scripts function  
> (move, slice, rotate or zoom).  

======================  

####Moving Data: `test_move.py`
> This will move the data set, interpreting the hand's position as the position of  
> the data in the view. This position is scaled where the origin is located just   
> above the controller. Note one hand must be used, but there is no requirement as   
> to how how many fingers need to be present.

======================


####Slicing Data: `test_slice.py` 
> This will perform a slice of the data set and display it on the screen. The   
> user's hand is sensed by the controller and interprets the hand's normal from   
> the palm as the normal of the slicing plane. Note that the slicing plane is  
> always centered at the origin of the data set.

======================


####Rotating Data: `test_rotate.py`  
> This will rotate the camera about the viewing axis. This is activated by  
> placing two hands in front of the controller but one is a closed fist and the   
> the other a hand with at least two fingers present. When the user rotates their  
> non-closed hand, the camera will rotate in the same direction.

======================

####Zooming Data: `test_zoom.py`  
> This will zoom in on the data set. It is activated by placing two hands in the  
> controller's view where both hands have at least two fingers present. When the  
> user moves his or her hands away from each other, the view will zoom into the  
> data. Similarly, if a user moves his or her hands toward each other, the view  
> will zoom outwards. Note that the user can stop zooming by closing both hands,  
> which defines the "empty" action and the frame will not change when the user  
> moves his or her hands.

======================

####Slicing, Rotating, Zooming Data: `test_total.py`
> This will allow slicing, rotating and zooming in the same window. All  
> controls are the same as previously mentioned except that roation is   
> activated when two hands are present but one has no fingers present and the  
> other has at least two fingers present. There is also the inclusion of the  
> "empty" action as defined in the zooming function. This activates when two  
> hands are present with each presenting no fingers. This will stop updating   
> the view and allows for repostion of hands without changing the current   
> view.
