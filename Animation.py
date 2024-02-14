'''
Define animation interface at here, which is used to control update of our object by frame.
Created on Oct 31, 2018

:author: micou(Zezhou Sun)
:version: 2021.1.1
'''

class Animation:
    """
    Abstract class used for animation object. Object inherit from this should implement animationUpdate method.
    """
    def animationUpdate(self):
        """
        Called when animation object need to update
        """
        raise NotImplementedError("animationUpdate method not implemented yet")