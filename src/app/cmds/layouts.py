from base_cmd import CmdBase

class CmdLayout(CmdBase):
    def execute(self):
        canvas = self.context.umlwin
        
        if canvas.GetDiagram().GetCount() == 0:
            return
        canvas.layout_and_position_shapes()
        
    def undo(self):  # override
        """ Docstring """
        # not implemented

class CmdLayoutExpandContractBase(CmdBase):   # BASE
    def __init__(self, remove_overlaps=True):
        self.remove_overlaps = remove_overlaps

    def ChangeScale(self, delta):
        coordmapper = self.context.coordmapper
        
        coordmapper.AllToLayoutCoords() # this used to be optional, now I do it all the time to preserve layout exactly
        coordmapper.Recalibrate(scale=coordmapper.scale + delta)
        coordmapper.AllToWorldCoords()

        if self.remove_overlaps:
            self.context.umlwin.remove_overlaps(watch_removals=False)
        self.context.umlwin.stateofthenation()
            
class CmdLayoutExpand(CmdLayoutExpandContractBase):
    def execute(self):
        if self.context.coordmapper.scale > 0.8:
            self.ChangeScale(-0.2)
            #print "expansion ", self.coordmapper.scale
        else:
            print "Max expansion prevented.", self.context.coordmapper.scale

class CmdLayoutContract(CmdLayoutExpandContractBase):
    def execute(self):
        if self.context.coordmapper.scale < 3:
            self.ChangeScale(0.2)
            #print "contraction ", self.coordmapper.scale
        else:
            print "Min expansion thwarted.", self.context.coordmapper.scale


from blackboard_frame import MainBlackboardFrame
from layout.blackboard import LayoutBlackboard

class CmdDeepLayout(CmdBase):
    def execute(self):
        """Init Main App."""
        f = MainBlackboardFrame(parent=self.context.frame)
        f.Show(True)
        
        b = LayoutBlackboard(graph=self.context.model.graph, umlwin=self.context.umlwin)
        f.SetBlackboardObject(b)
        f.Start(num_attempts=3)
        
        # any code here would run immediately, since f.Start() launches another thread.
        