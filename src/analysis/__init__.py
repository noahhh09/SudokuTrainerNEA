from src.analysis.Technique import Technique
from src.analysis.techniques.NakedGroup import NakedPair, NakedTriple
from src.analysis.techniques.NakedSingle import NakedSingle
from src.analysis.techniques.HiddenSingle import HiddenSingle
from src.analysis.techniques.PointingGroup import PointingGroup

# Order by "relative simpleness" where 0th element is most simple.
ALL_TECHNIQUE_TYPES: list[type[Technique]] = [NakedSingle, HiddenSingle, NakedPair, PointingGroup, NakedTriple]