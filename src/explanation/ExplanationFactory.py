from src.analysis.Technique import Technique
from src.analysis.techniques.HiddenSingle import HiddenSingle
from src.analysis.techniques.NakedSingle import NakedSingle
from src.analysis.techniques.PointingGroup import PointingGroup
from src.core.BoardState import BoardState
from src.explanation.HiddenSingleExplanation import HiddenSingleExplanation
from src.explanation.NakedSingleExplanation import NakedSingleExplanation
from src.explanation.PointingGroupExplanation import PointingGroupExplanation
from src.explanation.TechniqueExplanation import TechniqueExplanation

# Thank you https://stackoverflow.com/a/66394022 for help with the implementation.
class ExplanationFactory:
    techTypeToExplanationType: dict[type[Technique], type[TechniqueExplanation]] = {
        NakedSingle: NakedSingleExplanation,
        HiddenSingle: HiddenSingleExplanation,
        PointingGroup: PointingGroupExplanation
    }

    @classmethod
    def getExplanation(cls, technique: Technique, board: BoardState) -> TechniqueExplanation:
        techniqueType = type(technique)
        if techniqueType in cls.techTypeToExplanationType:
            return cls.techTypeToExplanationType[techniqueType](technique, board)
        
        raise NotImplementedError(f"Technique {techniqueType.__name__} not supported for explanations yet! Did you check the mappings in TechniqueExplanation.py?")