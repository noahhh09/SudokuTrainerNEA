from src.analysis.Technique import HiddenSingle, NakedSingle, Technique
from src.analysis.techniques.NakedGroup import NakedPair, NakedTriple


ALL_TECHNIQUES: list[type[Technique]] = [NakedSingle, HiddenSingle, NakedPair, NakedTriple]