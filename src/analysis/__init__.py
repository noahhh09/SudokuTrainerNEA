from src.analysis.Technique import Technique
from src.analysis.techniques.NakedGroup import NakedPair, NakedTriple
from src.analysis.techniques.NakedSingle import NakedSingle
from src.analysis.techniques.HiddenSingle import HiddenSingle

# Order by "relative simpleness" where 0th element is most simple.
ALL_TECHNIQUES: list[type[Technique]] = [NakedSingle, HiddenSingle, NakedPair, NakedTriple]